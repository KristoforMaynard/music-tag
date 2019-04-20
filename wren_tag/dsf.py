#!/usr/bin/env python
# coding: utf-8

import mutagen.dsf

from wren_tag.file import TAG_MAP_ENTRY
from wren_tag.id3 import Id3File


class DsfFile(Id3File):
    tag_format = "DSF"
    mutagen_kls = mutagen.dsf.DSF

    def __init__(self, filename, **kwargs):
        super(DsfFile, self).__init__(filename, **kwargs)

        self.tag_map = self.tag_map.copy()
        self.tag_map.update({
            '#codec': TAG_MAP_ENTRY(getter=lambda afile, wren_tag: 'dsf',
                                    type=str),
        })