# -*- coding: utf-8 -*-
"""
DEPO — site deposunun sağlığı ve takılan git kilidi.

Neden var: GitHub Desktop bir işlemi yarıda kesildiğinde (uygulama kapanır,
bilgisayar uyur, eşzamanlı iki işlem çakışır) .git/index.lock dosyası geride
kalıyor. Git bunu "başka bir git süreci çalışıyor" sanıp bütün yazma
işlemlerini reddediyor. Hata mesajı şu:

    A lock file already exists in the repository, which blocks this operation

Çözümü tek satır: kilit dosyasını silmek. Ama bunun için terminal açmak
gerekiyordu; artık gerekmiyor.

GÜVENLİK: Kilidi silmeden önce gerçekten çalışan bir git süreci var mı diye
bakıyoruz. Varsa DOKUNMUYORUZ — çalışan bir git'in kilidini silmek depoyu
bozabilir. Ayrıca kilit dosyası boş değilse (içinde veri varsa) yarım kalmış
bir yazma işlemi olabilir; o durumda da uyarıp bırakıyoruz.
"""
import os, re, subprocess, datetime

from .ayarlar import SITE_KOK

KILIT_YOLLARI = ("index.lock", "HEAD.lock", "config.lock",
                 "refs/heads/main.lock", "refs/heads/master.lock",
                 "ORIG_HEAD.lock", "shallow.lock")


def _git(kok, *arg, zaman=20):
    """Sadece OKUMA komutları için. Yazma komutu bu modülden çalıştırılmıyor."""
    try:
        # --no-optional-locks: git durum okurken index.lock ALMAZ.
        # (Bu bayrak olmadan 'git status' bile kilit oluşturuyor ve dosya silme
        #  yetkisinin kısıtlı olduğu ortamlarda kilit geride kalıyor.)
        p = subprocess.run(("git", "--no-optional-locks") + arg, cwd=kok,
                           capture_output=True, text=True, timeout=zaman)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as ex:
        return 1, "", "%s: %s" % (type(ex).__name__, ex)


def _git_calisiyor():
    """Şu an çalışan bir git süreci var mı? Varsa kilide dokunmuyoruz."""
    try:
        p = subprocess.run(["ps", "-Ao", "comm="], capture_output=True, text=True, timeout=10)
        satirlar = [s.strip() for s in (p.stdout or "").splitlines()]
        return [s for s in satirlar if s.endswith("/git") or s == "git"]
    except Exception:
        return []


def kilitleri_bul(kok=None):
    kok = kok or SITE_KOK
    g = os.path.join(kok, ".git")
    if not os.path.isdir(g):
        return []
    bulunan = []
    for ad in KILIT_YOLLARI:
        y = os.path.join(g, ad)
        if os.path.isfile(y):
            st = os.stat(y)
            bulunan.append({
                "ad": ad, "yol": y, "bayt": st.st_size,
                "yas_dk": int((datetime.datetime.now().timestamp() - st.st_mtime) / 60),
                "zaman": datetime.datetime.fromtimestamp(st.st_mtime).strftime("%d.%m.%Y %H:%M"),
            })
    return bulunan


def durum(kok=None):
    """Deponun tek bakışta hâli."""
    kok = kok or SITE_KOK
    d = {"kok": kok, "depo_mu": os.path.isdir(os.path.join(kok, ".git")),
         "kilit": [], "surec": [], "dal": None, "degisiklik": 0,
         "yeni": 0, "degisen": 0, "silinen": 0, "son_islem": None, "hata": None}
    if not d["depo_mu"]:
        d["hata"] = "Bu klasör bir git deposu değil: %s" % kok
        return d
    d["kilit"] = kilitleri_bul(kok)
    d["surec"] = _git_calisiyor()

    kod, cikti, _ = _git(kok, "rev-parse", "--abbrev-ref", "HEAD")
    d["dal"] = cikti if kod == 0 else None
    kod, cikti, hata = _git(kok, "status", "--porcelain")
    if kod == 0:
        satir = [s for s in cikti.splitlines() if s.strip()]
        d["degisiklik"] = len(satir)
        for s in satir:
            im = s[:2]
            if "?" in im:
                d["yeni"] += 1
            elif "D" in im:
                d["silinen"] += 1
            else:
                d["degisen"] += 1
    else:
        d["hata"] = hata[:200]
    kod, cikti, _ = _git(kok, "log", "-1", "--format=%h · %ad · %s", "--date=format:%d.%m.%Y %H:%M")
    d["son_islem"] = cikti if kod == 0 else None
    return d


def kilit_coz(kok=None, zorla=False):
    """
    Bayat kilitleri kaldırır.
    zorla=False iken: çalışan git süreci varsa ya da kilit dosyası doluysa dokunmaz.
    """
    kok = kok or SITE_KOK
    kilitler = kilitleri_bul(kok)
    surec = _git_calisiyor()
    sonuc = {"kaldirilan": [], "atlanan": [], "surec": surec, "kok": kok}

    if not kilitler:
        sonuc["mesaj"] = "Kilit yok — depo zaten açık."
        return sonuc

    if surec and not zorla:
        sonuc["atlanan"] = [k["ad"] for k in kilitler]
        sonuc["mesaj"] = ("Şu anda çalışan bir git süreci var (%s). Çalışan git'in kilidini "
                          "silmek depoyu bozabilir. Önce GitHub Desktop'ta işlemin bitmesini "
                          "bekleyin; sürmüyorsa uygulamayı kapatıp tekrar deneyin."
                          % ", ".join(surec[:3]))
        return sonuc

    cop = os.path.join(kok, ".git", "bayat-kilit")
    os.makedirs(cop, exist_ok=True)
    damga = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    for k in kilitler:
        if k["bayt"] > 0 and not zorla:
            sonuc["atlanan"].append(k["ad"])
            continue
        hedef = os.path.join(cop, "%s.%s" % (k["ad"].replace("/", "_"), damga))
        try:
            os.replace(k["yol"], hedef)          # önce yeniden adlandır
            try:
                os.remove(hedef)                  # silinebiliyorsa tamamen kaldır
                nasil = "silindi"
            except OSError:
                nasil = "kenara alındı (.git/bayat-kilit)"
            sonuc["kaldirilan"].append({"ad": k["ad"], "nasil": nasil,
                                        "yas_dk": k["yas_dk"], "zaman": k["zaman"]})
        except OSError as ex:
            sonuc["atlanan"].append("%s (%s)" % (k["ad"], ex.strerror or ex))

    if sonuc["kaldirilan"]:
        sonuc["mesaj"] = ("%d kilit kaldırıldı. GitHub Desktop'a dönüp işlemi tekrar "
                          "deneyebilirsin." % len(sonuc["kaldirilan"]))
    if sonuc["atlanan"]:
        sonuc["mesaj"] = (sonuc.get("mesaj", "") + " "
                          "Şunlara dokunulmadı (içi dolu — yarım kalmış bir yazma olabilir): %s. "
                          "Emin isen 'zorla' seçeneğiyle tekrar dene."
                          % ", ".join(str(a) for a in sonuc["atlanan"])).strip()

    # yarım kalmış geçici nesneler de gürültü yapıyor, onları da topla
    nesne = os.path.join(kok, ".git", "objects")
    yarim = 0
    if os.path.isdir(nesne):
        for dizin, _, dosyalar in os.walk(nesne):
            for d in dosyalar:
                if d.startswith("tmp_obj_"):
                    try:
                        os.remove(os.path.join(dizin, d)); yarim += 1
                    except OSError:
                        pass
    sonuc["yarim_nesne"] = yarim
    return sonuc
