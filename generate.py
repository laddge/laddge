import glob
import os
import re
import shutil

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
    reducss.auto(distdir)

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


if __name__ == "__main__":
    generate()
