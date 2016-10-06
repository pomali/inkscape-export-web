#!/usr/bin/env python

import sys
sys.path.append('/usr/share/inkscape/extensions')
import inkex
import os
import operator
import subprocess

icon_sizes = { 
        'android': [48*i for i in range(1,5)], 
        'windows': [16,32,48,256],
        'metro': [30,50,150],
        'macos': [1024,512,256,128,64,32,16],
        'gnome': [24,48,96],
        'ios6': [57,114,1024,72,144,512],
        'ios8': [120,180,1024,120,80, 152,76,58,29],
        'windowsphone': [62,173,99,200],
        }

all_sizes = list(set(reduce(operator.add, icon_sizes.values())))

class PNGExport(inkex.Effect):
    def __init__(self):
        """init the effetc library and get options from gui"""
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--path", action="store", type="string", dest="path", default="./webicons", help="")

    def effect(self):
        dirname = os.path.expanduser(self.options.path)
        dirname = os.path.expandvars(dirname)
        dirname = os.path.abspath(dirname)
        if dirname[-1] != os.path.sep:
            dirname += os.path.sep
        if not os.path.exists(os.path.join(dirname)):
            os.makedirs(os.path.join(dirname))

        curfile = self.args[-1]

        for fs in all_sizes:
            self.exportToPng(curfile, dirname, fs)


    def exportToPng(self, svg_path, dirname, size):
        filename = "icon-{}x{}.png".format(size,size)
        output_filename = os.path.join(dirname, filename)
        command = "inkscape -C -w {w} -h {h} -e \"{}\" \"{}\"".format(output_filename, svg_path, w=size, h=size)
        inkex.errormsg('<link rel="icon" href="{}" sizes="{w}x{h}">'.format(filename, w=size, h=size))
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()



if __name__ == "__main__":
    e = PNGExport()
    e.affect()
    #e.close()
