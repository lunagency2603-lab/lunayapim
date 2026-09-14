# -*- coding: utf-8 -*-
"""
Eksikler kapatılırsa ne değişir?
MODEL tamamen varsayıma dayalıdır; her çıktı "tahmin" olarak işaretlenir.
Amaç kesin rakam vermek değil, büyüklük mertebesini ve önceliği göstermek.
"""
from .ayarlar import MODEL

def _taban_goruntulenme(aday):
    y = aday["yorum_sayisi"] or 0
    g = MODEL["goruntulenme_taban"] + y * MODEL["goruntulenme_yorum_carpani"]
    return int(min(g, MODEL["goruntulenme_tavan"]))

def hesapla(aday, eksikler, kapatilacaklar=None, ortalama_is=None):
    """
    kapatilacaklar: None ise tüm eksikler kapatılıyor varsayılır.
    döner: sözlük (rapor ve demo bunu kullanır)
    """
    kapat = list(kapatilacaklar if kapatilacaklar is not None else eksikler)
    mevcut_g = _taban_goruntulenme(aday)

    carpan = 1.0
    katkilar = []
    for k in kapat:
        c = MODEL["etki"].get(k, 1.0)
        if c <= 1.0: continue
        carpan *= c
        katkilar.append((k, c))
    carpan = min(carpan, MODEL["carpan_tavani"])
    hedef_g = int(round(mevcut_g * carpan))

    d_mev = MODEL["donusum_mevcut"]
    d_hed = MODEL["donusum_iyilesmis"] if kapat else d_mev
    mevcut_i = round(mevcut_g * d_mev, 1)
    hedef_i  = round(hedef_g * d_hed, 1)

    kap = MODEL["kapanis_orani"]
    mevcut_is = round(mevcut_i * kap, 1)
    hedef_is  = round(hedef_i * kap, 1)

    if ortalama_is is None:
        ortalama_is = MODEL["ortalama_is"].get(aday["sektor"], 12000)
    ek_gelir = round((hedef_is - mevcut_is) * ortalama_is)

    # tek tek katkı sıralaması — "önce hangisini yapalım" sorusu için
    tekil = []
    for k in kapat:
        c = MODEL["etki"].get(k, 1.0)
        if c <= 1.0: continue
        g2 = int(round(mevcut_g * c))
        i2 = round(g2 * d_hed, 1)
        tekil.append({"eksik": k, "carpan": round(c, 2),
                      "tek_basina_goruntulenme": g2,
                      "tek_basina_ek_iletisim": round(i2 - mevcut_i, 1)})
    tekil.sort(key=lambda x: -x["tek_basina_ek_iletisim"])

    return {
        "mevcut_goruntulenme": mevcut_g,
        "hedef_goruntulenme": hedef_g,
        "goruntulenme_artis_yuzde": int(round((hedef_g / mevcut_g - 1) * 100)) if mevcut_g else 0,
        "mevcut_iletisim": mevcut_i,
        "hedef_iletisim": hedef_i,
        "mevcut_is": mevcut_is,
        "hedef_is": hedef_is,
        "ek_gelir": ek_gelir,
        "ortalama_is": ortalama_is,
        "toplam_carpan": round(carpan, 2),
        "kapatilan": kapat,
        "tekil_katki": tekil,
        "varsayimlar": {
            "donusum_mevcut": d_mev, "donusum_iyilesmis": d_hed,
            "kapanis_orani": kap, "carpan_tavani": MODEL["carpan_tavani"],
            "not": "Rakamlar modelleme sonucudur, garanti değildir. Ayarlar dosyasından değiştirilebilir."
        }
    }
