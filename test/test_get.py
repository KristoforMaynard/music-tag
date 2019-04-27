import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import _test_common as test_common
music_tag = test_common.music_tag


def _main():
    for fname in test_common.sample_files:
        rel_fname = os.path.relpath(fname, test_common.sample_dir)
        f = music_tag.load_file(fname)
        test_common.check_tags(f, rel_fname, test_common.sample_tags)

if __name__ == '__main__':
    _main()
