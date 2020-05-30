# music-tag

music-tag is a library for editing audio metadata with an interface
that does not depend on the underlying file format. In other words, editing
mp3 files shouldn not be any different than flac, m4a, ... This library is
just a layer on top of [mutagen](https://mutagen.readthedocs.io/en/latest/),
which does all the heavy lifting.

## Formats

The following file formats are actively tested.

- ``aac``
- ``aiff``
- ``dsf``
- ``flac``
- ``m4a``
- ``mp3``
- ``ogg``
- ``opus``
- ``wav``
- ``wv``

## Keys

Metadata is available using a dictionary-like interface with the following keys.
Keys are not case sensitive and can contain arbitrary whitespace, '-', and '_'
characters. In other words, ``Album Artist``, ``album-artist``, and
``album_artist`` are all synonyms for ``albumartist``. Also, ``disk`` is synonymous with ``disc``.

- ``album``
- ``albumartist``
- ``artist``
- ``artwork``
- ``comment``
- ``compilation``
- ``composer``
- ``discnumber``
- ``genre``
- ``lyrics``
- ``totaldiscs``
- ``totaltracks``
- ``tracknumber``
- ``tracktitle``
- ``year``

## Examples

### Reading tags

``` python
import music_tag

f = music_tag.load_file("music-tag/sample/440Hz.m4a")

# dict access returns a MetadataItem
title_item = f['title']

# MetadataItems keep track of multi-valued keys
title_item.values  # -> ['440Hz']

# A single value can be extracted
title_item.first  # -> '440Hz'
title_item.value  # -> '440Hz'

# MetadataItems can also be cast to a string
str(title_item)  # -> '440Hz'
```

### Setting tags

``` python
# tags can be set as if the file were a dictionary
f['title'] = '440Hz'

# additional values can be appended to the tags
f.append_tag('title', 'subtitle')
title_item.values  # -> ['440Hz', 'subtitle']
title_item.first  # -> '440Hz'
title_item.value  # -> '440Hz, subtitle'
str(title_item)  # -> '440Hz, subtitle'
```

### Removing tags

``` python
del f['title']
f.remove_tag('title')
```

### Album artwork

Album artwork is wrapped in an object that keeps track of some of the
extra metadata associated with images. Note that some album art functionality
requires the Pillow (modern day PIL) library.

``` python
# get artwork
art = f['artwork']

# Note: `art` is a MetadataItem. Use ``art.value`` if there is
#       only one image embeded in the file. This will raise a
#       ValueError if there is more than one image. You can also
#       use ``art.first``, or iterate through ``art.values``.

art.first.mime  # -> 'image/jpeg'
art.first.width  # -> 1280
art.first.height  # -> 1280
art.first.depth  # -> 24
art.first.data  # -> b'... raw image data ...'

# set artwork
with open('music_tag/test/sample/imgA.jpg', 'rb') as img_in:
    f['artwork'] = img_in.read()
with open('music_tag/test/sample/imgB.jpg', 'rb') as img_in:
    f.append_tag('artwork', img_in.read())

# Make a thumbnail (requires Pillow)
art.first.thumbnail([64, 64])  # -> pillow image
art.first.raw_thumbnail([64, 64])  # -> b'... raw thumbnail data ...'
```

### Saving tags

``` python
# finally, you can bounce the edits to disk
f.save()
```

### Skipping Type Normalization

By default, tags are validated and normalized. For instance, track numbers
and years are return as integers. Some tag formats store everything as strings
to enable things like leading zeros in tracknumbers (i.e., track '01'). I think
this is ugly, but you can use the file object's ``raw`` property if you like
this kind of thing.

``` python
f.raw['tracknumber'] = '01'
f.raw['tracknumber'].value  # -> '01'
```
