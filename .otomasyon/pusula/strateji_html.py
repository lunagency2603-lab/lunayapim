# -*- coding: utf-8 -*-
"""strateji.py'nin ürettiği sözlüğü müşteriye gidecek belgeye çevirir."""
import html


def _e(x):
    return html.escape(str(x if x is not None else ""), quote=True)


CSS = """
:root{--ink:#0A0A0C;--ink2:#131317;--ink3:#1b1b21;--bone:#EFEDE8;--kirmizi:#E8452C;
--yesil:#3BA55C;--sari:#E0A32E;--gri:#8C8A84;--cizgi:rgba(239,237,232,.13)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--ink);color:var(--bone);font-family:"Manrope",system-ui,-apple-system,sans-serif;
line-height:1.62;-webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin:0 auto;padding:0 26px}
h1,h2,h3{font-family:"Bricolage Grotesque","Manrope",sans-serif;font-weight:800;
letter-spacing:-.03em;line-height:1.06}
h1{font-size:clamp(30px,5vw,50px)}
h2{font-size:clamp(23px,3.2vw,33px);margin-bottom:8px}
h3{font-size:19px;margin-bottom:6px}
.etk{font-family:"Space Mono",ui-monospace,monospace;font-size:10.5px;letter-spacing:.2em;
text-transform:uppercase;color:var(--kirmizi)}
header{border-bottom:1px solid var(--cizgi);padding:18px 0}
.mrk{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.mrk b{font-family:"Bricolage Grotesque",sans-serif;font-size:17px}
.kapak{padding:64px 0 48px;border-bottom:1px solid var(--cizgi);
background:linear-gradient(180deg,var(--ink2),var(--ink))}
.kapak p{color:rgba(239,237,232,.72);max-width:70ch;margin-top:14px;font-size:16.5px}
section{padding:52px 0;border-bottom:1px solid var(--cizgi)}
.alt{color:var(--gri);max-width:74ch;margin-bottom:20px;font-size:15px}
.no{font-family:"Space Mono",monospace;font-size:11px;color:var(--kirmizi);
letter-spacing:.16em;display:block;margin-bottom:7px}
table{width:100%;border-collapse:collapse;margin-top:14px;font-size:14.5px}
th,td{text-align:left;padding:11px 13px;border-bottom:1px solid var(--cizgi);vertical-align:top}
th{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:.14em;
text-transform:uppercase;color:var(--kirmizi);font-weight:400}
td.sag,th.sag{text-align:right}
.karne{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:13px;margin-top:18px}
.kk{border:1px solid var(--cizgi);border-radius:5px;padding:17px}
.kk.zayif{border-color:var(--kirmizi);box-shadow:0 0 0 1px rgba(232,69,44,.2)}
.kk .etk{display:block;line-height:1.5;min-height:2.6em;color:var(--gri)}
.kk b{font-family:"Bricolage Grotesque",sans-serif;font-size:36px;line-height:1;
display:block;margin:7px 0 9px;letter-spacing:-.04em}
.cub{height:4px;background:rgba(239,237,232,.1);border-radius:99px;overflow:hidden}
.cub i{display:block;height:100%;border-radius:99px}
.kutu{border:1px solid var(--cizgi);border-left:2px solid var(--kirmizi);border-radius:4px;
padding:19px 22px;margin-top:16px;background:rgba(232,69,44,.045)}
.kart{border:1px solid var(--cizgi);border-radius:5px;padding:20px 22px;margin-top:14px}
.kart h3{margin-bottom:5px}
.kart .rol{font-family:"Space Mono",monospace;font-size:9.5px;letter-spacing:.16em;
text-transform:uppercase;color:var(--kirmizi);display:block;margin-bottom:8px}
.kart p{font-size:14.5px;color:rgba(239,237,232,.82)}
.kart small{display:block;color:var(--gri);font-size:12.5px;margin-top:8px;
border-top:1px solid var(--cizgi);padding-top:8px}
.izgara{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;margin-top:16px}
.pay{display:flex;align-items:center;gap:11px;margin-top:9px}
.pay .bar{flex:1;height:7px;background:rgba(239,237,232,.09);border-radius:99px;overflow:hidden}
.pay .bar i{display:block;height:100%;background:var(--kirmizi);border-radius:99px}
.pay b{font-family:"Space Mono",monospace;font-size:12px;min-width:38px;text-align:right}
.donem{border-left:2px solid var(--cizgi);padding-left:22px;margin-top:22px;position:relative}
.donem::before{content:"";position:absolute;left:-6px;top:6px;width:10px;height:10px;
border-radius:50%;background:var(--kirmizi)}
.donem h3{font-size:20px}
.donem .amac{color:var(--gri);font-size:14px;margin:5px 0 12px}
.donem ol{margin-left:18px}
.donem li{font-size:14.5px;margin-bottom:7px;line-height:1.6}
.risk{border:1px solid var(--cizgi);border-radius:5px;padding:18px 20px;margin-top:12px}
.risk b{display:block;font-size:15.5px;margin-bottom:5px}
.risk .ne{color:var(--gri);font-size:14px}
.risk .onlem{margin-top:9px;padding-top:9px;border-top:1px solid var(--cizgi);font-size:14px}
.risk .onlem span{color:var(--yesil);font-family:"Space Mono",monospace;font-size:9.5px;
letter-spacing:.14em;text-transform:uppercase;display:block;margin-bottom:4px}
.uyari{border:1px solid var(--sari);border-left-width:3px;border-radius:4px;padding:15px 18px;
margin-top:18px;font-size:14px;color:rgba(239,237,232,.86);background:rgba(224,163,46,.05)}
.rozet{display:inline-block;font-family:"Space Mono",monospace;font-size:9.5px;
letter-spacing:.14em;text-transform:uppercase;border:1px solid var(--cizgi);border-radius:99px;
padding:3px 9px;color:var(--gri);margin-left:7px}
.rozet.yok{border-color:var(--kirmizi);color:var(--kirmizi)}
.rozet.var{border-color:var(--yesil);color:var(--yesil)}
.cta{background:var(--kirmizi);color:#fff;padding:52px 0;text-align:left}
.cta h2{color:#fff}
.cta a{display:inline-block;margin:16px 10px 0 0;padding:13px 26px;border-radius:2px;
background:#fff;color:var(--kirmizi);text-decoration:none;font-weight:700;font-size:15px}
.cta a.c{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.6)}
footer{padding:24px 0;color:var(--gri);font-size:12.5px}
@media print{body{background:#fff;color:#111}section{break-inside:avoid}}
"""


def sayfa(s, firma_bilgi):
    """Strateji sözlüğünü tek dosyalık HTML belgeye çevirir."""
    p = []
    a = p.append
    renk = lambda v: "#E8452C" if v < 45 else ("#E0A32E" if v < 75 else "#3BA55C")

    a('<!DOCTYPE html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">')
    a('<meta name="viewport" content="width=device-width,initial-scale=1">')
    a('<meta name="robots" content="noindex,nofollow">')
    a('<title>%s · Pazarlama Stratejisi · Luna Yapım</title>' % _e(s["firma"]))
    a('<link rel="preconnect" href="https://fonts.googleapis.com">')
    a('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    a('<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;'
      '12..96,800&family=Manrope:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" '
      'rel="stylesheet">')
    a("<style>%s</style>\n</head>\n<body>" % CSS)

    a('<header><div class="wrap mrk"><b>LUNA YAPIM</b>'
      '<span class="etk">Pazarlama Stratejisi · %s</span></div></header>' % _e(s["zaman"]))

    a('<div class="kapak"><div class="wrap">'
      '<p class="etk">%s · %s</p>'
      '<h1>%s için 90 günlük pazarlama stratejisi</h1>'
      '<p>Bu belge şablon değil. Aşağıdaki her başlık, sizin sitenizde ve harita profilinizde '
      'yaptığımız denetimden çıkan bulgulara göre yazıldı — hangi başlıkta zayıf olduğunuz, '
      'hangi kanalın sizde eksik olduğu ve paranın önce nereye gitmesi gerektiği buna göre '
      'belirlendi. Rakamların tamamı <strong>varsayım</strong> olarak işaretli; sizin gerçek '
      'verinizle güncellendiğinde çok daha isabetli oluyor.</p>'
      '</div></div>' % (_e(s["sektor_ad"]), _e(s["sehir"]), _e(s["firma"])))

    # 1 — bugün nerede
    a('<section><div class="wrap"><span class="no">01</span><h2>Bugün nerede duruyoruz</h2>'
      '<p class="alt">Tek bir puan yerine beş ayrı not. Strateji en düşük nottan başlıyor — '
      'çünkü en çok para orada kaybediliyor.</p><div class="karne">')
    for g, v in s["karne"].items():
        a('<div class="kk%s"><span class="etk">%s</span><b style="color:%s">%d</b>'
          '<div class="cub"><i style="width:%d%%;background:%s"></i></div>'
          '<small style="color:var(--gri);font-size:12px;display:block;margin-top:8px">%s</small></div>'
          % (" zayif" if g == s["zayif"]["anahtar"] else "", _e(v["baslik"]),
             renk(v["skor"]), v["skor"], v["skor"], renk(v["skor"]),
             _e(v.get("not") or ("%d başlık eksik" % len(v["kodlar"]) if v["kodlar"] else "eksik yok"))))
    a('</div><div class="kutu"><strong>Buradan başlıyoruz:</strong> %s. '
      'İlk 30 günün tamamı bu başlığa ayrıldı.</div></div></section>'
      % _e(s["zayif"]["baslik"]))

    # 2 — kime satıyoruz
    a('<section><div class="wrap"><span class="no">02</span><h2>Kime satıyoruz</h2>'
      '<p class="alt">Üç katman var ve aynı içerik üçüne birden çalışmıyor. '
      'Sıralama önemli: önce şimdi alacak olana, sonra araştırana.</p><div class="izgara">')
    for ad, kim, tetik, nasil in s["katman"]:
        a('<div class="kart"><span class="rol">%s</span><h3>%s</h3><p>%s</p>'
          '<small><b>Satın alma tetikleyicisi:</b> %s<br><b>Ne üretiyoruz:</b> %s</small></div>'
          % (_e(ad), _e(kim.split(",")[0]), _e(kim), _e(tetik), _e(nasil)))
    a('</div></div></section>')

    # 3 — konumlandırma
    a('<section><div class="wrap"><span class="no">03</span><h2>Nerede konumlanıyoruz</h2>'
      '<p class="alt">Rakiplerin hepsinin söylediği şeyi söylersek ayrışamayız. '
      'Bu sektörde ayrışmanın gerçekten mümkün olduğu yer şurası:</p>'
      '<div class="kutu">%s</div>' % _e(s["konumlandirma"]))
    a('<h3 style="margin-top:28px">Bunu nasıl gösteriyoruz</h3><div class=\"tablo-kaydir\"><table>'
      '<tr><th>Genelde böyle yapılır</th><th>Bizde böyle</th><th>Sonuç</th></tr>')
    for f in s["fark"]:
        a("<tr><td style='color:var(--gri)'>%s</td><td>%s</td><td>%s</td></tr>"
          % (_e(f["sıradan"]), _e(f["bizde"]), _e(f["sonuc"])))
    a('</table></div></section>')

    # 4 — kanal
    a('<section><div class="wrap"><span class="no">04</span><h2>Hangi kanal, neden</h2>'
      '<p class="alt">Kanal seçimi moda değil sebep işidir. Aşağıdaki sıralama sizin '
      'sektörünüzde hangi kanalın gerçekten iş getirdiğine göre yapıldı.</p><div class=\"tablo-kaydir\"><table>'
      '<tr><th>Kanal</th><th>Durum</th><th>Neden bu kanal</th></tr>')
    for k in s["kanal"]:
        a('<tr><td><b>%s</b><span class="rozet %s">%s</span></td><td>%s</td><td>%s</td></tr>'
          % (_e(k["platform"]), "var" if k["var"] else "yok",
             "var" if k["var"] else "yok", _e(k["durum"]), _e(k["neden"])))
    a('</table></div>')
    t = s["tempo"]
    a('<h3 style="margin-top:26px">Aylık tempo</h3><p class="alt">%s</p>'
      % _e(" · ".join("%s %s" % (v, SO_FORMAT.get(k, k)) for k, v in t.items() if v)
           + ". Hepsi tek çekim gününde toplanıyor; siz sadece yayınlıyorsunuz."))
    a('</div></section>')

    # 5 — içerik sütunları
    a('<section><div class="wrap"><span class="no">05</span><h2>Ne anlatacağız</h2>'
      '<p class="alt">Dört içerik sütunu. Her birinin tek bir işi var — '
      '"içerik üretelim" değil, "bu içerik şunu çözecek".</p>')
    for ad, ne, is_, pay in s["sutun"]:
        a('<div class="kart"><h3>%s <span class="rozet">%%%d</span></h3>'
          '<p>%s</p><small><b>İşi:</b> %s</small>'
          '<div class="pay"><div class="bar"><i style="width:%d%%"></i></div><b>%%%d</b></div></div>'
          % (_e(ad), pay, _e(ne), _e(is_), pay, pay))
    a('</div></section>')

    # 6 — yol haritası
    a('<section><div class="wrap"><span class="no">06</span><h2>30 / 60 / 90 gün</h2>'
      '<p class="alt">Her şey aynı anda yapılmıyor. Sıra, en çok kaybettiren yerden başlıyor.</p>')
    for y in s["yol"]:
        a('<div class="donem"><h3>%s — %s</h3><p class="amac">%s</p><ol>%s</ol></div>'
          % (_e(y["donem"]), _e(y["baslik"]), _e(y["amac"]),
             "".join("<li>%s</li>" % _e(x) for x in y["adim"])))
    a('</div></section>')

    # 7 — huni
    a('<section><div class="wrap"><span class="no">07</span><h2>Huni matematiği</h2>'
      '<p class="alt">Görüntülenmenin işe dönüşme yolu. Aşağıdaki oranlar '
      '<strong>varsayımdır</strong>, garanti değildir — amaç büyüklük mertebesini göstermek.</p>'
      '<div class=\"tablo-kaydir\"><table><tr><th>Aşama</th><th class="sag">Bugün</th><th class="sag">Hedef</th>'
      '<th>Nasıl ölçülüyor</th></tr>')
    for ad, su, hedef, nasil in s["huni"]:
        a('<tr><td><b>%s</b></td><td class="sag">%s</td>'
          '<td class="sag" style="color:var(--kirmizi)">%s</td><td>%s</td></tr>'
          % (_e(ad), "{:,}".format(su).replace(",", "."),
             "{:,}".format(hedef).replace(",", "."), _e(nasil)))
    a('</table></div><div class="uyari">Varsayımlar: mevcut dönüşüm %%%s, iyileştirilmiş dönüşüm %%%s, '
      'iletişimden işe dönüşüm %%%s. Kendi rakamlarınızı verdiğinizde bu tabloyu '
      'sizin verinizle yeniden çalıştırıyoruz.</div></div></section>'
      % (round(s["varsayim"]["donusum_mevcut"] * 100, 1),
         round(s["varsayim"]["donusum_iyilesmis"] * 100, 1),
         round(s["varsayim"]["kapanis"] * 100, 1)))

    # 8 — bütçe
    a('<section><div class="wrap"><span class="no">08</span><h2>Bütçe nereye gidiyor</h2>'
      '<p class="alt">Toplam bütçenin dağılımı. Oranlar sizin en zayıf başlığınıza göre '
      'ayarlandı — teknik tarafı zayıf olan firmada site kalemi ağırlaşıyor.</p>')
    for x in s["butce"]:
        a('<div class="kart"><h3>%s <span class="rozet">%%%d</span></h3>'
          '<div class="pay"><div class="bar"><i style="width:%d%%"></i></div><b>%%%d</b></div>'
          '<small>%s</small></div>' % (_e(x["kalem"]), x["yuzde"], x["yuzde"], x["yuzde"],
                                       _e(x["not"])))
    a('<div class="uyari">Reklam kalemi bilerek küçük. Organik olarak tuttuğu '
      '<strong>kanıtlanmamış</strong> içeriğe reklam vermek, kötü içeriği daha çok kişiye '
      'göstermekten başka bir işe yaramıyor.</div></div></section>')

    # 9 — ölçüm
    a('<section><div class="wrap"><span class="no">09</span><h2>Ne ölçeceğiz</h2>'
      '<p class="alt">Ölçülmeyen iş tekrar edilemez. Aşağıdaki tablo ilk ay '
      '<strong>taban çizgisi</strong> olarak dolduruluyor; kıyas ikinci aydan başlıyor.</p>'
      '<div class=\"tablo-kaydir\"><table><tr><th>Ölçüt</th><th>Nereden okunuyor</th><th>Sıklık</th><th>Hedef</th></tr>')
    for ad, nereden, siklik, hedef in s["kpi"]:
        a("<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td style='color:var(--kirmizi)'>%s</td></tr>"
          % (_e(ad), _e(nereden), _e(siklik), _e(hedef)))
    a('</table></div><div class="kutu"><strong>En önemli ölçüt en basit olanı:</strong> '
      '"Bizi nereden buldunuz?" sorusunu her müşteriye sorup çeteleye yazmak. '
      'Hiçbir panel bunun yerini tutmuyor.</div></div></section>')

    # 10 — riskler
    a('<section><div class="wrap"><span class="no">10</span><h2>Ne ters gidebilir</h2>'
      '<p class="alt">Bu işlerin çoğu bütçe yetmediği için değil, aşağıdaki beş sebepten '
      'ölüyor. Her birinin önlemini baştan yazıyoruz.</p>')
    for ad, ne, onlem in s["risk"]:
        a('<div class="risk"><b>%s</b><div class="ne">%s</div>'
          '<div class="onlem"><span>önlem</span>%s</div></div>' % (_e(ad), _e(ne), _e(onlem)))
    a('</div></section>')

    # çalışma modeli
    md = s["model"]
    a('<section><div class="wrap"><span class="no">11</span><h2>Nasıl çalışırız</h2>'
      '<p class="alt">Bu strateji iki biçimde yürütülebilir. Sizin işinizde önerdiğimiz: '
      '<strong>%s</strong>.</p><div class="izgara">' % _e(md[md["onerilen"]]["ad"]))
    for anahtar in (md["onerilen"], "aylik" if md["onerilen"] == "proje" else "proje"):
        m = md[anahtar]
        one = anahtar == md["onerilen"]
        a('<div class="kart"%s><span class="rol">%s</span><h3>%s</h3><p>%s</p>'
          '<ol style="margin:12px 0 0 18px;font-size:14px">%s</ol>'
          '<small><b>Süre:</b> %s · <b>Ödeme:</b> %s<br><b>Artısı:</b> %s</small></div>'
          % (' style="border-color:var(--kirmizi)"' if one else "",
             "size önerdiğimiz" if one else "diğer yol", _e(m["ad"]), _e(m["kime"]),
             "".join("<li>%s</li>" % _e(x) for x in m["nasil"]),
             _e(m["sure"]), _e(m["odeme"]), _e(m["avantaj"])))
    a('</div></div></section>')

    a('<div class="cta"><div class="wrap">'
      '<p class="etk" style="color:rgba(255,255,255,.75)">Sıradaki adım</p>'
      '<h2>Bu belgeyi birlikte gözden geçirelim.</h2>'
      '<p style="max-width:60ch;margin-top:10px">Rakamları sizin gerçek verinizle güncelleyelim, '
      'ilk 30 günün listesini birlikte kısaltalım. Yarım saat yeterli.</p>'
      '<a href="https://wa.me/%s">WhatsApp\'tan yaz</a>'
      '<a class="c" href="tel:%s">%s</a>'
      '</div></div>' % (_e(firma_bilgi.get("wa", "")), _e(firma_bilgi.get("telefon", "")),
                        _e(firma_bilgi.get("telefon", ""))))

    a('<footer><div class="wrap mrk"><span>Luna Yapım · lunayapim.com · Bursa</span>'
      '<span>%s · Luna Pusula ile üretildi</span></div></footer>' % _e(s["zaman"]))
    a("</body></html>")
    return "\n".join(p)


SO_FORMAT = {"reels": "reels / dikey video", "carousel": "kaydırmalı görsel seti",
             "tekli": "tek görsel", "story": "story", "uzun": "uzun video", "canli": "canlı yayın"}
