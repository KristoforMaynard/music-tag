#!/usr/bin/env python
# coding: utf-8

# asf is a microsoft format (wma, wmv, etc.)

import mutagen.asf

from music_tag.file import AudioFile


class AsfFile(AudioFile):
    tag_format = "ASF"
    mutagen_kls = mutagen.asf.ASF

    def __init__(self, filename, **kwargs):
        raise NotImplementedError("ASF format not implemented")
