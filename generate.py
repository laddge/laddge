import glob
import os
import re
import shutil


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


if __name__ == "__main__":
    generate()
