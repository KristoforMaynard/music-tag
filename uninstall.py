#!/usr/bin/env python

from __future__ import print_function
import json
import os
import shutil
import sys


INSTALL_MANIFEST = '.install_manifest.json'


try:
    FileNotFoundError
except NameError:
    class FileNotFoundError(Exception):
        pass


def _main():
    verb = '-v' in sys.argv or '--verbose' in sys.argv
    verb = True

    # read the install manifest
    try:
        with open(INSTALL_MANIFEST, 'r') as fin:
            inst_manifest = json.load(fin)
    except (IOError, FileNotFoundError):
        print("Uninstall Error: Manifest not found, `make install` must be "
              "run first.", file=sys.stderr)
        return 0

    if sys.executable in inst_manifest:
        # remove the whole package directory, which now should just
        # be populated with empty subdirectories
        file_list = inst_manifest[sys.executable]['file_list']
        for fname in file_list:
            if os.path.isdir(fname):
                if verb:
                    print("Remove tree:", fname, file=sys.stderr)
                shutil.rmtree(fname, ignore_errors=False)
            elif os.path.isfile(fname):
                if verb:
                    print("Removing:", fname, file=sys.stderr)
                os.remove(fname)
            else:
                if verb:
                    print("Ignoring:", fname, "(file DNE)", file=sys.stderr)

        # remove the whole package directory, which now should just
        # be populated with empty subdirectories
        try:
            pkg_instdir = inst_manifest[sys.executable]['pkg_instdir']

            if verb:
                print("Remove tree:", pkg_instdir, file=sys.stderr)
            shutil.rmtree(pkg_instdir, ignore_errors=False)
        except OSError:
            pass

        # pretend we were never installed in this and rewrite the
        # install manifest
        del inst_manifest[sys.executable]

        with open(INSTALL_MANIFEST, 'w') as fout:
            json.dump(inst_manifest, fout, indent=2, sort_keys=True)
    elif verb:
        print("Uninstall: not in manifest for", sys.executable,
              file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(_main())

##
## EOF
##
