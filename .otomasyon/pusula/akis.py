# -*- coding: utf-8 -*-
"""Panelden çağrılan iş akışları — cli komutlarını sarar, terminal gerektirmez."""
import types
from . import cli
from .ayarlar import SEKTORLER


def _arg(**k):
    a = types.SimpleNamespace(sehir=None, sektor=None, adet=0, hizli=True,
                              sadece_sicak=False, ortalama_is=None, sadece_yeni=False)
    for x, v in k.items():
        setattr(a, x, v)
    return a


ADIMLAR = [
    ("tara",         "Aday bulunuyor",              cli.komut_tara),
    ("denetle",      "Eksikler tespit ediliyor",    cli.komut_denetle),
    ("zenginlestir", "İletişim ve yetkili araştırması", cli.komut_zenginlestir),
    ("hesapla", "Kazanç tahmini",            cli.komut_hesapla),
    ("demo",    "Demo sunumları üretiliyor", cli.komut_demo),
    ("rapor",   "Rapor ve pano",             cli.komut_rapor),
]


def akis(gorev, sehir, sektor=None, adet=0, hizli=True, sadece_sicak=False,
         ortalama_is=None, adimlar=None):
    secili = [a for a in ADIMLAR if not adimlar or a[0] in adimlar]
    gorev["toplam_adim"] = len(secili)
    # sadece_yeni: daha önce araştırılmış adayı tekrar gezmez — akış yarıda kalırsa
    # kaldığı yerden devam eder, tekrar çalıştırmak baştan taramaz.
    a = _arg(sehir=sehir, sektor=sektor or None, adet=adet, hizli=hizli,
             sadece_sicak=sadece_sicak, ortalama_is=ortalama_is, sadece_yeni=True)
    print("▸ %s%s — %d adım" % (sehir, (" / " + SEKTORLER[sektor]["ad"]) if sektor else "", len(secili)))
    for i, (anahtar, baslik, fn) in enumerate(secili, 1):
        gorev["adim_no"] = i
        gorev["adim"] = baslik
        print("\n── %d/%d  %s" % (i, len(secili), baslik))
        fn(a)
    gorev["adim"] = "tamamlandı"
    print("\n✓ Akış tamamlandı.")
