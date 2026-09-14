# -*- coding: utf-8 -*-
"""Google Places API (New) ile işletme arama. Anahtar yoksa boş döner."""
from .agir import json_getir
from .. import ayarlar

UC = "https://places.googleapis.com/v1/places:searchText"
ALANLAR = ("places.id,places.displayName,places.formattedAddress,places.internationalPhoneNumber,"
           "places.websiteUri,places.rating,places.userRatingCount,places.location,"
           "places.photos,places.addressComponents,places.primaryTypeDisplayName")

def ara(sorgu, sehir, sayfa_basi=20, azami=60):
    if not ayarlar.GOOGLE_ANAHTAR:
        return []
    sonuc, jeton = [], None
    while len(sonuc) < azami:
        gövde = {"textQuery": "%s %s" % (sorgu, sehir), "languageCode": "tr", "regionCode": "TR",
                 "maxResultCount": min(sayfa_basi, azami - len(sonuc))}
        if jeton: gövde["pageToken"] = jeton
        y = json_getir(UC, gövde, {
            "X-Goog-Api-Key": ayarlar.GOOGLE_ANAHTAR,
            "X-Goog-FieldMask": ALANLAR + ",nextPageToken"})
        if not y or "places" not in y: break
        for p in y["places"]:
            ilce = ""
            for bilesen in p.get("addressComponents", []):
                if "administrative_area_level_2" in bilesen.get("types", []):
                    ilce = bilesen.get("longText", "")
            sonuc.append({
                "kaynak": "google", "kaynak_id": "g:" + p.get("id", ""),
                "ad": (p.get("displayName") or {}).get("text", ""),
                "adres": p.get("formattedAddress", ""),
                "telefon": p.get("internationalPhoneNumber"),
                "site": p.get("websiteUri"),
                "puan": p.get("rating"),
                "yorum_sayisi": p.get("userRatingCount") or 0,
                "fotograf_sayisi": len(p.get("photos") or []),
                "enlem": (p.get("location") or {}).get("latitude"),
                "boylam": (p.get("location") or {}).get("longitude"),
                "ilce": ilce,
            })
        jeton = y.get("nextPageToken")
        if not jeton: break
    return sonuc
