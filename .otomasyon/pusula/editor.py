# -*- coding: utf-8 -*-
"""
TrendSaphiens editörlük katmanı (12.10.2026).

Neden: AdSense yayıncı politikası "insan incelemesinden geçmemiş otomatik içerik"
üzerinde reklamı yasaklıyor; Google da gerçek bir kişinin adını okumadığı yazıya
koymayı "aldatma" sayıyor. Bu yüzden:

  · KESIM tarihinden sonra üretilen her yazı TASLAK olarak doğar: /taslak/<slug>
    adresinde noindex önizleme, reklamsız, site haritası ve akışlar dışında.
  · Editör /editor panelinden okuyup "Yayınla" dediğinde onay Cloudflare KV'ye yazılır
    (functions/api/onay.js). Actions turu başında onay_cek.py onayları veri/onay.json'a
    indirir; yazı o turda editörün imzasıyla yayına girer.
  · KESIM'den önce yayımlanmış yazılar yerinde kalır ama "inceleme bekliyor" sayılır;
    editör onayladıkça imzası eklenir. İmza yalnız ONAYLANAN yazıda görünür.
"""
import datetime, html, json, os

from .ayarlar import KOK_DIZIN

KESIM = "2026-10-12"
ONAY_DOSYA = os.path.join(KOK_DIZIN, "veri", "onay.json")

EDITOR = {
    "ad": "Pusat Ceylan",
    "slug": "pusat-ceylan",
    "unvan": "TrendSaphiens Editörü",
    "kisa": "Dizi-film, müzik, spor ve gündem yazılarını okur, kaynaklarını kontrol eder ve yayına alır.",
    "bio": ("Pusat Ceylan, TrendSaphiens'in editörüdür. Yayına çıkan her yazıyı okur; isim, tarih ve "
            "rakamları kaynağına karşı kontrol eder, başlığın yazının söylediğinden fazlasını vaat "
            "etmediğinden emin olur. Liste, test ve anketlerin sorularını ve sonuç metinlerini de yayından "
            "önce o gözden geçirir. Bir yazıda hata görürseniz iletişim sayfasındaki adrese yazmanız "
            "yeterli; düzeltme yazının içinde tarihiyle belirtilir."),
}


def _e(x):
    return html.escape(str(x or ""), quote=True)


def onaylar():
    try:
        d = json.load(open(ONAY_DOSYA, encoding="utf-8"))
        return d.get("onay", d) if isinstance(d, dict) else {}
    except Exception:
        return {}


def durum(slug, tarih):
    """'onayli' · 'taslak' (KESIM sonrası, onaysız) · 'inceleme' (KESIM öncesi, onaysız)."""
    o = onaylar()
    if slug in o:
        return "onayli"
    return "taslak" if str(tarih or "")[:10] >= KESIM else "inceleme"


def onay_tarihi(slug):
    return (onaylar().get(slug) or {}).get("t", "")


def yazar_url(on=""):
    return "%syazar/%s" % (on, EDITOR["slug"])


def kisi_sema(mutlak_kok="https://lunayapim.com/trend/"):
    return {"@type": "Person", "name": EDITOR["ad"], "jobTitle": EDITOR["unvan"],
            "url": mutlak_kok + "yazar/" + EDITOR["slug"]}


def imza_html(slug, tr=""):
    """Yazının başındaki imza satırı. Onaysız yazıda yayın adı görünür, kişi adı görünmez."""
    if durum(slug, "") == "onayli" or slug in onaylar():
        t = onay_tarihi(slug)
        ek = (' · <span>Editör onayı %s</span>' % _e(_tr(t))) if t else ""
        return ('<div class="ts-imza"><a class="ts-imza-ad" href="%s"><span class="ts-imza-harf" aria-hidden="true">PC</span>'
                '<span><b>%s</b><small>%s</small></span></a>%s</div>'
                % (yazar_url(tr), _e(EDITOR["ad"]), _e(EDITOR["unvan"]), ek))
    return '<div class="ts-imza"><span class="ts-imza-ad"><span class="ts-imza-harf" aria-hidden="true">TS</span><span><b>TrendSaphiens</b><small>Yayın masası</small></span></span></div>'


def editor_kutu_html(slug, tr=""):
    """Yazının sonundaki editör kutusu — yalnız onaylı yazıda."""
    if slug not in onaylar():
        return ""
    return ('<aside class="ts-editor-kutu"><span class="ts-imza-harf" aria-hidden="true">PC</span><div>'
            '<b>%s</b><small>%s</small><p>%s</p><a href="%s">Tüm yazıları ve yayın ilkeleri &rarr;</a></div></aside>'
            % (_e(EDITOR["ad"]), _e(EDITOR["unvan"]), _e(EDITOR["kisa"]), yazar_url(tr)))


AY = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


def _tr(iso):
    try:
        d = datetime.date.fromisoformat(str(iso)[:10])
        return "%d %s %d" % (d.day, AY[d.month - 1], d.year)
    except Exception:
        return str(iso or "")
