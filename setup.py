#!/usr/bin/env python

from __future__ import print_function
from distutils.core import setup
from glob import glob
import io
import json
import os
import re
import shutil
import sys

try:
    import setuptools
except ImportError:
    pass


INSTALL_MANIFEST = '.install_manifest.json'
RECORD_FNAME = '.temp_install_list.txt'


def get_version(init_py):
    with io.open(init_py, 'r', encoding="utf-8") as f:
        quoted_str = r"((?<![\\])(?:'''|\"\"\"|\"|'))((?:.(?!(?<![\\])\1))*.?)\1"
        ver_re = r"__version__\s*=\s*" + quoted_str
        for line in f:
            m = re.search(ver_re, line)
            if m:
                return m.groups()[1]
    return 'x.x.x'

version = get_version(os.path.join('music_tag', '__init__.py'))
url = "https://github.com/KristoforMaynard/music-tag"
download_url = "{0}/archive/{1}.zip".format(url, version)

pkgs = ['music_tag',
       ]
scripts = glob(os.path.join('scripts', '*'))

cmdclass = {}


def _main():
    # prepare a cute hack to get an `uninstall`
    desired_record_fname = ''
    if 'install' in sys.argv:
        try:
            i = sys.argv.index('--record')
            sys.argv.pop(i)
            desired_record_fname = sys.argv[i]
            sys.argv.pop(i)
        except ValueError:
            pass
        except IndexError:
            print("error: --record must be followed by a filename")
            sys.exit(4)
        sys.argv += ['--record', RECORD_FNAME]

    with open("README.md", "r") as fh:
        long_description = fh.read()

    setup(name='music-tag',
          version=version,
          description='Simple interface to edit audio file metadata',
          long_description=long_description,
          long_description_content_type="text/markdown",
          author='Kristofor Maynard',
          author_email='kristofor.maynard@gmail.com',
          license='MIT',
          url=url,
          download_url=download_url,
          keywords=['music', 'metadata', 'id3'],
          install_requires=['mutagen'],
          extras_require={
              'artwork': 'Pillow',
          },
          packages=pkgs,
          cmdclass=cmdclass,
          scripts=scripts,
          zip_safe=True,
          classifiers=(
              "Programming Language :: Python :: 3",
              "Programming Language :: Python :: 3.3",
              "Programming Language :: Python :: 3.4",
              "Programming Language :: Python :: 3.5",
              "Programming Language :: Python :: 3.6",
              "Programming Language :: Python :: 3.7",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
          ),
    )

    # if installed, store list of installed files in a json file - this
    # manifest is used to implement an uninstall
    if os.path.isfile(RECORD_FNAME):
        try:
            with open(INSTALL_MANIFEST, 'r') as fin:
                inst_manifest = json.load(fin)
        except (IOError, FileNotFoundError):
            inst_manifest = dict()

        with open(RECORD_FNAME) as fin:
            file_list = [line.strip() for line in fin]

        init_pys = [s for s in file_list if '__init__.py' in s or s.endswith('.egg')]
        pkg_instdir = os.path.dirname(min(init_pys, key=len))

        inst_manifest[sys.executable] = dict(pkg_instdir=pkg_instdir,
                                             file_list=file_list)

        with open(INSTALL_MANIFEST, 'w') as fout:
            json.dump(inst_manifest, fout, indent=2, sort_keys=True)

        if desired_record_fname:
            shutil.copy(RECORD_FNAME, desired_record_fname)
        os.remove(RECORD_FNAME)


if __name__ == "__main__":
    _main()

##
## EOF
##
