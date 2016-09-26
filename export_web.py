#!/usr/bin/env python

import sys
sys.path.append('/usr/share/inkscape/extensions')
import inkex
import os
import subprocess


class PNGExport(inkex.Effect):
    def __init__(self):
        """init the effetc library and get options from gui"""
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--path", action="store", type="string", dest="path", default="~/webicons", help="")

    def effect(self):
        dirname = os.path.expanduser(self.options.path)
        dirname = os.path.expandvars(dirname)
        dirname = os.path.abspath(dirname)
        if dirname[-1] != os.path.sep:
            dirname += os.path.sep
        if not os.path.exists(os.path.join(dirname)):
            os.makedirs(os.path.join(dirname))

        curfile = self.args[-1]

        for fs in [(92,92), (152,152),(48,48)]:
            self.exportToPng(curfile, dirname, fs)


    def exportToPng(self, svg_path, dirname, size):
        w, h = size
        output_filename = os.path.join(dirname, "icon-{}x{}.png".format(w,h))
        command = "inkscape -C -w {w} -h {h} -e \"{}\" \"{}\"".format(output_filename, svg_path, w=w, h=h)
        print(command)
        inkex.errormsg(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()



if __name__ == "__main__":
    e = PNGExport()
    e.affect()
    e.close()
