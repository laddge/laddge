import glob
import os
import re
import shutil
import subprocess

import fontTools.subset
import reducss
import sass
from bs4 import BeautifulSoup


def generate():
    # settings
    srcdir = "./src"
    distdir = "./dist"

    # clean
    if os.path.isfile(distdir):
        os.remove(distdir)
    if os.path.isdir(distdir):
        shutil.rmtree(distdir)

    # copy
    files = glob.glob(os.path.join(srcdir, "**"), recursive=True)
    for path in files:
        saveto = os.path.join(distdir, re.sub(f"^{srcdir}/?", "", path))
        os.makedirs(os.path.dirname(saveto), exist_ok=True)
        if os.path.isfile(path):
            shutil.copy(path, saveto)

    # build css
    sass.compile(
        dirname=(os.path.join(srcdir, ".ignore/scss"), os.path.join(distdir, "css")),
        output_style="compressed",
    )

    # reduce css
    with open(os.path.join(srcdir, "index.html")) as f:
        index_html = f.read()
    with open(os.path.join(srcdir, ".ignore/card.html")) as f:
        card_html = f.read()
    with open(os.path.join(distdir, "css/bootstrap.custom.css")) as f:
        cssstr = f.read()
    with open(os.path.join(distdir, "css/main.css"), "w") as f:
        f.write(reducss.reduce(index_html, cssstr))
    with open(os.path.join(distdir, "css/card.css"), "w") as f:
        f.write(reducss.reduce(card_html, cssstr))
    os.remove(os.path.join(distdir, "css/bootstrap.custom.css"))

    # subset fonts
    htmls = glob.glob(os.path.join(distdir, "**/*.html"), recursive=True)
    subset_chars = ""
    for html in htmls:
        with open(html) as f:
            htmlstr = f.read()
        soup = BeautifulSoup(htmlstr, "html.parser")
        text = "".join([el.get_text(strip=True) for el in soup.select(".mplus2")])
        subset_chars += text
    subset_chars = "".join(set(subset_chars))
    font = "MPLUS2-Bold.ttf"
    output = font.replace(".ttf", ".woff2").lower()
    args = []
    args.append(os.path.join(srcdir, f"fonts/.ignore/{font}"))
    args.append(f"--text={subset_chars}")
    args.append("--flavor=woff2")
    args.append("--output-file=" + os.path.join(distdir, f"fonts/{output}"))
    os.makedirs(os.path.join(distdir, "fonts"), exist_ok=True)
    fontTools.subset.main(args)

    # cache buster
    commit_id = subprocess.run(
        "git rev-parse --short HEAD", shell=True, capture_output=True, text=True
    ).stdout.strip("\n")
    for html in htmls:
        with open(html) as f:
            htmlstr = f.read()
        htmlstr = htmlstr.format(commit_id=commit_id)
        with open(html, "w") as f:
            f.write(htmlstr)
    csspath = os.path.join(distdir, "css/main.css")
    with open(csspath) as f:
        cssstr = f.read()
    with open(csspath, "w") as f:
        f.write(cssstr.replace(".woff2", f".woff2?{commit_id}"))


if __name__ == "__main__":
    generate()
