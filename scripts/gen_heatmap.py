import re, urllib.request, datetime, html
USER = "hedichakchouk"
req = urllib.request.Request(f"https://github.com/users/{USER}/contributions", headers={"User-Agent": "Mozilla/5.0"})
page = urllib.request.urlopen(req, timeout=30).read().decode()
days = {}
for m in re.finditer(r'<td[^>]*data-date="(\d{4}-\d{2}-\d{2})"[^>]*id="([^"]+)"[^>]*data-level="(\d)"', page):
    days[m.group(1)] = [int(m.group(3)), m.group(2)]
counts = {}
for m in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', page):
    n = re.match(r'(\d+) contribution', m.group(2).strip())
    counts[m.group(1)] = int(n.group(1)) if n else 0
cells = sorted((d, v[0], counts.get(v[1], 0)) for d, v in days.items())
total = sum(c for _, _, c in cells)
first = datetime.date.fromisoformat(cells[0][0])
pal = ["#161b22", "#2e1a6b", "#5e30e8", "#8a63ff", "#c4aaff"]
S, G, X0, Y0 = 13, 4, 30, 44
W = X0 + 53 * (S + G) + 10
H = Y0 + 7 * (S + G) + 30
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
'<style>text{font:12px "SF Mono",Consolas,monospace;fill:#8b949e}.t{fill:#c9d1d9;font-size:13px}.c{opacity:0;animation:in .5s ease-out forwards}@keyframes in{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}</style>',
f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117"/>',
f'<text x="{X0}" y="26" class="t">{total} contributions in the last year</text>']
for d, lvl, n in cells:
    dt = datetime.date.fromisoformat(d)
    col = (dt - first).days // 7 + (1 if first.weekday() != 6 else 0) if False else ((dt - first + datetime.timedelta(days=(first.weekday()+1) % 7)).days // 7)
    row = (dt.weekday() + 1) % 7
    x, y = X0 + col * (S + G), Y0 + row * (S + G)
    delay = round((col + row) * 0.025, 3)
    out.append(f'<rect class="c" style="animation-delay:{delay}s" x="{x}" y="{y}" width="{S}" height="{S}" rx="3" fill="{pal[lvl]}"><title>{n} on {d}</title></rect>')
out.append('</svg>')
open("assets/heatmap.svg", "w").write("\n".join(out))
print("cells", len(cells), "total", total)
