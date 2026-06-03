from pathlib import Path

TIMESTAMP = "2026-05-01 13:55:07 PDT"
OUT = Path("output/pdf/repo-architecture.pdf")


def esc(value):
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )


class PdfCanvas:
    def __init__(self):
        self.ops = []

    def raw(self, value):
        self.ops.append(value)

    def line(self, x1, y1, x2, y2, width=1, color=(0.2, 0.25, 0.32)):
        r, g, b = color
        self.raw(f"{r} {g} {b} RG {width} w {x1} {y1} m {x2} {y2} l S")

    def rect(self, x, y, w, h, fill=(1, 1, 1), stroke=(0.18, 0.23, 0.3), width=1):
        fr, fg, fb = fill
        sr, sg, sb = stroke
        self.raw(f"{fr} {fg} {fb} rg {sr} {sg} {sb} RG {width} w {x} {y} {w} {h} re B")

    def text(self, x, y, text, size=11, font="F1", color=(0.08, 0.1, 0.14)):
        r, g, b = color
        self.raw(f"BT /{font} {size} Tf {r} {g} {b} rg {x} {y} Td ({esc(text)}) Tj ET")

    def multiline(self, x, y, lines, size=10, leading=14, font="F1", color=(0.08, 0.1, 0.14)):
        for idx, line in enumerate(lines):
            self.text(x, y - idx * leading, line, size=size, font=font, color=color)

    def arrow(self, x1, y1, x2, y2):
        self.line(x1, y1, x2, y2, width=1.2, color=(0.1, 0.34, 0.62))
        if x2 >= x1:
            self.raw(f"0.1 0.34 0.62 rg {x2} {y2} m {x2-7} {y2+4} l {x2-7} {y2-4} l f")
        else:
            self.raw(f"0.1 0.34 0.62 rg {x2} {y2} m {x2+7} {y2+4} l {x2+7} {y2-4} l f")

    def box(self, x, y, w, h, title, lines, fill=(0.95, 0.98, 1.0)):
        self.rect(x, y, w, h, fill=fill, stroke=(0.58, 0.66, 0.76), width=1)
        self.text(x + 12, y + h - 22, title, size=12, font="F2", color=(0.05, 0.15, 0.28))
        self.multiline(x + 12, y + h - 42, lines, size=9.5, leading=12, color=(0.22, 0.26, 0.32))


def build_pdf():
    c = PdfCanvas()

    c.raw("1 1 1 rg 0 0 612 792 re f")

    # Header
    c.text(54, 744, "Repo Architecture", size=24, font="F2")
    c.text(54, 724, f"Generated: {TIMESTAMP}", size=10, color=(0.38, 0.42, 0.48))
    c.line(54, 710, 558, 710, width=0.8, color=(0.72, 0.76, 0.82))

    # Brief document
    c.text(54, 684, "Overview", size=15, font="F2")
    overview = [
        "This repository is a small static GitHub Pages portfolio site served from docs/.",
        "It has no build step, backend service, database, or framework dependency.",
        "The homepage is a static shell that fetches JSON content and renders sections in the browser.",
    ]
    c.multiline(54, 664, overview, size=10.5, leading=15)

    c.text(54, 608, "Key Files", size=15, font="F2")
    key_files = [
        "docs/index.html - page shell, CSS, render functions, content fetcher, analytics hook",
        "docs/content.json - navigation, theme, copy, work sections, writing links, contact data",
        "docs/assets/image.jpg - profile image used by the hero section",
        "docs/publications/index.md - publications landing page linked from the main nav",
    ]
    c.multiline(54, 588, key_files, size=10, leading=14)

    c.text(54, 516, "Architecture Diagram", size=15, font="F2")

    # Diagram boxes
    c.box(54, 430, 120, 58, "Visitor Browser", ["Requests site", "Runs client JS"], fill=(0.98, 0.99, 1.0))
    c.box(220, 430, 142, 58, "GitHub Pages", ["Serves docs/ files", "Static hosting only"], fill=(0.96, 0.99, 0.96))
    c.box(408, 430, 150, 58, "docs/index.html", ["HTML shell", "CSS + render script"], fill=(1.0, 0.98, 0.94))

    c.box(54, 314, 142, 76, "docs/content.json", ["Metadata + nav", "Theme + page copy", "Analytics config"], fill=(0.97, 0.97, 1.0))
    c.box(236, 314, 142, 76, "Rendered Sections", ["Hero, About, Work", "Writing, Contact", "Client-side DOM"], fill=(0.95, 0.99, 1.0))
    c.box(416, 314, 142, 76, "Static Assets", ["docs/assets/image.jpg", "Publication Markdown", "Directly served"], fill=(1.0, 0.96, 0.97))

    # Arrows
    c.arrow(174, 459, 220, 459)
    c.arrow(362, 459, 408, 459)
    c.arrow(483, 430, 483, 390)
    c.arrow(408, 358, 378, 358)
    c.arrow(196, 358, 236, 358)
    c.arrow(125, 430, 125, 390)

    c.text(54, 258, "Runtime Flow", size=15, font="F2")
    flow = [
        "1. Browser loads docs/index.html from GitHub Pages.",
        "2. The script fetches ./content.json with cache disabled.",
        "3. JSON data is escaped and injected into predefined section roots.",
        "4. Image assets and Markdown publication pages are served as static files.",
    ]
    c.multiline(54, 238, flow, size=10.5, leading=15)

    c.text(54, 158, "Deployment Model", size=15, font="F2")
    deploy = [
        "Publish the docs/ folder with GitHub Pages. Content updates usually happen in",
        "docs/content.json. Longer articles can live as Markdown pages under docs/publications/.",
    ]
    c.multiline(54, 138, deploy, size=10.5, leading=15)

    c.text(54, 48, "Source note: generated from the current workspace repository layout.", size=8.5, color=(0.45, 0.48, 0.54))

    stream = "\n".join(c.ops).encode("latin-1")
    objects = []

    def add(obj):
        objects.append(obj)
        return len(objects)

    catalog_id = add("<< /Type /Catalog /Pages 2 0 R >>")
    pages_id = add("<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    page_id = add(
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>"
    )
    font_regular_id = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    font_bold_id = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    content_id = add(f"<< /Length {len(stream)} >>\nstream\n{stream.decode('latin-1')}\nendstream")

    assert (catalog_id, pages_id, page_id, font_regular_id, font_bold_id, content_id) == (1, 2, 3, 4, 5, 6)

    pdf = bytearray()
    pdf.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{idx} 0 obj\n{obj}\nendobj\n".encode("latin-1"))
    xref_at = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    pdf.extend(
        (
            "trailer\n"
            f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            "startxref\n"
            f"{xref_at}\n"
            "%%EOF\n"
        ).encode("latin-1")
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(pdf)


if __name__ == "__main__":
    build_pdf()
