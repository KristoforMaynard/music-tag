#!/usr/bin/env python
# pylint: disable=unused-import

from __future__ import print_function
import os
import sys

do_exit = False

if '--version' in sys.argv or 'version' in sys.argv:
    import music_tag
    print("Version: {0}".format(music_tag.__version__), file=sys.stderr)
    exit_code = 0
    do_exit = True

if do_exit:
    sys.exit(exit_code)
else:
    import music_tag
    from music_tag import load_file

##
## EOF
##
