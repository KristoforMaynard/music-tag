#!/usr/bin/env python
# This whole module is just id3 tag part of MusicBrainz Picard
# The idea is to get Musicbrainz's layer on top of mutagen without
# dependancies (like qt)

import logging

import mutagen

from wren_tag import file
from wren_tag import util
from wren_tag import aac
from wren_tag import aiff
from wren_tag import apev2
from wren_tag import asf
from wren_tag import dsf
from wren_tag import flac
from wren_tag import id3
from wren_tag import mp4
from wren_tag import smf
from wren_tag import vorbis

from wren_tag.file import Artwork, MetadataItem, NotAppendable, AudioFile


__version__ = """0.0.2"""


logger = logging.getLogger("wren")
log = logger


def _subclass_spider_dfs(kls, _lst=None):
    if _lst is None:
        _lst = []
    for sub in kls.__subclasses__():
        _subclass_spider_dfs(sub, _lst=_lst)
    _lst.append(kls)
    return _lst


def load_file(filename, err='raise'):
    filename = os.path.expanduser(os.path.expandvars(filename))
    mfile = mutagen.File(filename, easy=False)
    ret = None

    for kls in _subclass_spider_dfs(file.AudioFile):
        # print("checking against:", kls, kls.mutagen_kls)
        if kls.mutagen_kls is not None and isinstance(mfile, kls.mutagen_kls):
            ret = kls(filename, _mfile=mfile)
            break

    if ret is None and err == 'raise':
        raise NotImplementedError("Mutagen type {0} not implemented"
                                  "".format(type(mfile)))

    return ret

__all__ = ['file', 'util',
           'aac', 'aiff', 'apev2', 'asf', 'dsf', 'flac',
           'id3', 'mp4', 'smf', 'vorbis',
           'logger', 'log',
           'Artwork', 'MetadataItem', 'NotAppendable',
           'AudioFile',
           'load_file',
           ]

##
## EOF
##
