import os
import sys

wren_tag_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(os.path.join(wren_tag_dir))

from wren_tag import load_file

sample_dir = os.path.join(wren_tag_dir, 'sample')

f = load_file(os.path.join(sample_dir, '440Hz.m4a'))

# getting tags
print('track title:', f['title'])
assert f['title'].values == ['440Hz']
assert f['title'].value == '440Hz'
assert f['title'].first == '440Hz'

# setting tags
f['title'] = '440Hz'
f.append_tag('title', 'subtitle')
assert f['title'].values == ['440Hz', 'subtitle']
assert f['title'].value == '440Hz, subtitle'
assert f['title'].first == '440Hz'

# removing tags
del f['title']
f['title'] = '440Hz'
f.remove_tag('title')
f['title'] = '440Hz'

# album artwork
art = f['artwork']
assert art.first.mime == 'image/jpeg'
print("??", art.first.height)
assert art.first.width == 314
assert art.first.height == 314
assert art.first.depth == 24
# art.first.data  # <- b'...raw image data...'

with open(os.path.join(sample_dir, 'imgA.jpg'), 'rb') as img_in:
    f['artwork'] = img_in.read()
with open(os.path.join(sample_dir, 'imgB.jpg'), 'rb') as img_in:
    f.append_tag('artwork', img_in.read())

# thumbnails (requires Pillow)
art.first.thumbnail([64, 64])  # <- pillow image
art.first.raw_thumbnail([64, 64])  # <- b'... raw thumbnail data ...'

# saving edits
# f.save()
