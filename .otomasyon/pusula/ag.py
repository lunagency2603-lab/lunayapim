# -*- coding: utf-8 -*-
"""
AĞ KİPİ — paneli ikinci bir bilgisayardan açabilmek için.

Panel varsayılan olarak sadece bu bilgisayardan açılır (127.0.0.1). Ağ kipi
açıldığında aynı ev/ofis ağındaki başka bir bilgisayar da panele girebilir.

Kurallar:
  • Veritabanı TEK yerde durur — panelin çalıştığı bilgisayarda. İkinci
    bilgisayar sadece tarayıcıyla bağlanır. (pusula.db'yi iCloud/Dropbox
    üzerinden iki makinede birden açmak veriyi bozar; bu yüzden o yol
    kapalı tutuluyor.)
  • Ağ kipi açıkken erişim anahtarı zorunlu. Anahtarsız istek 403 döner.
  • Anahtar bir kez üretilip ag-anahtar.txt dosyasında saklanır. Adres
    çubuğuna bir kez yapıştırılınca tarayıcıya çerez olarak yazılır.
  • Ağ kipi kendiliğinden açılmaz — Panel-Ag.command veya PUSULA_AG=1 gerekir.
"""
import os, socket, secrets, time, threading, http.cookies

from .ayarlar import AYAR_DOSYA

CEREZ_AD = "pusula_anahtar"


def _anahtar_yolu():
    return os.path.join(os.path.dirname(AYAR_DOSYA), "ag-anahtar.txt")


def anahtar(yenile=False):
    """Erişim anahtarını okur; yoksa (ya da yenile=True ise) üretir."""
    y = _anahtar_yolu()
    if not yenile and os.path.isfile(y):
        try:
            with open(y, encoding="utf-8") as f:
                a = f.read().strip()
            if len(a) >= 12:
                return a
        except Exception:
            pass
    a = secrets.token_urlsafe(15)
    try:
        with open(y, "w", encoding="utf-8") as f:
            f.write(a + "\n")
        os.chmod(y, 0o600)
    except Exception:
        pass
    return a


def _pin_yolu():
    return os.path.join(os.path.dirname(AYAR_DOSYA), "ag-pin.txt")


def pin(yenile=False):
    """
    Adres çubuğuna uzun anahtar yapıştırmak yerine girilecek kısa şifre.
    Sekiz hane: telefonda okunacak kadar kısa, denemeyle bulunamayacak kadar
    uzun (aşağıdaki deneme sınırıyla birlikte).
    """
    y = _pin_yolu()
    if not yenile and os.path.isfile(y):
        try:
            with open(y, encoding="utf-8") as f:
                a = "".join(ch for ch in f.read() if ch.isdigit())
            if len(a) >= 6:
                return a
        except Exception:
            pass
    a = "".join(secrets.choice("0123456789") for _ in range(8))
    try:
        with open(y, "w", encoding="utf-8") as f:
            f.write(a + "\n")
        os.chmod(y, 0o600)
    except Exception:
        pass
    return a


def pin_okunakli(p=None):
    """4-4 ayrılmış hâli: telefonda söylemesi kolay olsun."""
    p = p or pin()
    return p[:4] + " " + p[4:] if len(p) == 8 else p


# ---------------------------------------------------------------- deneme sınırı
# Panel tünelle internete açılabildiği için PIN denemesi serbest bırakılamaz.
_DENEME = {}
_D_KILIT = threading.Lock()
DENEME_HAKKI = 5
DENEME_PENCERE = 600          # saniye


def deneme_hakki(ip):
    """Kalan deneme hakkı ve kilitliyse ne kadar kaldığı."""
    simdi = time.time()
    with _D_KILIT:
        d = [t for t in _DENEME.get(ip, []) if simdi - t < DENEME_PENCERE]
        _DENEME[ip] = d
    kalan = max(0, DENEME_HAKKI - len(d))
    bekle = 0
    if kalan == 0 and d:
        bekle = int(DENEME_PENCERE - (simdi - min(d))) + 1
    return {"kalan": kalan, "bekle": bekle}


def deneme_isle(ip, dogru):
    """Yanlış denemeyi sayıyor, doğru girişte sayacı sıfırlıyor."""
    with _D_KILIT:
        if dogru:
            _DENEME.pop(ip, None)
        else:
            _DENEME.setdefault(ip, []).append(time.time())


def yerel_ip():
    """
    Bu bilgisayarın yerel ağdaki adresi. Dışarı paket göndermeden,
    yönlendiriciye yönelen bir UDP soketinin yerel ucuna bakarak buluyor.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def makine_adi():
    """
    Bonjour/mDNS adı (macOS'ta 'Macbook.local'). IP değişse bile bu ad aynı
    kalıyor — yönlendirici yeni bir IP verdiğinde bağlantı kopmasın diye
    ikinci bir adres olarak veriliyor.
    """
    try:
        ad = socket.gethostname().strip()
    except Exception:
        return ""
    if not ad or ad.startswith("localhost"):
        return ""
    ad = ad.split(".")[0]
    return ad + ".local"


def panoya_kopyala(metin):
    """Adresi panoya koyuyor — kullanıcı terminalden elle kopyalamasın."""
    import subprocess, sys as _s
    komut = None
    if _s.platform == "darwin":
        komut = ["pbcopy"]
    elif _s.platform.startswith("linux"):
        for k in (["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "-ib"]):
            try:
                subprocess.run(["which", k[0]], capture_output=True, check=True)
                komut = k
                break
            except Exception:
                continue
    if not komut:
        return False
    try:
        p = subprocess.Popen(komut, stdin=subprocess.PIPE)
        p.communicate(metin.encode("utf-8"), timeout=5)
        return p.returncode == 0
    except Exception:
        return False


def adresler(kapi, anah=None):
    """
    İkinci bilgisayara verilecek adreslerin tamamı.
    Birincisi IP'li, ikincisi (varsa) makine adlı — IP değişirse ikincisi çalışır.
    """
    a = anah or anahtar()
    liste = []
    ip = yerel_ip()
    if not ip.startswith("127."):
        liste.append({"ad": "Ağ adresi", "url": "http://%s:%d/?anahtar=%s" % (ip, kapi, a),
                      "not": "En güvenilir olan bu. Yönlendirici IP'yi değiştirirse alttakini kullan."})
    m = makine_adi()
    if m:
        liste.append({"ad": "Bilgisayar adı", "url": "http://%s:%d/?anahtar=%s" % (m, kapi, a),
                      "not": "IP değişse bile bu adres aynı kalıyor (macOS ve Windows 10+ tanır)."})
    if not liste:
        liste.append({"ad": "Ağ bulunamadı",
                      "url": "http://%s:%d/?anahtar=%s" % (ip, kapi, a),
                      "not": "Yerel ağ adresi okunamadı — bilgisayar ağa bağlı değil gibi görünüyor."})
    return liste


def ag_var_mi():
    """Yerel ağ adresi bulunabildi mi? Bulunamazsa verilecek adres işe yaramaz."""
    return not yerel_ip().startswith("127.")


def adres(kapi, anah=None):
    """İkinci bilgisayara verilecek tam adres."""
    return "http://%s:%d/?anahtar=%s" % (yerel_ip(), kapi, anah or anahtar())


def cerezden(baslik):
    """İstek başlığındaki çerezden anahtarı çıkarır."""
    if not baslik:
        return ""
    try:
        c = http.cookies.SimpleCookie()
        c.load(baslik)
        return c[CEREZ_AD].value if CEREZ_AD in c else ""
    except Exception:
        return ""


def cerez_basligi(anah):
    # SameSite=Lax: adres çubuğundan girişte çerez gider, dışarıdan tetiklenen
    # isteklerde gitmez. Yerel ağda HTTPS olmadığı için Secure konulmuyor.
    return "%s=%s; Path=/; Max-Age=31536000; SameSite=Lax" % (CEREZ_AD, anah)


def giris_sayfasi(mesaj="", kalan=None):
    """
    Anahtarsız gelen herkese gösterilen giriş ekranı.
    Uzun bağlantıyı yapıştırmak yerine PIN yazmak yetiyor.
    """
    uyari = ('<p class="uyari">%s</p>' % mesaj) if mesaj else ""
    ipucu = ""
    if kalan is not None and 0 < kalan <= 3:
        ipucu = '<p class="ipucu">Kalan deneme hakkı: %d</p>' % kalan
    return (_GIRIS_KALIP
            .replace("{{UYARI}}", uyari)
            .replace("{{IPUCU}}", ipucu))


_GIRIS_KALIP = """<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Luna Pusula — giriş</title>
<style>
 *{box-sizing:border-box}
 body{margin:0;min-height:100vh;display:grid;place-items:center;background:#14110f;
      color:#efe7dd;font:15px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;padding:20px}
 .k{width:100%;max-width:390px;padding:34px 30px;border:1px solid #2a2724;
    border-radius:12px;background:#1a1715}
 .logo{font-weight:800;letter-spacing:.02em;font-size:15px;margin-bottom:22px}
 .logo span{color:#e8452c}
 h1{font-size:20px;margin:0 0 6px}
 p{color:#a49a90;margin:0 0 18px;font-size:14px}
 input{width:100%;background:#12100f;color:#efe7dd;border:1px solid #2a2724;
       border-radius:8px;padding:15px;font:600 25px/1 ui-monospace,Menlo,monospace;
       letter-spacing:.28em;text-align:center}
 input:focus{outline:none;border-color:#e8452c}
 button{width:100%;margin-top:14px;background:#e8452c;border:0;color:#fff;
        padding:14px;border-radius:8px;font:600 15px/1 inherit;cursor:pointer}
 .uyari{background:#3a1f1f;color:#e8907c;padding:11px 13px;border-radius:8px;
        margin:0 0 16px;font-size:13.5px}
 .ipucu{color:#a49a90;font-size:12.5px;margin:12px 0 0;text-align:center}
 .alt{color:#6f665e;font-size:12.5px;margin:20px 0 0;line-height:1.5}
</style></head><body><form class="k" method="POST" action="/giris">
 <div class="logo">LUNA <span>PUSULA</span></div>
 {{UYARI}}
 <h1>Giriş</h1>
 <p>Panelin çalıştığı bilgisayardaki sekiz haneli PIN'i gir. Bir kez giriyorsun —
    bu tarayıcı bir daha sormuyor.</p>
 <input type="text" name="pin" inputmode="numeric" autocomplete="one-time-code"
        pattern="[0-9 ]*" maxlength="11" placeholder="- - - -  - - - -" autofocus>
 <button type="submit">Gir</button>
 {{IPUCU}}
 <p class="alt">PIN'i bilmiyorsan panelin açık olduğu bilgisayarda
    Kılavuz sekmesine bak; orada yazıyor.</p>
</form></body></html>"""


# Eski adı kullanan yerler için
RET_SAYFA = giris_sayfasi()
