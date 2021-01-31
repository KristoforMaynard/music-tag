import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import _test_common as test_common
music_tag = test_common.music_tag


def _main():
    for fname in test_common.sample_files:
        rel_fname = os.path.relpath(fname, test_common.sample_dir)
        f = music_tag.load_file(fname)

        f['album artist'] = 'Brian'
        assert str(f.resolve('album artist')) == 'Brian'

        f['artist'] = 'Brian'
        del f['album artist']
        f['compilation'] = False
        assert str(f.resolve('album artist')) == 'Brian'

        f['compilation'] = True
        assert str(f.resolve('album artist')) == 'Various Artists'


        del f['compilation']
        f['album artist'] = 'Various Artists'
        assert f.resolve('compilation')

        f['album artist'] = 'Brian'
        assert not f.resolve('compilation')


if __name__ == '__main__':
    _main()
