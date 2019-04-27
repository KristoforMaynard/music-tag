import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
import _test_common as test_common
music_tag = test_common.music_tag


with open(os.path.join(test_common.sample_dir, 'imgA.jpg'), 'rb') as fin:
    new_artwork = fin.read()


def _make_temp_fname(fname):
    return os.path.join(os.path.dirname(fname),
                        '_test_' + os.path.basename(fname))


def _main():
    for fname in test_common.sample_files:
        temp_fname = _make_temp_fname(fname)
        shutil.copy(fname, temp_fname)
        rel_fname = os.path.relpath(temp_fname, test_common.sample_dir)

        f = music_tag.load_file(temp_fname)
        for key, _ in test_common.sample_tags.items():
            del f[key]

        f.save()

        f = music_tag.load_file(temp_fname)

        for key, _ in test_common.sample_tags.items():
            if key not in ('tracknumber', 'totaltracks', 'discnumber',
                           'totaldiscs', 'artwork'):
                assert key not in f, 'key {0} exists'.format(key)

        os.remove(temp_fname)

if __name__ == '__main__':
    _main()
