# this file is used for building a Windows exe file.
# use as following:
# python setup.py py2exe

from distutils.core import setup
import py2exe
import sys
import glob
import os

# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")


def resource_files():
    v = []
    for dir in glob.glob("resources/*"):
        if os.path.isdir(dir):
            v.append((dir, glob.glob(os.path.join(dir, "*"))))
    return v

icon = os.path.join(os.path.join("resources","images"), "notes.ico"),

options = { "compressed"   : 1,
            "optimize"     : 2,
            "ascii"        : 1,
            "bundle_files" : 1
          }

setup(
      name         = "readMusic!",
      version      = "0.2",
      author       = "Francisco Dibar",
      author_email = "frandibar@gmail.com",
      url          = "http://code.google.com/p/readmusicalnotes",
      data_files   = resource_files(),
#     options      = {"py2exe": options},
#     zipfile      = None, # append zip-archive to the executable
      windows      = [{"script"         : "src/readMusic.py"#, 
#                      "icon_resources" : [(1, icon)]
                      }]
)
