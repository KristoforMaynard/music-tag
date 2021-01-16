import os
import sys

music_tag_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(os.path.join(music_tag_dir, '..'))

from music_tag import load_file

sample_dir = os.path.join(music_tag_dir, 'sample')

files = [
    load_file(os.path.join(sample_dir, '440Hz.aac')),
    load_file(os.path.join(sample_dir, '440Hz.aiff')),
    load_file(os.path.join(sample_dir, '440Hz.dsf')),
    load_file(os.path.join(sample_dir, '440Hz.flac')),
    load_file(os.path.join(sample_dir, '440Hz.m4a')),
    load_file(os.path.join(sample_dir, '440Hz.mp3')),
    load_file(os.path.join(sample_dir, '440Hz.ogg')),
    load_file(os.path.join(sample_dir, '440Hz.opus')),
    load_file(os.path.join(sample_dir, '440Hz_id3.wav')),
    load_file(os.path.join(sample_dir, '440Hz.wv')),
]

with open(os.path.join(sample_dir, 'imgA.jpg'), 'rb') as fin:
    img1 = fin.read()

with open(os.path.join(sample_dir, 'imgB.jpg'), 'rb') as fin:
    img2 = fin.read()

set_vals = {
    'tracktitle': 'NEW TITLE',
    'artist': 'NEW ARTIST',
    'album': 'NEW ALBUM',
    'albumartist': 'NEW ALBUM ARTIST',
    'composer': 'NEW COMPOSER',
    'tracknumber': 900,
    'totaltracks': 910,
    'discnumber': 920,
    'totaldiscs': 930,
    'genre': 'NEW GENRE',
    'year': 9991,
    'compilation': False,
    'lyrics': 'NEW LYRICS',
    'comment': 'NEW COMMENT',
    'artwork': [img1, img2],
}

append_vals = {
    'tracktitle': 'APPENDED TITLE',
    'artist': 'APPENDED ARTIST',
    'album': 'APPENDED ALBUM',
    'albumartist': 'APPENDED ALBUM ARTIST',
    'composer': 'APPENDED COMPOSER',
    # 'tracknumber': 900,
    # 'totaltracks': 910,
    # 'discnumber': 920,
    # 'totaldiscs': 930,
    'genre': 'APPENDED GENRE',
    # 'year': 9991,
    # 'compilation': False,
    'lyrics': 'APPENDED LYRICS',
    'comment': 'APPENDED COMMENT',
    'artwork': img2,
}


for f in files:
    for key in f.tag_map.keys():
        try:
            print("{0} {1}: {2}".format(f.filename, key, f[key]))
        except NotImplementedError as e:
            print(str(e))

for f in files:
    for key in f.tag_map.keys():
        try:
            print("{0} {1}: {2}".format(f.filename, key, f.resolve(key)))
        except NotImplementedError as e:
            print(str(e))

for f in files:
    for key, val in set_vals.items():
        try:
            if key == 'artwork':
                print("{0} {1}: ({2}) -> ({3})".format(f.filename, key,
                                                       len(f[key].values),
                                                       len(val)))
            else:
                print("{0} {1}: {2} -> {3}".format(f.filename, key, f[key], val))
            f[key] = val
            f.mfile.save()
        except NotImplementedError as e:
            print('-> exception ->', str(e))

for f in files:
    for key, val in append_vals.items():
        try:
            if key == 'artwork':
                pass
            else:
                print("{0} {1}: {2} -> {3}".format(f.filename, key, f[key], val))
            f.append_tag(key, val)
            f.mfile.save()
        except NotImplementedError as e:
            print('-> exception ->', str(e))


# f = load_file(os.path.join(sample_dir, '14235-AAC-20K-FTD.aac'))
# import IPython
# IPython.embed()
