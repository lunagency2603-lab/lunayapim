# -*- coding: utf-8 -*-
"""SQLite katmanı — aday işletmeler, denetim sonuçları, tahminler, demolar."""
import sqlite3, os, json, datetime
from .ayarlar import VT_YOLU

SEMA = """
CREATE TABLE IF NOT EXISTS adaylar (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kaynak TEXT, kaynak_id TEXT UNIQUE,
  ad TEXT NOT NULL, sektor TEXT, sehir TEXT, ilce TEXT,
  adres TEXT, telefon TEXT, site TEXT,
  puan REAL, yorum_sayisi INTEGER, fotograf_sayisi INTEGER,
  enlem REAL, boylam REAL,
  bulundu TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS ziyaret_kayit (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  yuklendi TEXT DEFAULT (datetime('now')),
  kaynak TEXT, donem TEXT,
  kullanici INTEGER, goruntuleme INTEGER, iletisim INTEGER,
  ozet TEXT
);
CREATE TABLE IF NOT EXISTS arama_kayit (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  yuklendi TEXT DEFAULT (datetime('now')),
  kaynak TEXT,
  donem TEXT,                -- kullanıcının yazdığı dönem etiketi
  tiklama INTEGER, gosterim INTEGER, sayfa INTEGER,
  ozet TEXT                  -- json: tam analiz
);
CREATE TABLE IF NOT EXISTS denetimler (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  aday_id INTEGER NOT NULL,
  tarih TEXT DEFAULT (datetime('now')),
  skor INTEGER,
  eksikler TEXT,          -- json listesi
  detay TEXT,             -- json sözlük
  UNIQUE(aday_id, tarih),
  FOREIGN KEY(aday_id) REFERENCES adaylar(id)
);
CREATE TABLE IF NOT EXISTS tahminler (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  aday_id INTEGER NOT NULL,
  tarih TEXT DEFAULT (datetime('now')),
  mevcut_goruntulenme INTEGER, hedef_goruntulenme INTEGER,
  mevcut_iletisim REAL, hedef_iletisim REAL,
  mevcut_is REAL, hedef_is REAL,
  ek_gelir REAL, detay TEXT,
  FOREIGN KEY(aday_id) REFERENCES adaylar(id)
);
CREATE TABLE IF NOT EXISTS demolar (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  aday_id INTEGER NOT NULL,
  tarih TEXT DEFAULT (datetime('now')),
  dosya TEXT, mesaj TEXT,
  FOREIGN KEY(aday_id) REFERENCES adaylar(id)
);
CREATE TABLE IF NOT EXISTS temas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  aday_id INTEGER NOT NULL,
  tarih TEXT DEFAULT (datetime('now')),
  kanal TEXT, durum TEXT, not_ TEXT,
  yon TEXT DEFAULT 'giden',        -- giden | gelen
  kisi TEXT,                        -- kiminle konuşuldu
  sonraki_adim TEXT,
  sonraki_tarih TEXT,
  FOREIGN KEY(aday_id) REFERENCES adaylar(id)
);
CREATE TABLE IF NOT EXISTS kisiler (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  aday_id INTEGER NOT NULL,
  isim TEXT, unvan TEXT, eposta TEXT, telefon TEXT,
  kaynak TEXT,                      -- hangi sayfada bulundu
  bulundu TEXT DEFAULT (datetime('now')),
  UNIQUE(aday_id, isim, unvan),
  FOREIGN KEY(aday_id) REFERENCES adaylar(id)
);
CREATE TABLE IF NOT EXISTS kanallar (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  aday_id INTEGER NOT NULL,
  tur TEXT NOT NULL,                -- eposta | telefon | whatsapp | instagram | facebook | linkedin | x | youtube | web
  deger TEXT NOT NULL,
  kaynak TEXT, dogrulandi INTEGER DEFAULT 0, not_ TEXT,
  bulundu TEXT DEFAULT (datetime('now')),
  UNIQUE(aday_id, tur, deger),
  FOREIGN KEY(aday_id) REFERENCES adaylar(id)
);
CREATE TABLE IF NOT EXISTS rakip_teklif (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  hizmet TEXT NOT NULL, sehir TEXT, tutar REAL NOT NULL,
  kaynak TEXT, not_ TEXT, tarih TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS isler (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  aday_id INTEGER,
  musteri TEXT NOT NULL, hizmet TEXT NOT NULL, sehir TEXT,
  asama TEXT DEFAULT 'teklif',      -- teklif|onay|uretim|kurgu|teslim|kapandi|kayip
  bedel REAL, teslim_tarihi TEXT, notlar TEXT,
  acildi TEXT DEFAULT (datetime('now')),
  guncellendi TEXT DEFAULT (datetime('now')),
  FOREIGN KEY(aday_id) REFERENCES adaylar(id)
);
CREATE INDEX IF NOT EXISTS ix_aday_sehir ON adaylar(sehir, sektor);
CREATE INDEX IF NOT EXISTS ix_is_asama ON isler(asama);
CREATE INDEX IF NOT EXISTS ix_kisi_aday ON kisiler(aday_id);
CREATE INDEX IF NOT EXISTS ix_kanal_aday ON kanallar(aday_id);
CREATE INDEX IF NOT EXISTS ix_temas_aday ON temas(aday_id);
"""

# iCloud Drive, ağ sürücüsü ya da senkron klasörlerde SQLite yazamaz.
# Bu durumda veritabanını ev dizinine alır ve bir kere haber verir.
YEDEK_YOL = os.path.expanduser("~/.luna-pusula/pusula.db")
_kullanilan = {"yol": VT_YOLU, "uyarildi": False}


def vt_yolu():
    return _kullanilan["yol"]


EK_SUTUNLAR = [
    ("adaylar", "durum", "TEXT DEFAULT 'yeni'"),
    ("adaylar", "eposta", "TEXT"),
    ("adaylar", "telefon_tipi", "TEXT"),
    ("adaylar", "wa_uygun", "INTEGER"),
    ("adaylar", "zengin", "INTEGER DEFAULT 0"),
    ("adaylar", "not_", "TEXT"),
    ("adaylar", "sosyal", "TEXT"),          # json: sosyal denetim sonucu
    ("adaylar", "sosyal_skor", "INTEGER"),
    ("temas", "yon", "TEXT DEFAULT 'giden'"),
    ("temas", "kisi", "TEXT"),
    ("temas", "sonraki_adim", "TEXT"),
    ("temas", "sonraki_tarih", "TEXT"),
    ("temas", "kullanici", "TEXT"),
    ("isler", "kullanici", "TEXT"),
]


def _gocur(b):
    """Eski veritabanlarına eksik sütunları sessizce ekler."""
    for tablo, sutun, tanim in EK_SUTUNLAR:
        try:
            b.execute("ALTER TABLE %s ADD COLUMN %s %s" % (tablo, sutun, tanim))
        except sqlite3.OperationalError:
            pass


def _ac(yol):
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    # timeout: kilit varsa hata vermeden bu kadar saniye bekler (eskiden 15'ti)
    b = sqlite3.connect(yol, timeout=60)
    b.row_factory = sqlite3.Row
    b.executescript(SEMA)
    # WAL: okuyucu yazıcıyı, yazıcı okuyucuyu bloklamaz. Ağ/iCloud sürücüsünde
    # WAL desteklenmediği için orada sessizce DELETE'e düşüyoruz.
    try:
        kip = b.execute("PRAGMA journal_mode=WAL").fetchone()[0]
        if str(kip).lower() != "wal":
            b.execute("PRAGMA journal_mode=DELETE")
    except sqlite3.Error:
        b.execute("PRAGMA journal_mode=DELETE")
    b.execute("PRAGMA busy_timeout=60000")
    b.execute("PRAGMA synchronous=NORMAL")
    _gocur(b)
    b.commit()
    return b


def baglan():
    yol = _kullanilan["yol"]
    try:
        return _ac(yol)
    except sqlite3.OperationalError:
        if yol == YEDEK_YOL:
            raise
        if not _kullanilan["uyarildi"]:
            print("  ! Veritabanı bu klasöre yazılamıyor (iCloud/ağ sürücüsü olabilir).")
            print("    Yedek konuma geçildi: %s" % YEDEK_YOL)
            _kullanilan["uyarildi"] = True
        _kullanilan["yol"] = YEDEK_YOL
        return _ac(YEDEK_YOL)

def aday_ekle(b, k):
    try:
        b.execute("""INSERT INTO adaylar
          (kaynak,kaynak_id,ad,sektor,sehir,ilce,adres,telefon,site,puan,yorum_sayisi,fotograf_sayisi,enlem,boylam)
          VALUES (:kaynak,:kaynak_id,:ad,:sektor,:sehir,:ilce,:adres,:telefon,:site,:puan,:yorum_sayisi,:fotograf_sayisi,:enlem,:boylam)""", k)
        return True
    except sqlite3.IntegrityError:
        b.execute("""UPDATE adaylar SET ad=:ad, telefon=COALESCE(:telefon,telefon), site=COALESCE(:site,site),
                     puan=:puan, yorum_sayisi=:yorum_sayisi, fotograf_sayisi=:fotograf_sayisi
                     WHERE kaynak_id=:kaynak_id""", k)
        return False

def denetim_kaydet(b, aday_id, skor, eksikler, detay):
    b.execute("INSERT INTO denetimler (aday_id,skor,eksikler,detay) VALUES (?,?,?,?)",
              (aday_id, skor, json.dumps(eksikler, ensure_ascii=False), json.dumps(detay, ensure_ascii=False)))

def tahmin_kaydet(b, aday_id, t):
    b.execute("""INSERT INTO tahminler
      (aday_id,mevcut_goruntulenme,hedef_goruntulenme,mevcut_iletisim,hedef_iletisim,mevcut_is,hedef_is,ek_gelir,detay)
      VALUES (?,?,?,?,?,?,?,?,?)""",
      (aday_id, t["mevcut_goruntulenme"], t["hedef_goruntulenme"], t["mevcut_iletisim"],
       t["hedef_iletisim"], t["mevcut_is"], t["hedef_is"], t["ek_gelir"],
       json.dumps(t, ensure_ascii=False)))

def demo_kaydet(b, aday_id, dosya, mesaj):
    b.execute("INSERT INTO demolar (aday_id,dosya,mesaj) VALUES (?,?,?)", (aday_id, dosya, mesaj))

def son_denetimler(b, sehir=None, sektor=None, limit=None):
    q = """SELECT a.*, d.skor, d.eksikler, d.detay, d.tarih AS denetim_tarihi
           FROM adaylar a
           JOIN denetimler d ON d.id = (SELECT id FROM denetimler WHERE aday_id=a.id ORDER BY id DESC LIMIT 1)"""
    k, p = [], []
    if sehir:  k.append("a.sehir=?");  p.append(sehir)
    if sektor: k.append("a.sektor=?"); p.append(sektor)
    if k: q += " WHERE " + " AND ".join(k)
    q += " ORDER BY d.skor ASC"
    if limit: q += " LIMIT %d" % int(limit)
    return b.execute(q, p).fetchall()

def son_tahmin(b, aday_id):
    r = b.execute("SELECT * FROM tahminler WHERE aday_id=? ORDER BY id DESC LIMIT 1", (aday_id,)).fetchone()
    return dict(r) if r else None


ASAMALAR = ["teklif","onay","uretim","kurgu","teslim","kapandi","kayip"]
ASAMA_AD = {"teklif":"Teklif","onay":"Onaylandı","uretim":"Üretim","kurgu":"Kurgu",
            "teslim":"Teslim","kapandi":"Kapandı","kayip":"Kayıp"}

def is_ekle(b, musteri, hizmet, sehir=None, aday_id=None, bedel=None, teslim=None,
            notlar=None, kullanici=None):
    i = b.execute("""INSERT INTO isler (aday_id,musteri,hizmet,sehir,bedel,teslim_tarihi,
                                        notlar,kullanici)
                     VALUES (?,?,?,?,?,?,?,?)""",
                  (aday_id, musteri, hizmet, sehir, bedel, teslim, notlar, kullanici))
    return i.lastrowid

def is_asama(b, is_id, asama):
    b.execute("UPDATE isler SET asama=?, guncellendi=datetime('now') WHERE id=?", (asama, is_id))

def temas_ekle(b, aday_id, kanal, durum, not_=None):
    b.execute("INSERT INTO temas (aday_id,kanal,durum,not_) VALUES (?,?,?,?)", (aday_id, kanal, durum, not_))

def istatistik(b):
    def tek(q, *p):
        r = b.execute(q, p).fetchone()
        return (r[0] if r and r[0] is not None else 0)
    d = {
      "aday": tek("SELECT COUNT(*) FROM adaylar"),
      "denetlenen": tek("SELECT COUNT(DISTINCT aday_id) FROM denetimler"),
      "demo": tek("SELECT COUNT(DISTINCT aday_id) FROM demolar"),
      "temas": tek("SELECT COUNT(DISTINCT aday_id) FROM temas"),
      "is": tek("SELECT COUNT(*) FROM isler"),
      "kazanilan": tek("SELECT COUNT(*) FROM isler WHERE asama='kapandi'"),
      "ciro": tek("SELECT SUM(bedel) FROM isler WHERE asama='kapandi'"),
      "acik_ciro": tek("SELECT SUM(bedel) FROM isler WHERE asama NOT IN ('kapandi','kayip')"),
    }
    d["sehirler"] = [dict(r) for r in b.execute(
      "SELECT sehir, COUNT(*) adet FROM adaylar GROUP BY sehir ORDER BY adet DESC").fetchall()]
    d["sektorler"] = [dict(r) for r in b.execute(
      "SELECT sektor, COUNT(*) adet FROM adaylar GROUP BY sektor ORDER BY adet DESC").fetchall()]
    d["skor_dagilim"] = [dict(r) for r in b.execute(
      """SELECT CASE WHEN skor<40 THEN '0-39' WHEN skor<55 THEN '40-54'
                     WHEN skor<70 THEN '55-69' WHEN skor<85 THEN '70-84' ELSE '85-100' END kusak,
                COUNT(*) adet FROM (SELECT aday_id, MAX(id) mid, skor FROM denetimler GROUP BY aday_id)
         GROUP BY kusak ORDER BY kusak""").fetchall()]
    d["asamalar"] = [dict(r) for r in b.execute(
      "SELECT asama, COUNT(*) adet, SUM(bedel) bedel FROM isler GROUP BY asama").fetchall()]
    return d


# ============================================================
#  RAF (CRM) — durumlar ve temas kaydı
# ============================================================
DURUMLAR = ["yeni", "arastirildi", "temas", "cevap_bekleniyor", "gorusme",
            "teklif", "kazanildi", "kayip", "uygun_degil"]
DURUM_AD = {
    "yeni": "Yeni", "arastirildi": "Araştırıldı", "temas": "Temas kuruldu",
    "cevap_bekleniyor": "Cevap bekleniyor", "gorusme": "Görüşme", "teklif": "Teklif verildi",
    "kazanildi": "Kazanıldı", "kayip": "Kayıp", "uygun_degil": "Uygun değil",
}
# Bir temas sonucundan hangi duruma geçilir
SONUC_DURUM = {
    "mesaj atildi": "cevap_bekleniyor", "eposta gonderildi": "cevap_bekleniyor",
    "arandi ulasilamadi": "cevap_bekleniyor", "arandi gorusuldu": "gorusme",
    "gorusuldu": "gorusme", "teklif verildi": "teklif",
    "kazanildi": "kazanildi", "ilgilenmiyor": "kayip", "uygun degil": "uygun_degil",
}


def durum_ayarla(b, aday_id, durum):
    if durum in DURUMLAR:
        b.execute("UPDATE adaylar SET durum=? WHERE id=?", (durum, aday_id))


def temas_ekle(b, aday_id, kanal, durum, not_=None, yon="giden", kisi=None,
               sonraki_adim=None, sonraki_tarih=None, kullanici=None):
    b.execute("""INSERT INTO temas (aday_id,kanal,durum,not_,yon,kisi,sonraki_adim,
                                    sonraki_tarih,kullanici)
                 VALUES (?,?,?,?,?,?,?,?,?)""",
              (aday_id, kanal, durum, not_, yon, kisi, sonraki_adim, sonraki_tarih,
               kullanici))
    yeni = SONUC_DURUM.get((durum or "").strip().lower())
    if yeni:
        durum_ayarla(b, aday_id, yeni)


def kisi_ekle(b, aday_id, isim, unvan=None, eposta=None, telefon=None, kaynak=None):
    try:
        b.execute("""INSERT INTO kisiler (aday_id,isim,unvan,eposta,telefon,kaynak)
                     VALUES (?,?,?,?,?,?)""", (aday_id, isim, unvan, eposta, telefon, kaynak))
        return True
    except sqlite3.IntegrityError:
        b.execute("""UPDATE kisiler SET eposta=COALESCE(?,eposta), telefon=COALESCE(?,telefon),
                     kaynak=COALESCE(?,kaynak) WHERE aday_id=? AND isim=? AND unvan IS ?""",
                  (eposta, telefon, kaynak, aday_id, isim, unvan))
        return False
def ziyaret_kaydet(b, kaynak, donem, sonuc):
    t = sonuc.get("toplam") or {}
    b.execute("""INSERT INTO ziyaret_kayit (kaynak,donem,kullanici,goruntuleme,iletisim,ozet)
                 VALUES (?,?,?,?,?,?)""",
              (kaynak, donem, t.get("kullanici"), t.get("goruntuleme"),
               sonuc.get("iletisim_toplam"), json.dumps(sonuc, ensure_ascii=False)))
    return b.execute("SELECT last_insert_rowid()").fetchone()[0]


def ziyaret_listesi(b, limit=24):
    return [dict(r) for r in b.execute(
        "SELECT id,yuklendi,kaynak,donem,kullanici,goruntuleme,iletisim FROM ziyaret_kayit "
        "ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]


def ziyaret_getir(b, kayit_id=None):
    q = ("SELECT * FROM ziyaret_kayit WHERE id=?" if kayit_id
         else "SELECT * FROM ziyaret_kayit ORDER BY id DESC LIMIT 1")
    r = b.execute(q, (kayit_id,) if kayit_id else ()).fetchone()
    if not r:
        return None
    d = dict(r)
    try:
        d["ozet"] = json.loads(d["ozet"])
    except Exception:
        d["ozet"] = None
    return d


def arama_kaydet(b, kaynak, donem, sonuc):
    t = (sonuc.get("sayfa") or {}).get("toplam") or {}
    b.execute("""INSERT INTO arama_kayit (kaynak,donem,tiklama,gosterim,sayfa,ozet)
                 VALUES (?,?,?,?,?,?)""",
              (kaynak, donem, t.get("tiklama"), t.get("gosterim"), t.get("sayfa"),
               json.dumps(sonuc, ensure_ascii=False)))
    return b.execute("SELECT last_insert_rowid()").fetchone()[0]


def arama_listesi(b, limit=24):
    return [dict(r) for r in b.execute(
        "SELECT id,yuklendi,kaynak,donem,tiklama,gosterim,sayfa FROM arama_kayit "
        "ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]


def arama_getir(b, kayit_id=None):
    q = ("SELECT * FROM arama_kayit WHERE id=?" if kayit_id
         else "SELECT * FROM arama_kayit ORDER BY id DESC LIMIT 1")
    r = b.execute(q, (kayit_id,) if kayit_id else ()).fetchone()
    if not r:
        return None
    d = dict(r)
    try:
        d["ozet"] = json.loads(d["ozet"])
    except Exception:
        d["ozet"] = None
    return d


def sosyal_kaydet(b, aday_id, sonuc, skor=None):
    """Sosyal medya denetim sonucunu adayın satırına json olarak yazar."""
    b.execute("UPDATE adaylar SET sosyal=?, sosyal_skor=? WHERE id=?",
              (json.dumps(sonuc, ensure_ascii=False), skor, aday_id))


def sosyal_getir(b, aday_id):
    """Kayıtlı sosyal denetim sonucunu döner; yoksa None."""
    r = b.execute("SELECT sosyal FROM adaylar WHERE id=?", (aday_id,)).fetchone()
    if not r or not r["sosyal"]:
        return None
    try:
        return json.loads(r["sosyal"])
    except Exception:
        return None


def kanal_ekle(b, aday_id, tur, deger, kaynak=None, dogrulandi=0, not_=None):
    try:
        b.execute("""INSERT INTO kanallar (aday_id,tur,deger,kaynak,dogrulandi,not_)
                     VALUES (?,?,?,?,?,?)""", (aday_id, tur, deger, kaynak, dogrulandi, not_))
        return True
    except sqlite3.IntegrityError:
        b.execute("""UPDATE kanallar SET kaynak=COALESCE(?,kaynak), dogrulandi=?, not_=COALESCE(?,not_)
                     WHERE aday_id=? AND tur=? AND deger=?""",
                  (kaynak, dogrulandi, not_, aday_id, tur, deger))
        return False


def kisiler_getir(b, aday_id):
    return [dict(r) for r in b.execute(
        "SELECT * FROM kisiler WHERE aday_id=? ORDER BY id", (aday_id,)).fetchall()]


def kanallar_getir(b, aday_id):
    return [dict(r) for r in b.execute(
        "SELECT * FROM kanallar WHERE aday_id=? ORDER BY tur, id", (aday_id,)).fetchall()]


def temaslar_getir(b, aday_id=None, limit=200):
    q = """SELECT t.*, a.ad AS firma, a.sehir FROM temas t
           JOIN adaylar a ON a.id=t.aday_id"""
    p = []
    if aday_id:
        q += " WHERE t.aday_id=?"; p.append(aday_id)
    q += " ORDER BY t.id DESC LIMIT %d" % int(limit)
    return [dict(r) for r in b.execute(q, p).fetchall()]


def takip_gerekenler(b):
    """Sonraki adım tarihi gelmiş ya da geçmiş temaslar."""
    return [dict(r) for r in b.execute("""
        SELECT t.*, a.ad AS firma, a.sehir, a.telefon, a.durum
        FROM temas t JOIN adaylar a ON a.id=t.aday_id
        WHERE t.sonraki_tarih IS NOT NULL AND t.sonraki_tarih <> ''
          AND date(t.sonraki_tarih) <= date('now')
          AND a.durum NOT IN ('kazanildi','kayip','uygun_degil')
          AND t.id = (SELECT MAX(id) FROM temas WHERE aday_id=a.id)
        ORDER BY t.sonraki_tarih""").fetchall()]


def raf(b):
    """Durum bazında aday sayısı ve tahmini ek ciro."""
    return [dict(r) for r in b.execute("""
        SELECT COALESCE(durum,'yeni') AS durum, COUNT(*) AS adet FROM adaylar
        GROUP BY COALESCE(durum,'yeni')""").fetchall()]


def rakip_teklif_ekle(b, hizmet, tutar, sehir=None, kaynak=None, not_=None):
    b.execute("INSERT INTO rakip_teklif (hizmet,tutar,sehir,kaynak,not_) VALUES (?,?,?,?,?)",
              (hizmet, float(tutar), sehir, kaynak, not_))


def rakip_ortalama(b, hizmet):
    r = b.execute("""SELECT COUNT(*) n, AVG(tutar) ort, MIN(tutar) alt, MAX(tutar) ust
                     FROM rakip_teklif WHERE hizmet=?""", (hizmet,)).fetchone()
    if not r or not r["n"]:
        return None
    return {"adet": r["n"], "ortalama": r["ort"], "alt": r["alt"], "ust": r["ust"]}
