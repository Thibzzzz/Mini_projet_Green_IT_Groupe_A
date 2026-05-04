"""Generate minified CSS/JS assets for production-like delivery."""
from pathlib import Path

from rcssmin import cssmin
from rjsmin import jsmin


ROOT = Path(__file__).resolve().parent
STATIC = ROOT.parent / "frontend" / "static"


def minify_css():
    for css_file in (STATIC / "css").glob("*.css"):
        if css_file.name.endswith(".min.css"):
            continue
        content = css_file.read_text(encoding="utf-8")
        target = css_file.with_name(css_file.stem + ".min.css")
        target.write_text(cssmin(content), encoding="utf-8")


def minify_js():
    for js_file in (STATIC / "js").glob("*.js"):
        if js_file.name.endswith(".min.js"):
            continue
        content = js_file.read_text(encoding="utf-8")
        target = js_file.with_name(js_file.stem + ".min.js")
        target.write_text(jsmin(content), encoding="utf-8")


if __name__ == "__main__":
    minify_css()
    minify_js()
    print("Minified assets generated.")
