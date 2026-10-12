# -*- coding: utf-8 -*-
"""Editör onaylarını canlı siteden indirir → veri/onay.json (12.10.2026).

Actions turunun başında çalışır. Ağ yoksa ya da cevap bozuksa mevcut dosyaya
DOKUNMAZ (onaylı yazı yanlışlıkla taslağa düşmesin)."""
import json, os, urllib.request

from .editor import ONAY_DOSYA

ADRES = os.environ.get("TS_ONAY_ADRES", "https://trendsaphiens.com/api/onay")


def cek():
    try:
        req = urllib.request.Request(ADRES, headers={"User-Agent": "TrendSaphiens-Otomasyon/1.0"})
        d = json.loads(urllib.request.urlopen(req, timeout=20).read().decode("utf-8"))
        onay = d.get("onay")
        if not isinstance(onay, dict):
            raise ValueError("onay alanı yok")
    except Exception as ex:
        print("onay çekilemedi, mevcut liste korunuyor:", ex)
        return None
    os.makedirs(os.path.dirname(ONAY_DOSYA), exist_ok=True)
    json.dump({"onay": onay, "cekildi": __import__("datetime").datetime.now().isoformat(timespec="minutes")},
              open(ONAY_DOSYA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("onaylı yazı: %d" % len(onay))
    return onay


if __name__ == "__main__":
    cek()
