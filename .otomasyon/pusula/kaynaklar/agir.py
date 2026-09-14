# -*- coding: utf-8 -*-
"""Ortak HTTP yardımcıları — sadece standart kütüphane."""
import json, urllib.request, urllib.parse, urllib.error, ssl, gzip, io, time
from ..ayarlar import KULLANICI_AJANI, ISTEK_ZAMAN_ASIMI

_ctx = ssl.create_default_context()

def getir(url, veri=None, basliklar=None, zaman_asimi=None, dogrula_ssl=True):
    """(durum_kodu, govde_metni, son_url) döner. Hata durumunda (0, '', url)."""
    bas = {"User-Agent": KULLANICI_AJANI, "Accept-Encoding": "gzip"}
    if basliklar: bas.update(basliklar)
    gövde = None
    if veri is not None:
        gövde = json.dumps(veri).encode("utf-8")
        bas.setdefault("Content-Type", "application/json")
    istek = urllib.request.Request(url, data=gövde, headers=bas)
    ctx = _ctx if dogrula_ssl else ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(istek, timeout=zaman_asimi or ISTEK_ZAMAN_ASIMI, context=ctx) as c:
            ham = c.read()
            if c.headers.get("Content-Encoding") == "gzip":
                ham = gzip.decompress(ham)
            metin = ham.decode(c.headers.get_content_charset() or "utf-8", "replace")
            return c.status, metin, c.geturl()
    except urllib.error.HTTPError as ex:
        try: metin = ex.read().decode("utf-8", "replace")
        except Exception: metin = ""
        return ex.code, metin, url
    except Exception:
        return 0, "", url

def json_getir(url, veri=None, basliklar=None):
    k, m, _ = getir(url, veri, basliklar)
    if k != 200 or not m: return None
    try: return json.loads(m)
    except Exception: return None
