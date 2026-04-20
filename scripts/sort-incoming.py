#!/usr/bin/env python3
"""
Sort /imgs/incoming/ into /imgs/YYYY/ with YYYY-MM-DD-slug.ext names.
Reads EXIF DateTimeOriginal + GPS. Prints a summary for wiring into photos.html.
Run with: /home/will/.venvs/photos/bin/python scripts/sort-incoming.py
"""
import os, re, shutil, sys
from pathlib import Path
from PIL import Image, ExifTags
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent.parent
INCOMING = ROOT / "imgs" / "incoming"
IMGS = ROOT / "imgs"

DT_TAG = next(k for k, v in ExifTags.TAGS.items() if v == "DateTimeOriginal")
GPS_TAG = next(k for k, v in ExifTags.TAGS.items() if v == "GPSInfo")

def gps_to_deg(dms, ref):
    d, m, s = [float(x) for x in dms]
    val = d + m/60 + s/3600
    return -val if ref in ("S", "W") else val

def slug(name):
    stem = Path(name).stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    return stem or "img"

def process(path):
    try:
        img = Image.open(path)
        exif = img.getexif()
        # merge ExifIFD (where DateTimeOriginal actually lives)
        ifd = exif.get_ifd(0x8769) if exif else {}
        gps = exif.get_ifd(0x8825) if exif else {}
    except Exception as e:
        return {"error": str(e)}
    dt = ifd.get(DT_TAG) or exif.get(306)  # DateTime fallback
    date = None
    if dt:
        m = re.match(r"(\d{4}):(\d{2}):(\d{2})", dt)
        if m:
            date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    lat = lon = None
    if gps and 1 in gps and 2 in gps and 3 in gps and 4 in gps:
        try:
            lat = gps_to_deg(gps[2], gps[1])
            lon = gps_to_deg(gps[4], gps[3])
        except Exception:
            pass
    return {"date": date, "lat": lat, "lon": lon}

def main():
    if not INCOMING.exists():
        print(f"no {INCOMING}"); sys.exit(1)
    files = sorted(p for p in INCOMING.iterdir() if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".heic"})
    if not files:
        print("incoming/ is empty"); return
    rows = []
    for f in files:
        info = process(f)
        if "error" in info:
            print(f"  ERR  {f.name}: {info['error']}")
            continue
        date = info["date"]
        if not date:
            print(f"  SKIP {f.name}: no EXIF date (leaving in incoming/)")
            continue
        year = date[:4]
        dest_dir = IMGS / year
        dest_dir.mkdir(exist_ok=True)
        s = slug(f.name)
        dest = dest_dir / f"{date}-{s}{f.suffix.lower()}"
        n = 2
        while dest.exists():
            dest = dest_dir / f"{date}-{s}-{n}{f.suffix.lower()}"
            n += 1
        shutil.move(str(f), str(dest))
        rel = dest.relative_to(ROOT)
        gps = f"{info['lat']:.5f},{info['lon']:.5f}" if info["lat"] is not None else "-"
        rows.append((rel, date, gps))
        print(f"  OK   {f.name} -> {rel}  gps={gps}")
    print()
    print("=== <img> tags (paste into photos.html) ===")
    for rel, date, gps in rows:
        tag = f'<img src="../{rel}"'
        if gps != "-":
            tag += f' data-gps="{gps}"'
        tag += ">"
        print(tag)

if __name__ == "__main__":
    main()
