# -*- coding: utf-8 -*-
"""OpenStreetMap Overpass — ücretsiz, anahtarsız yedek kaynak."""
import time, urllib.parse
import json

UC = "https://overpass-api.de/api/interpreter"

def ara(etiketler, sehir, azami=200):
    """etiketler: ['"office"="estate_agent"', ...]"""
    parcalar = []
    for et in etiketler:
        for tur in ("node", "way"):
            parcalar.append('%s[%s](area.a);' % (tur, et))
    sorgu = """[out:json][timeout:60];
area["name"="%s"]["boundary"="administrative"]->.a;
(%s);
out center %d;""" % (sehir, "".join(parcalar), azami)
    import urllib.request
    istek = urllib.request.Request(UC, data=urllib.parse.urlencode({"data": sorgu}).encode(),
                                   headers={"User-Agent":"LunaPusula/1.0"})
    try:
        with urllib.request.urlopen(istek, timeout=90) as c:
            y = json.loads(c.read().decode("utf-8","replace"))
    except Exception:
        return []
    sonuc = []
    for el in y.get("elements", []):
        t = el.get("tags", {})
        ad = t.get("name")
        if not ad: continue
        sonuc.append({
            "kaynak":"osm", "kaynak_id":"o:%s/%s" % (el.get("type"), el.get("id")),
            "ad": ad,
            "adres": " ".join(filter(None,[t.get("addr:street"), t.get("addr:housenumber"),
                                           t.get("addr:district"), t.get("addr:city")])),
            "telefon": t.get("phone") or t.get("contact:phone"),
            "site": t.get("website") or t.get("contact:website"),
            "puan": None, "yorum_sayisi": 0, "fotograf_sayisi": 0,
            "enlem": el.get("lat") or (el.get("center") or {}).get("lat"),
            "boylam": el.get("lon") or (el.get("center") or {}).get("lon"),
            "ilce": t.get("addr:district") or "",
        })
    return sonuc
