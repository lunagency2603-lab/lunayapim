# -*- coding: utf-8 -*-
"""
Arka plan iş motoru.
Panelden başlatılan taramalar burada ayrı bir iş parçacığında çalışır;
ekrana basılan her satır göreve log olarak yazılır, panel canlı okur.
Terminal açmaya gerek kalmaz.
"""
import threading, itertools, traceback, io, sys, time, contextlib

_sayac = itertools.count(1)
_kilit = threading.Lock()
GOREVLER = {}          # id -> sözlük
SIRA = []              # en yeni sonda


class _Yakala(io.TextIOBase):
    """print() çıktısını göreve satır satır yazar."""
    def __init__(self, gorev):
        self.g = gorev
        self.tampon = ""

    def write(self, s):
        self.tampon += s
        while "\n" in self.tampon:
            satir, self.tampon = self.tampon.split("\n", 1)
            satir = satir.rstrip()
            if satir:
                with _kilit:
                    self.g["log"].append(satir)
                    if len(self.g["log"]) > 4000:
                        del self.g["log"][:1000]
        return len(s)

    def flush(self):
        pass


def yeni(ad, aciklama=""):
    gid = next(_sayac)
    g = {"id": gid, "ad": ad, "aciklama": aciklama, "durum": "bekliyor",
         "log": [], "basladi": time.time(), "bitti": None, "hata": None,
         "adim": "", "toplam_adim": 0, "adim_no": 0}
    with _kilit:
        GOREVLER[gid] = g
        SIRA.append(gid)
        for eski in SIRA[:-25]:
            GOREVLER.pop(eski, None)
        del SIRA[:-25]
    return g


def calistir(ad, fn, aciklama=""):
    """fn(gorev) çağrılır; stdout göreve yönlendirilir."""
    g = yeni(ad, aciklama)

    def sar():
        g["durum"] = "calisiyor"
        yakala = _Yakala(g)
        try:
            with contextlib.redirect_stdout(yakala):
                fn(g)
            yakala.write("\n")
            g["durum"] = "bitti"
        except Exception as ex:
            g["hata"] = "%s: %s" % (type(ex).__name__, ex)
            g["log"].append("HATA — " + g["hata"])
            for satir in traceback.format_exc().splitlines()[-6:]:
                g["log"].append("   " + satir)
            g["durum"] = "hata"
        finally:
            g["bitti"] = time.time()

    t = threading.Thread(target=sar, daemon=True)
    t.start()
    return g


def durum(gid=None, log_baslangic=0):
    with _kilit:
        if gid is not None:
            g = GOREVLER.get(int(gid))
            if not g:
                return None
            return {"id": g["id"], "ad": g["ad"], "durum": g["durum"], "hata": g["hata"],
                    "adim": g["adim"], "adim_no": g["adim_no"], "toplam_adim": g["toplam_adim"],
                    "gecen": round((g["bitti"] or time.time()) - g["basladi"], 1),
                    "log": g["log"][log_baslangic:], "log_uzunluk": len(g["log"])}
        return [{"id": GOREVLER[i]["id"], "ad": GOREVLER[i]["ad"], "durum": GOREVLER[i]["durum"],
                 "adim": GOREVLER[i]["adim"], "hata": GOREVLER[i]["hata"],
                 "gecen": round((GOREVLER[i]["bitti"] or time.time()) - GOREVLER[i]["basladi"], 1)}
                for i in reversed(SIRA) if i in GOREVLER]


def mesgul():
    with _kilit:
        return any(GOREVLER[i]["durum"] == "calisiyor" for i in SIRA if i in GOREVLER)
