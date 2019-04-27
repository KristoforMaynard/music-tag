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
    # 'tracknumber': 99,  # not appendable
    # 'totaltracks': 99,  # not appendable
    # 'discnumber': 2,  # not appendable
    # 'totaldiscs': 2,  # not appendable
    'genre': 'test genre',
    # 'year': 2020,  # not appendable
    # 'compilation': False,  # not appendable
    # 'lyrics': "And malt does more than Milton can.To justify God's ways to man.",
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
            f.append(key, val)

        f.save()

        f = music_tag.load_file(temp_fname)

        for key, val in new_tags.items():
            if key == 'artwork':
                if fname.endswith(('.aac', '.wv')):
                    continue
                aval = [test_common.sample_tags[key], new_tags[key]]

                err_str = "{0} : {1} != {2}".format(fname,
                                                    [v.data[-3:] for v in f[key].values],
                                                    [s[-3:] for s in aval])
                assert [v.data for v in f[key].values] == aval, err_str
            else:
                avalA = [test_common.sample_tags[key], new_tags[key]]
                avalB = [', '.join([str(test_common.sample_tags[key]),
                                    str(new_tags[key])])]

                err_str = "{0} : {1} != {2}".format(fname, f[key].values, avalA)
                assert f[key].values in (avalA, avalB), err_str

        os.remove(temp_fname)

if __name__ == '__main__':
    _main()
