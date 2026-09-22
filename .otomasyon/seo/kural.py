# -*- coding: utf-8 -*-
"""
ÖZGÜNLÜK VE SEO KURALLARI — iki sitenin tek kural dosyası.

22.09.2026'da yazıldı. O güne kadar eşikler üç ayrı yere dağılmıştı:
denetci.py'nin E sözlüğü, trend.py'nin başlık/meta kırpmaları, benzerlik.py'nin
renk sınırları. Dağınık eşiğin sorunu şu: biri değişince ötekiler eskiyor ve
"kural neydi" sorusunun tek cevabı kalmıyor.

İKİ SİTE, İKİ İŞ — bu yüzden iki profil:

  luna  (lunayapim.com)      Hizmet sitesi. Az sayıda, derin sayfa. Okur zaten
                             ne istediğini biliyor; sayfa onu işe çevirmeli.
                             Şehir sayfaları kardeş sayfalarla benzer olur —
                             doğası bu — ama eşiği aşmamalı.

  trend (trendsaphiens.com)  Günlük yayın. Çok sayıda, taze sayfa. Asıl risk
                             tersi: her gün aynı şablonun tekrar basılması.
                             Gün sayfalarında şablon payı yüksekse arama motoru
                             sayfayı "soft 404" sayar. Bu yüzden benzerlik
                             eşiği burada DAHA SIKI.

Eşikler nereden geldi (22.09.2026 ölçümü, 675 sayfa):
  · hizmetler grubu      ort. %2,5   en yüksek %24,6   → sağlıklı
  · sehir:* grupları     ort. %13-31 en yüksek %38,9   → sağlıklı
  · trend/aranan         ort. %49,1  en yüksek %59,3   → şablon ağır
  · trend/piyasa         ort. %39,6  en yüksek %75,8   → kopya sayılır
  · özgünlük ortalaması  80,7 / 100  en düşük 64,5

Yani kesilmesi gereken şey şehir sayfaları değil, gün sayfalarının şablonuydu.
Eşikler bu ölçümün biraz üstüne kuruldu: bugünü geçiren ama bozulmayı yakalayan
bir çizgi.
"""

# --------------------------------------------------------------------- profiller
PROFIL = {
    "luna": {
        "ad": "Luna Yapım — hizmet sitesi",
        "alan": "lunayapim.com",
        # Başlık: arama sonucunda kesilmeden görünen bütçe. " | Luna Yapım" eki
        # 13 karakter; gövde 47'yi aşarsa sonuç sayfasında üç nokta çıkar.
        "baslik_min": 30, "baslik_max": 70, "baslik_govde_max": 47,
        "aciklama_min": 110, "aciklama_max": 165,
        "kelime_min": 400,          # hizmet sayfası derin olmalı
        "ic_bag_min": 5,
        "h2_min": 2,
        # Kardeş sayfalar arası 5 kelimelik parça (shingle) benzerliği
        "benzerlik_uyari": 0.45,
        "benzerlik_hata": 0.65,
        "ozgunluk_min": 55,         # seo/ozgunluk.py puanı (0-100)
        "sema_zorunlu": (),         # hizmet sayfalarında şema serbest
    },
    "trend": {
        "ad": "TrendSaphiens — günlük yayın",
        "alan": "trendsaphiens.com",
        # " | TrendSaphiens" eki 16 karakter. Gövde 52'yi aşarsa kesilir —
        # 22.09'da on başlığın dokuzu bu yüzden ortasından kesilmişti.
        "baslik_min": 25, "baslik_max": 70, "baslik_govde_max": 52,
        "aciklama_min": 110, "aciklama_max": 158,
        "kelime_min": 350,          # haber daha kısa olabilir
        "ic_bag_min": 3,
        "h2_min": 2,
        "benzerlik_uyari": 0.40,    # gün sayfaları için daha sıkı
        "benzerlik_hata": 0.60,
        "ozgunluk_min": 55,
        "sema_zorunlu": ("NewsArticle", "Article", "WebPage", "CollectionPage",
                         "ItemList", "AboutPage", "ContactPage", "WebApplication"),
    },
}

# Yazı sayfalarında (kendi kalemimizden çıkan haber/rehber) ek şartlar
YAZI_KURALI = {
    "kaynak_min": 2,        # en az iki bağımsız yayıncı
    "atif_zorunlu": True,   # şemada citation boş kalmayacak
    "alinti_azami": 1,      # doğrudan alıntı en çok bir cümle
    "intihal_kapsama": 0.18,  # kaynakla örtüşen en uzun parça oranı üst sınırı
}

# Gün sayfası arşivi (piyasa/aranan gibi her gün yeniden basılan sayfalar)
ARSIV_KURALI = {
    "dizine_giren": "yalnız en yeni gün",
    "eskiler": "noindex, follow — okur için durur, site haritasından çıkar",
    "gerekce": ("Gün sayfasının özgün yanı o günün rakamıdır; tablolar ve "
                "açıklamalar zorunlu olarak tekrar eder. Ölçüm (22.09.2026): iki "
                "ardışık piyasa günü arasında %76 parça benzerliği. Uzun blokları "
                "bölüm sayfasına taşımak %73'e indirdi, tablolar kaldığı sürece "
                "daha aşağı inmedi. Metni zorlamak yerine dürüst sinyal: bugünün "
                "sayfası dizine girer, eski günler girmez."),
}

# Hiçbir sayfada geçmeyecek kalıplar (tık tuzağı)
YASAK_KALIP = ("şok", "işte o", "tam liste", "bomba", "olay oldu",
               "inanılmaz", "asla tahmin edemezsiniz")


def profil(yol):
    """Depo içindeki bir yol → hangi profile tabi."""
    y = (yol or "").replace("\\", "/").lstrip("./")
    return "trend" if y == "trend" or y.startswith("trend/") else "luna"


def kural(yol):
    return PROFIL[profil(yol)]


def grup(yol):
    """Benzerlik karşılaştırmasında hangi kardeş kümesine girer.

    Kardeşi olmayan sayfa tek başına ölçülmez — benzerlik ancak aynı kalıptan
    basılan sayfalar arasında anlamlıdır.
    """
    y = (yol or "").replace("\\", "/").lstrip("./")
    p = y.split("/")
    if p[0] == "sehir" and len(p) == 2:
        ad = p[1][:-5] if p[1].endswith(".html") else p[1]
        parca = ad.split("-", 1)
        return "sehir:" + (parca[1] if len(parca) > 1 else "genel")
    if p[0] == "trend" and len(p) >= 3:
        return "trend/" + p[1]
    return p[0] if len(p) > 1 else "kok"


def ozet():
    """İnsan okusun diye tek ekranlık kural özeti."""
    satir = []
    for ad, k in PROFIL.items():
        satir.append("%s (%s)" % (k["ad"], k["alan"]))
        satir.append("  başlık gövdesi ≤ %d · açıklama %d-%d · en az %d kelime"
                     % (k["baslik_govde_max"], k["aciklama_min"], k["aciklama_max"], k["kelime_min"]))
        satir.append("  kardeş benzerliği: uyarı %%%d · hata %%%d · özgünlük en az %d"
                     % (k["benzerlik_uyari"] * 100, k["benzerlik_hata"] * 100, k["ozgunluk_min"]))
        satir.append("")
    satir.append("Gün sayfası arşivi: %s dizine girer; eskiler %s."
                 % (ARSIV_KURALI["dizine_giren"], ARSIV_KURALI["eskiler"]))
    satir.append("")
    satir.append("Yazı sayfaları: en az %d bağımsız kaynak · şemada citation dolu · "
                 "doğrudan alıntı en çok %d cümle · intihal kapsaması ≤ %%%d"
                 % (YAZI_KURALI["kaynak_min"], YAZI_KURALI["alinti_azami"],
                    YAZI_KURALI["intihal_kapsama"] * 100))
    return "\n".join(satir)


if __name__ == "__main__":
    print(ozet())
