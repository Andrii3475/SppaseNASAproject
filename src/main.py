"""Точка входу."""

import os
import sys

from panda3d.core import loadPrcFileData

loadPrcFileData("", "load-display pandagl")
loadPrcFileData("", "audio-library-name null")  # див. пункт про звук нижче

# У зібраному застосунку ресурси лежать поруч з програмою
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

from app import App


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()