#!/usr/bin/env python3
"""Sort log tables in reverse-chronological order by first <td> date."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "logs"
FILES = ["shows.html", "sports.html", "albums.html", "classes.html",
         "books.html", "movies.html", "tv.html", "vidya.html"]

ROW_RE = re.compile(r"<tr>\s*(?:<td>.*?</td>\s*)+</tr>", re.DOTALL)
FIRST_TD_RE = re.compile(r"<td>([^<]*)</td>")


def date_key(row):
    m = FIRST_TD_RE.search(row)
    s = m.group(1).strip() if m else ""
    md = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
    if md:
        return (int(md.group(1)), int(md.group(2)), int(md.group(3)))
    mm = re.match(r"^(\d{4})-(\d{2})$", s)
    if mm:
        return (int(mm.group(1)), int(mm.group(2)), 99)
    my = re.match(r"^(\d{4})$", s)
    if my:
        return (int(my.group(1)), 99, 99)
    return (0, 0, 0)


def sort_file(path):
    text = path.read_text()
    matches = list(ROW_RE.finditer(text))
    if not matches:
        return False
    rows = [m.group(0) for m in matches]
    order = list(range(len(rows)))
    order.sort(key=lambda i: date_key(rows[i]), reverse=True)
    if order == list(range(len(rows))):
        return False
    new_rows = [rows[i] for i in order]
    separators = [text[matches[i].end():matches[i + 1].start()]
                  for i in range(len(matches) - 1)]
    before = text[:matches[0].start()]
    after = text[matches[-1].end():]
    body = new_rows[0]
    for i in range(1, len(new_rows)):
        body += separators[i - 1] + new_rows[i]
    path.write_text(before + body + after)
    return True


def main():
    for name in FILES:
        p = ROOT / name
        if not p.exists():
            continue
        changed = sort_file(p)
        print(f"{name}: {'sorted' if changed else 'already ordered'}")


if __name__ == "__main__":
    main()
