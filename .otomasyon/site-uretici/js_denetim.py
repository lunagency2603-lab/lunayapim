# -*- coding: utf-8 -*-
"""Sayfalardaki satır-içi JavaScript'i sözdizimi denetiminden geçirir.

Niçin var: 03.10.2026'da sonislem.py'nin tablo sarmalayıcısı <script> bloğunun
içine class="tablo-kaydir" bastı. Sayfa gözle normal görünüyordu — başlık,
metin, form yerindeydi — ama o sayfadaki bütün JS tek bir "Unexpected
identifier" ile düşmüştü ve araç sessizce çalışmıyordu. Böyle bir arızayı
HTML denetimi yakalamaz; yakalayan tek şey JS'i ayrıştırmaktır.

Kullanım:
    python3 site-uretici/js_denetim.py <depo kökü>
Çıktı: bozuk sayfa listesi. node yoksa sessizce atlar (0 döner).
"""
import io
import os
import re
import subprocess
import sys
import tempfile

_SCRIPT = re.compile(r"<script\b([^>]*)>([\s\S]*?)</script\s*>", re.I)
_ATLA = ("/.git", "/node_modules", "/.otomasyon", "/onizleme")


def _node_var():
    try:
        subprocess.run(["node", "--version"], capture_output=True, timeout=10)
        return True
    except Exception:
        return False


def denetle(kok):
    if not _node_var():
        return {"node": False, "sayfa": 0, "bozuk": []}
    bozuk, sayilan = [], 0
    for r, _k, dosyalar in os.walk(kok):
        if any(a in r.replace(os.sep, "/") for a in _ATLA):
            continue
        for ad in dosyalar:
            if not ad.endswith(".html"):
                continue
            yol = os.path.join(r, ad)
            s = io.open(yol, encoding="utf-8", errors="replace").read()
            for sira, m in enumerate(_SCRIPT.finditer(s), 1):
                nitelik, govde = m.group(1) or "", m.group(2)
                # dış dosya ve JSON-LD gibi veri blokları JS değildir
                if "src=" in nitelik.lower() or "type=" in nitelik.lower():
                    continue
                if not govde.strip():
                    continue
                sayilan += 1
                with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                                 encoding="utf-8") as f:
                    f.write(govde)
                    gecici = f.name
                try:
                    p = subprocess.run(["node", "--check", gecici],
                                       capture_output=True, text=True, timeout=30)
                    if p.returncode != 0:
                        ilk = [x for x in (p.stderr or "").splitlines()
                               if "Error" in x or "error" in x]
                        bozuk.append((os.path.relpath(yol, kok), sira,
                                      (ilk[0] if ilk else "sözdizimi hatası").strip()))
                finally:
                    try:
                        os.unlink(gecici)
                    except Exception:
                        pass
    return {"node": True, "sayfa": sayilan, "bozuk": bozuk}


if __name__ == "__main__":
    kok = sys.argv[1] if len(sys.argv) > 1 else "."
    s = denetle(kok)
    if not s["node"]:
        print("js_denetim: node bulunamadı, atlandı")
        raise SystemExit(0)
    print("js_denetim: %d satır-içi betik denetlendi, %d bozuk"
          % (s["sayfa"], len(s["bozuk"])))
    for yol, sira, ileti in s["bozuk"]:
        print("  HATA  %-52s betik #%d  %s" % (yol, sira, ileti))
    raise SystemExit(1 if s["bozuk"] else 0)
