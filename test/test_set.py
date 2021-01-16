import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
import _test_common as test_common
music_tag = test_common.music_tag


with open(os.path.join(test_common.sample_dir, 'imgA.jpg'), 'rb') as fin:
    new_artwork = fin.read()

new_tags = {
    'tracktitle': 'test title',
    'artist': 'test artist',
    'album': 'test album',
    'albumartist': 'test album artist',
    'composer': 'test composer',
    'tracknumber': 99,
    'totaltracks': 99,
    'discnumber': 2,
    'totaldiscs': 2,
    'genre': 'test genre',
    'year': '2020',
    'compilation': False,
    # 'lyrics': "And malt does more than Milton can.To justify God's ways to man.",
    'isrc': 'US-AAA-01-12345',
    'comment': 'test comment',
    'artwork': new_artwork,
}

def _make_temp_fname(fname):
    return os.path.join(os.path.dirname(fname),
                        '_test_' + os.path.basename(fname))


def _main():
    for fname in test_common.sample_files:
        temp_fname = _make_temp_fname(fname)
        shutil.copy(fname, temp_fname)
        rel_fname = os.path.relpath(temp_fname, test_common.sample_dir)

        f = music_tag.load_file(temp_fname)
        for key, val in new_tags.items():
            f[key] = val

        f.save()

        f = music_tag.load_file(temp_fname)
        test_common.check_tags(f, rel_fname, new_tags)

        os.remove(temp_fname)

if __name__ == '__main__':
    _main()
