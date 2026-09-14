# -*- coding: utf-8 -*-
"""
ÜRETİM KATMANI — görsel ve video üretim araçlarının tek kapısı.

Amaç: hangi araç, hangi yol (API mi tarayıcı mı), kaç kredi — hepsi tek yerde.
Kredi harcayan hiçbir çağrı onaysız gitmez: önce tahmin, sonra onay=True.

Yollar:
  · API      → Runway (anahtar: Ayarlar → Üretim). Tarayıcıya gerek yok.
  · Kuyruk   → API'si olmayan araçlar (Higgsfield, Kling/Veo Higgsfield içinden).
               İş veri/uretim/kuyruk.json'a düşer; tarayıcıdan üretilip
               'tamamla()' ile dosya yolu verilince zincir devam eder.
  · Yerel    → Pillow + ffmpeg (sıfır maliyet): poster, kapak, kodlama, kırpma.

Sonuç ne olursa olsun aynı yere gider: assets/video/<ad>.{mp4,webm,jpg} ve
videolar.js kaydı. Yani üretilen şey saniyesinde sitede kullanılabilir hâle gelir.
"""
import datetime, json, os, re, subprocess, tempfile, time, urllib.request, urllib.error

from .ayarlar import KOK_DIZIN, SITE_KOK, _OZEL

RUNWAY_URL = "https://api.dev.runwayml.com/v1"
RUNWAY_SURUM = "2024-11-06"
RUNWAY_ANAHTAR = (_OZEL.get("runway_anahtar") or os.environ.get("RUNWAYML_API_SECRET", "")).strip()

# Kredi tahmini (saniye başına). Kaynak: Runway'in yayınladığı birim fiyatlar +
# 02.09.2026 ölçümü (uygulama içi Seedance 2, 5 sn 720p = 180 kredi = 36/sn).
# API fiyatı uygulama fiyatından FARKLI olabilir; ilk gerçek çağrıdan sonra
# ayarlar.json → "kredi_sn" ile üzerine yaz.
KREDI_SN = {
    # Uygulama içi ÖLÇÜLEN değerler (02.09.2026, Pro plan, kredi/sn):
    #   gen4_turbo 5 (25 kredi / 5 sn), seedance_2_5 30 (150 / 5 sn 720p 16:9),
    #   seedance_2_5 + video referans + HDR: 226 / 5 sn ölçüldü → referanslı üretimde ~45/sn say.
    "gen4_turbo": 5, "gen4.5": 12, "seedance_2_app": 36, "seedance_2_5_app": 30,
    "seedance_2_5_ref_app": 45, "veo_3_1": 40, "aleph": 15,
    "gen4_image": 5,          # görsel başına (saniye değil, adet)
}

# Bağlayıcı yolu (03.09.2026'dan itibaren tercih edilen): Runway ve Higgsfield'in resmi MCP
# bağlayıcıları Claude'a eklenince üretim tarayıcısız, doğrudan sohbetten yapılır; uygulama
# kredilerini kullanır, API anahtarı gerekmez.
#   Runway:     https://mcp.runwayml.com/mcp      (Claude → Customize → Connectors → Add)
#   Higgsfield: https://mcp.higgsfield.ai/mcp
# Bu dosyadaki API/kuyruk yolları yedek olarak kalır.
MCP_BAGLAYICI = {"runway": "https://mcp.runwayml.com/mcp", "higgsfield": "https://mcp.higgsfield.ai/mcp"}
KREDI_SN.update(_OZEL.get("kredi_sn", {}))

KUYRUK = os.path.join(KOK_DIZIN, "veri", "uretim", "kuyruk.json")
VIDEO_DIZIN = os.path.join(SITE_KOK or "", "assets", "video")


# ---------------------------------------------------------------- tahmin
def tahmin(tur, arac="runway", model=None, sn=5, adet=1):
    """Kredi ve yol tahmini — onaydan önce gösterilir."""
    if arac == "yerel":
        return {"yol": "yerel", "kredi": 0, "not": "Pillow + ffmpeg, maliyet yok."}
    if arac == "higgsfield":
        return {"yol": "kuyruk", "kredi": None,
                "not": "API yok; tarayıcıdan üretilir. Unlimited açıksa kredisiz, değilse ~36 kredi/üretim."}
    if tur == "gorsel":
        m = model or "gen4_image"
        return {"yol": "api" if RUNWAY_ANAHTAR else "kuyruk", "kredi": KREDI_SN.get(m, 5) * adet,
                "model": m, "not": "görsel başına"}
    m = model or "gen4_turbo"
    return {"yol": "api" if RUNWAY_ANAHTAR else "kuyruk", "kredi": KREDI_SN.get(m, 12) * sn * adet,
            "model": m, "sn": sn, "not": "%d kredi/sn × %d sn × %d" % (KREDI_SN.get(m, 12), sn, adet)}


# ---------------------------------------------------------------- Runway API
def _runway(yol, govde=None, metot="POST"):
    if not RUNWAY_ANAHTAR:
        raise RuntimeError("Runway API anahtarı yok (Ayarlar → Üretim).")
    veri = json.dumps(govde).encode("utf-8") if govde is not None else None
    istek = urllib.request.Request(RUNWAY_URL + yol, data=veri, method=metot, headers={
        "Authorization": "Bearer " + RUNWAY_ANAHTAR, "X-Runway-Version": RUNWAY_SURUM,
        "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(istek, timeout=60) as c:
            return json.loads(c.read().decode("utf-8", "ignore"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("Runway %s: %s" % (e.code, e.read().decode("utf-8", "ignore")[:300]))


def runway_bekle(gorev_id, azami_sn=600):
    bas = time.time()
    while time.time() - bas < azami_sn:
        d = _runway("/tasks/" + gorev_id, metot="GET")
        durum = d.get("status")
        if durum == "SUCCEEDED":
            return d
        if durum in ("FAILED", "CANCELLED"):
            raise RuntimeError("Runway görevi %s: %s" % (durum, d.get("failure") or d.get("failureCode") or ""))
        time.sleep(6)
    raise RuntimeError("Runway görevi zaman aşımı")


def runway_video(metin, sn=5, oran="1280:720", model="gen4_turbo", gorsel_uri=None):
    """Metinden (ya da görselden) video. Döner: çıktı URL listesi."""
    govde = {"model": model, "promptText": metin, "ratio": oran, "duration": int(sn)}
    if gorsel_uri:
        govde["promptImage"] = gorsel_uri
    d = _runway("/image_to_video", govde)
    s = runway_bekle(d["id"])
    return s.get("output") or []


def runway_gorsel(metin, oran="1920:1080", model="gen4_image", referanslar=()):
    govde = {"model": model, "promptText": metin, "ratio": oran}
    if referanslar:
        govde["referenceImages"] = [{"uri": u} for u in referanslar]
    d = _runway("/text_to_image", govde)
    s = runway_bekle(d["id"])
    return s.get("output") or []


def indir(url, hedef):
    with urllib.request.urlopen(url, timeout=120) as c, open(hedef, "wb") as f:
        f.write(c.read())
    return hedef


# ---------------------------------------------------------------- kuyruk (tarayıcı yolu)
def _kuyruk_oku():
    try:
        return json.load(open(KUYRUK, encoding="utf-8"))
    except Exception:
        return []


def _kuyruk_yaz(k):
    os.makedirs(os.path.dirname(KUYRUK), exist_ok=True)
    json.dump(k, open(KUYRUK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def kuyruga_al(ad, tur, arac, metin, sn=5, oran="16:9", not_=""):
    k = _kuyruk_oku()
    is_ = {"id": "%s-%s" % (datetime.datetime.now().strftime("%Y%m%d%H%M%S"), ad), "ad": ad,
           "tur": tur, "arac": arac, "metin": metin, "sn": sn, "oran": oran, "not": not_,
           "durum": "bekliyor", "olusturma": datetime.datetime.now().isoformat(timespec="seconds")}
    k.append(is_); _kuyruk_yaz(k)
    return is_


def tamamla(is_id, dosya_yolu):
    """Tarayıcıdan üretilen dosyayı kuyruktaki işe bağlar ve siteye yerleştirir."""
    k = _kuyruk_oku()
    for is_ in k:
        if is_["id"] == is_id:
            is_["durum"] = "tamam"; is_["dosya"] = dosya_yolu
            _kuyruk_yaz(k)
            return yerlestir(dosya_yolu, is_["ad"])
    raise KeyError(is_id)


# ---------------------------------------------------------------- yerleştirme (sıfır maliyet)
def yerlestir(kaynak, ad, kirp_sn=None, renk=True):
    """Üretilen videoyu site paletine göre kodlar: mp4 + webm + poster; videolar.js'e kaydeder."""
    os.makedirs(VIDEO_DIZIN, exist_ok=True)
    ad = re.sub(r"[^a-z0-9-]", "-", ad.lower())
    mp4 = os.path.join(VIDEO_DIZIN, ad + ".mp4")
    webm = os.path.join(VIDEO_DIZIN, ad + ".webm")
    jpg = os.path.join(VIDEO_DIZIN, ad + ".jpg")
    vf = "eq=contrast=1.06:saturation=0.94,format=yuv420p" if renk else "format=yuv420p"
    kes = ["-t", str(kirp_sn)] if kirp_sn else []
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", kaynak] + kes +
                   ["-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", "24",
                    "-movflags", "+faststart", "-an", mp4], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", kaynak] + kes +
                   ["-vf", vf.replace(",format=yuv420p", ""), "-c:v", "libvpx-vp9", "-crf", "36",
                    "-b:v", "0", "-deadline", "good", "-cpu-used", "2", "-an", webm], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1.5", "-i", mp4, "-frames:v", "1",
                    "-q:v", "3", jpg], check=True)
    return {"mp4": mp4, "webm": webm, "poster": jpg, "boyut_kb": round(os.path.getsize(mp4) / 1024)}


# ---------------------------------------------------------------- tek kapı
def uret(tur, metin, ad, arac="runway", sn=5, oran="1280:720", model=None, onay=False, gorsel_uri=None):
    """
    tur: "video" | "gorsel"
    Kredi harcayacaksa onay=True şart; aksi hâlde yalnızca tahmin döner.
    """
    t = tahmin(tur, arac, model, sn)
    if t["yol"] == "yerel":
        raise ValueError("Yerel üretim için onizleme.py / Pillow kullan.")
    if t["yol"] == "kuyruk":
        is_ = kuyruga_al(ad, tur, arac, metin, sn, oran, t.get("not", ""))
        return {"yol": "kuyruk", "is": is_, "tahmin": t,
                "mesaj": "API yok ya da anahtar girilmemiş — iş kuyruğa alındı; tarayıcıdan üretilip tamamla() ile bağlanır."}
    if not onay:
        return {"yol": "api", "tahmin": t, "onay_gerekli": True,
                "mesaj": "Tahmini %s kredi. Üretmek için onay=True." % t["kredi"]}
    gecici = tempfile.mkdtemp(prefix="luna-uretim-")
    if tur == "gorsel":
        cikti = runway_gorsel(metin, oran.replace(":", ":"), t["model"])
        yol = indir(cikti[0], os.path.join(gecici, ad + ".png"))
        return {"yol": "api", "dosya": yol, "tahmin": t}
    cikti = runway_video(metin, sn, oran, t["model"], gorsel_uri)
    ham = indir(cikti[0], os.path.join(gecici, ad + ".mp4"))
    return {"yol": "api", "dosya": ham, "site": yerlestir(ham, ad), "tahmin": t}


# ---------------------------------------------------------------- karga seti
KARGA_REF = "The same crow from Video 1, same warm amber backlight and near-black background. "
KARGA = [
    ("karga-k2", KARGA_REF + "The crow takes off from the branch toward frame right in slow motion, feathers catching a single hard rim light, motion blur on the wingtips, volumetric haze drifting through the light, anamorphic lens, restrained cinematic look, film grain. Static camera. No text, no logos, no people."),
    ("karga-k3", KARGA_REF + "Extreme close-up of the crow's eye and beak, the amber light catching the eye, slow push-in, shallow depth of field, film grain, teal shadows and amber highlights. No text, no logos, no people."),
    ("karga-k4", KARGA_REF + "The crow glides low over a construction site at golden hour, drone-follow shot from behind, dust in the light beams, long shadows, cinematic and restrained. No text, no logos, no people."),
    ("karga-k5", KARGA_REF + "The crow lands on a rooftop antenna at night, wide shot, city lights as soft bokeh behind, one amber rim light, anamorphic lens. No text, no logos, no people."),
    ("karga-k6", KARGA_REF + "The crow slowly turns its head toward camera, static camera, pure black background, minimal, seamless loop, subtle rim light only. No text, no logos, no people."),
]
# Üretim yolu: Runway Seedance 2.5 + Video 1 = karga-k1 (Assets'te "agent_generate_video - Silhouette").
# 9:16 sürümü ayrı üretilmez; ffmpeg ile merkezden kırpılır (uretim.dikey_kirp).


def karga_plani(model="gen4_turbo", sn=5):
    """Karga setinin toplam kredi tahmini — üretmeden önce göster."""
    t = tahmin("video", "runway", model, sn, adet=len(KARGA))
    return {"adet": len(KARGA), "model": model, "sn": sn, "kredi": t["kredi"], "yol": t["yol"],
            "klipler": [a for a, _ in KARGA]}


def dikey_kirp(kaynak, ad):
    """16:9 klipten 9:16 sürüm: merkezden kırp, assets/video/<ad>-dikey.mp4/.webm/.jpg."""
    import subprocess
    hedef = os.path.join(VIDEO_DIZIN, ad + "-dikey")
    vf = "crop=ih*9/16:ih,scale=720:1280"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", kaynak, "-vf", vf, "-c:v", "libx264", "-crf", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", hedef + ".mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", kaynak, "-vf", vf, "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "36", "-an", hedef + ".webm"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", hedef + ".mp4", "-ss", "1", "-frames:v", "1", "-q:v", "4", hedef + ".jpg"], check=True)
    return hedef + ".mp4"
