# -*- coding: utf-8 -*-
"""
X (Twitter) paylaşımı — stdlib, OAuth 1.0a (kullanıcı bağlamı), API v2 POST /2/tweets.

Kurulum (bir kez, kullanıcı yapar):
  1. developer.x.com → Projects & Apps → uygulama oluştur (Free tier yazma için yeter).
  2. User authentication settings → Read and Write.
  3. Keys: API Key, API Key Secret, Access Token, Access Token Secret üret.
  4. Panel → Ayarlar → X'e yapıştır  (ayarlar.json → "x": {...})  ya da ortam:
     LUNA_X_ANAHTAR, LUNA_X_GIZLI, LUNA_X_JETON, LUNA_X_JETON_GIZLI

Kullanım:
  x_paylas.paylas("metin", "https://lunayapim.com/trend/...")  → {"id": "...", "url": "..."}
  x_paylas.sinama()                                             → yetki var mı (gönderim yapmaz)

Kural: aynı bağlantı bir kez paylaşılır (veri/x/paylasim.json). Otomatik paylaşım
trend.yayinla(paylas=True) ile; kapatmak için ayarlar.json → "x": {"otomatik": false}.
"""
import base64, hashlib, hmac, json, os, time, urllib.parse, urllib.request, uuid

from .ayarlar import KOK_DIZIN, _OZEL

X = {"anahtar": "", "gizli": "", "jeton": "", "jeton_gizli": "", "otomatik": True}
X.update(_OZEL.get("x", {}))
for k, env in (("anahtar", "LUNA_X_ANAHTAR"), ("gizli", "LUNA_X_GIZLI"), ("jeton", "LUNA_X_JETON"), ("jeton_gizli", "LUNA_X_JETON_GIZLI")):
    if not X[k]:
        X[k] = os.environ.get(env, "").strip()

KAYIT = os.path.join(KOK_DIZIN, "veri", "x", "paylasim.json")


def hazir():
    return all(X[k] for k in ("anahtar", "gizli", "jeton", "jeton_gizli"))


def _pe(s):
    return urllib.parse.quote(str(s), safe="~")


def _imza(method, url, params):
    base = "&".join([method.upper(), _pe(url), _pe("&".join("%s=%s" % (_pe(k), _pe(v)) for k, v in sorted(params.items())))])
    key = "%s&%s" % (_pe(X["gizli"]), _pe(X["jeton_gizli"]))
    return base64.b64encode(hmac.new(key.encode(), base.encode(), hashlib.sha1).digest()).decode()


def _yetki(method, url):
    o = {"oauth_consumer_key": X["anahtar"], "oauth_nonce": uuid.uuid4().hex, "oauth_signature_method": "HMAC-SHA1",
         "oauth_timestamp": str(int(time.time())), "oauth_token": X["jeton"], "oauth_version": "1.0"}
    o["oauth_signature"] = _imza(method, url, o)
    return "OAuth " + ", ".join('%s="%s"' % (_pe(k), _pe(v)) for k, v in sorted(o.items()))


def _kayit_oku():
    try:
        return json.load(open(KAYIT, encoding="utf-8"))
    except Exception:
        return []


def _kayit_yaz(liste):
    os.makedirs(os.path.dirname(KAYIT), exist_ok=True)
    json.dump(liste, open(KAYIT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def sinama():
    """Anahtarlar geçerli mi? GET /2/users/me — gönderim yapmaz."""
    if not hazir():
        return {"ok": False, "neden": "anahtarlar eksik"}
    url = "https://api.x.com/2/users/me"
    r = urllib.request.Request(url, headers={"Authorization": _yetki("GET", url)})
    try:
        with urllib.request.urlopen(r, timeout=20) as c:
            d = json.load(c)
            return {"ok": True, "kullanici": d.get("data", {}).get("username")}
    except urllib.error.HTTPError as e:
        return {"ok": False, "neden": "%s %s" % (e.code, e.read()[:200].decode("utf-8", "ignore"))}
    except Exception as ex:
        return {"ok": False, "neden": str(ex)}


def paylas(metin, baglanti=None, zorla=False):
    """Tek gönderi. Aynı bağlantı daha önce paylaşıldıysa (zorla=False) atlar."""
    if not hazir():
        return {"ok": False, "neden": "anahtarlar eksik — Panel → Ayarlar → X"}
    kayit = _kayit_oku()
    if baglanti and not zorla and any(k.get("baglanti") == baglanti for k in kayit):
        return {"ok": False, "neden": "zaten paylaşıldı", "baglanti": baglanti}
    govde = metin.strip()
    if baglanti:
        govde = (govde[:275 - len(baglanti)].rstrip() + "\n" + baglanti) if len(govde) + len(baglanti) + 1 > 280 else govde + "\n" + baglanti
    url = "https://api.x.com/2/tweets"
    veri = json.dumps({"text": govde}).encode("utf-8")
    r = urllib.request.Request(url, data=veri, method="POST",
                               headers={"Authorization": _yetki("POST", url), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=25) as c:
            d = json.load(c)
            kimlik = d.get("data", {}).get("id")
            kayit.append({"t": time.strftime("%Y-%m-%d %H:%M"), "id": kimlik, "metin": govde, "baglanti": baglanti})
            _kayit_yaz(kayit)
            return {"ok": True, "id": kimlik, "url": "https://x.com/i/status/%s" % kimlik}
    except urllib.error.HTTPError as e:
        return {"ok": False, "neden": "%s %s" % (e.code, e.read()[:300].decode("utf-8", "ignore"))}
    except Exception as ex:
        return {"ok": False, "neden": str(ex)}


def gecmis(n=20):
    return _kayit_oku()[-n:]
