"""
DGS matematik gunlugu icin SVG yardimci kutuphanesi.

Amac: Kesirleri (pay ustte / cizgi / payda altta), uslu ifadeleri ve
denklemleri SLASH ("1/5") kullanmadan, gercekten gorsel olarak cizmek.

Kullanim ornegi:
    from svg_math import Canvas

    c = Canvas(1000, 1800)
    c.text(60, 60, "Baslik", size=28, weight="bold")
    end_x = c.hexpr(60, 200, [
        ("t", "100 x (1 + "),
        ("f", "20", "100"),
        ("t", ") = 120"),
    ], size=22)
    c.save("gunluk/ornek.svg")

Onemli: Font monospace kabul edilerek genislik hesabi yapilir
(CHAR_W_RATIO). Turkce karakterler (ITU sirasiyla İıŞşĞğÜüÖöÇç) de
sorunsuz calisir; metin XML icin escape edilir.
"""

FONT = "DejaVu Sans Mono, Consolas, monospace"
CHAR_W_RATIO = 0.62  # monospace karakter genisligi / font-size orani


class Canvas:
    def __init__(self, width, height, bg="#ffffff"):
        self.width = width
        self.height = height
        self.elements = []
        self.rect(0, 0, width, height, fill=bg)

    def rect(self, x, y, w, h, fill="none", stroke=None, stroke_width=1, rx=0):
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'
        if stroke:
            s += f' stroke="{stroke}" stroke-width="{stroke_width}"'
        if rx:
            s += f' rx="{rx}"'
        s += "/>"
        self.elements.append(s)

    def line(self, x1, y1, x2, y2, stroke="#1a1a1a", stroke_width=2):
        self.elements.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round"/>'
        )

    def circle(self, cx, cy, r, fill="none", stroke="#1a1a1a", stroke_width=2):
        self.elements.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{stroke_width}"/>'
        )

    def text(self, x, y, s, size=20, weight="normal", anchor="start",
              fill="#1a1a1a", italic=False, family=FONT):
        style_font = "italic" if italic else "normal"
        esc = (
            s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        self.elements.append(
            f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" font-style="{style_font}" '
            f'text-anchor="{anchor}" fill="{fill}">{esc}</text>'
        )

    def text_width(self, s, size):
        return len(s) * size * CHAR_W_RATIO

    def fraction(self, x, y_mid, num, den, size=20, fill="#1a1a1a"):
        """x: sol baslangic; y_mid: kesir cizgisinin dikey ortasi.
        Dondurur: kullanilan toplam genislik."""
        num_w = self.text_width(num, size)
        den_w = self.text_width(den, size)
        bar_w = max(num_w, den_w) + size * 0.5
        cx = x + bar_w / 2
        self.text(cx, y_mid - size * 0.35, num, size=size, anchor="middle", fill=fill)
        self.line(x, y_mid, x + bar_w, y_mid, stroke=fill, stroke_width=max(2, size * 0.06))
        self.text(cx, y_mid + size * 0.95, den, size=size, anchor="middle", fill=fill)
        return bar_w

    def sup(self, x, y_base, base, exponent, size=20, fill="#1a1a1a"):
        """Uslu ifade: taban^us. Dondurur: kullanilan genislik."""
        self.text(x, y_base, base, size=size, anchor="start", fill=fill)
        base_w = self.text_width(base, size)
        self.text(x + base_w, y_base - size * 0.45, exponent, size=size * 0.65,
                   anchor="start", fill=fill)
        exp_w = self.text_width(exponent, size * 0.65)
        return base_w + exp_w

    def hexpr(self, x, y_mid, tokens, size=20, gap=8, fill="#1a1a1a"):
        """
        tokens listesi, her biri:
          ("t", "metin")          -> duz metin (taban cizgisi y_mid + size*0.35)
          ("f", "pay", "payda")   -> kesir (dikey ortasi y_mid)
          ("s", "taban", "us")    -> uslu ifade (taban cizgisi y_mid + size*0.35)
        Soldan saga dizer, x'i ilerletir. Dondurur: bitis x.
        """
        cx = x
        for tok in tokens:
            if tok[0] == "t":
                self.text(cx, y_mid + size * 0.35, tok[1], size=size, fill=fill)
                cx += self.text_width(tok[1], size) + gap
            elif tok[0] == "f":
                w = self.fraction(cx, y_mid, tok[1], tok[2], size=size, fill=fill)
                cx += w + gap
            elif tok[0] == "s":
                w = self.sup(cx, y_mid + size * 0.35, tok[1], tok[2], size=size, fill=fill)
                cx += w + gap
        return cx

    def to_svg(self):
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" '
            f'height="{self.height}" viewBox="0 0 {self.width} {self.height}">\n'
            + "\n".join(self.elements)
            + "\n</svg>\n"
        )

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_svg())
