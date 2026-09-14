# -*- coding: utf-8 -*-
"""
UZAKTAN ERİŞİM — panel bir bilgisayarda çalışırken başka bir şehirden açılsın.

Ağ kipi (pusula/ag.py) sadece aynı Wi-Fi içindir. İki kişi farklı yerlerdeyse
o yol hiçbir zaman çalışmaz. Doğru yol Cloudflare tüneli: panel yine bu
bilgisayarda çalışır, dışarıya tek bir https adresi açılır, adres Cloudflare
üzerinden gelir — modemde port açmak, IP ezberlemek, güvenlik duvarıyla
uğraşmak yok.

İki seçenek var:

  1) HIZLI TÜNEL — hesap gerekmiyor, tek düğme. Rastgele bir
     ...trycloudflare.com adresi verir. Adres her başlatmada değişir ve panel
     kapanınca ölür. Panelin kendi PIN/anahtar kontrolü devrede kalır.
     Denemek ve acil durumlar için.

  2) KALICI TÜNEL + ACCESS — pusula.lunayapim.com gibi sabit bir adres, önünde
     Cloudflare Access. Sadece izin verilen e-posta adresleri girebilir
     (kda.lunayapim.com'da olduğu gibi). Asıl kullanılması gereken bu.

GÜVENLİK NOTU: tünel açıkken panel internete açılmış olur. Bu yüzden tünel
kipinde "bu bilgisayar serbest" muafiyeti KALDIRILIYOR — localhost'tan gelen
istek de anahtar/PIN istiyor, çünkü tünelin trafiği de localhost'tan geliyor.
"""
import os, re, shutil, subprocess, threading, time


ADRES_KALIBI = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com")

_surec = None          # çalışan cloudflared süreci
_adres = ""            # yakalanan https adresi
_gunluk = []           # son satırlar (teşhis için)
_kilit = threading.Lock()


# ------------------------------------------------------------------ kurulum
def kurulu_mu():
    return bool(shutil.which("cloudflared"))


def surum():
    if not kurulu_mu():
        return ""
    try:
        r = subprocess.run(["cloudflared", "--version"], capture_output=True,
                           text=True, timeout=6)
        return (r.stdout or r.stderr or "").strip().splitlines()[0][:80]
    except Exception:
        return ""


KURULUM = {
    "brew": "brew install cloudflared",
    "not": ("Homebrew yoksa önce onu kur: /bin/bash -c \"$(curl -fsSL "
            "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""),
}


# ------------------------------------------------------------------ hızlı tünel
def _oku(p):
    """cloudflared çıktısını okuyup adresi yakalıyor."""
    global _adres
    for satir in iter(p.stderr.readline, ""):
        if not satir:
            break
        s = satir.rstrip()
        _gunluk.append(s)
        del _gunluk[:-60]
        m = ADRES_KALIBI.search(s)
        if m and not _adres:
            _adres = m.group(0)


def baslat(kapi):
    """
    Hızlı tüneli başlatıyor. Döner: {"ok":bool, "adres":str, "sorun":str}
    Adres birkaç saniyede geliyor; gelene kadar bekliyoruz.
    """
    global _surec, _adres
    with _kilit:
        if _surec and _surec.poll() is None:
            return {"ok": True, "adres": _adres, "not": "Tünel zaten açık."}
        if not kurulu_mu():
            return {"ok": False, "sorun": "cloudflared kurulu değil.",
                    "kurulum": KURULUM}
        _adres = ""
        _gunluk.clear()
        try:
            _surec = subprocess.Popen(
                ["cloudflared", "tunnel", "--no-autoupdate",
                 "--url", "http://127.0.0.1:%d" % kapi],
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        except Exception as ex:
            return {"ok": False, "sorun": "%s: %s" % (type(ex).__name__, ex)}
        threading.Thread(target=_oku, args=(_surec,), daemon=True).start()

    for _ in range(60):                     # en fazla 30 saniye
        if _adres:
            return {"ok": True, "adres": _adres}
        if _surec.poll() is not None:
            return {"ok": False, "sorun": "cloudflared kapandı.",
                    "gunluk": _gunluk[-12:]}
        time.sleep(0.5)
    return {"ok": False, "sorun": "Adres 30 saniyede gelmedi.",
            "gunluk": _gunluk[-12:]}


def durdur():
    global _surec, _adres
    with _kilit:
        if _surec and _surec.poll() is None:
            try:
                _surec.terminate()
                _surec.wait(timeout=8)
            except Exception:
                try:
                    _surec.kill()
                except Exception:
                    pass
        _surec = None
        _adres = ""
    return {"ok": True}


def calisiyor_mu():
    return bool(_surec and _surec.poll() is None and _adres)


def durum(kapi=None):
    return {
        "kurulu": kurulu_mu(),
        "surum": surum(),
        "calisiyor": calisiyor_mu(),
        "adres": _adres,
        "kurulum": KURULUM,
        "gunluk": _gunluk[-8:],
    }


# ------------------------------------------------------------------ kalıcı tünel
def kalici_adimlar(alan="pusula.lunayapim.com", kapi=8765):
    """
    Kalıcı tünel + Access kurulumu. Tarayıcı gerektiren iki adım otomatikleşmiyor;
    o yüzden komutlar kopyalanabilir hâlde veriliyor.
    """
    return [
        {"baslik": "cloudflared kur",
         "komut": KURULUM["brew"],
         "aciklama": "Terminal'e yapıştır. Zaten kuruluysa atla."},
        {"baslik": "Cloudflare hesabına bağla",
         "komut": "cloudflared tunnel login",
         "aciklama": "Tarayıcı açılır; lunayapim.com alan adını seç. Bir kez yapılıyor."},
        {"baslik": "Tüneli oluştur",
         "komut": "cloudflared tunnel create pusula",
         "aciklama": "Bir kez. 'pusula' adında tünel oluşturur."},
        {"baslik": "Adresi tünele bağla",
         "komut": "cloudflared tunnel route dns pusula %s" % alan,
         "aciklama": "DNS kaydını Cloudflare kendisi ekliyor."},
        {"baslik": "Tüneli çalıştır",
         "komut": "cloudflared tunnel run --url http://127.0.0.1:%d pusula" % kapi,
         "aciklama": "Panel açıkken bu komut da açık kalmalı. Her gün bu komut."},
        {"baslik": "Access ile kapıyı kilitle",
         "komut": "",
         "aciklama": "one.dash.cloudflare.com → Access → Applications → Add an "
                     "application → Self-hosted → %s → Policy: Emails → senin ve "
                     "eşinin e-posta adresi. Bundan sonra adrese giren herkes önce "
                     "e-postasına gelen kodu giriyor — kda.lunayapim.com'daki düzenin "
                     "aynısı." % alan},
    ]


def access_epostasi(basliklar):
    """
    Cloudflare Access arkasındaysa hangi e-postanın girdiğini söylüyor.
    Bu başlığı yalnızca Cloudflare ekleyebiliyor; tünel dışından gelen istekte
    dikkate ALINMIYOR (panel.py bunu ayrıca kontrol ediyor).
    """
    try:
        return (basliklar.get("Cf-Access-Authenticated-User-Email") or "").strip().lower()
    except Exception:
        return ""


def tunelden_mi(basliklar):
    """İstek Cloudflare tünelinden mi geldi (localhost muafiyeti burada geçersiz)."""
    try:
        return bool(basliklar.get("Cf-Connecting-Ip") or basliklar.get("Cf-Ray"))
    except Exception:
        return False
