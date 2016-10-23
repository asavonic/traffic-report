import PIL.Image
import PIL.ImageMath
import urllib.request
from io import BytesIO
from os import path


DEBUG_DUMP_DIR = None


def load_img_url(url):
    req = urllib.request.urlopen(url)
    data = BytesIO(req.read())
    return PIL.Image.open(data)


def load_img_file(fname):
    return PIL.Image.open(fname)


def compute_histo_RYG(img, mask):
    img = img.convert(mode='RGB')
    mask = mask.convert(mode='1')

    black = PIL.Image.new('RGB', mask.size, color=(0, 0, 0, 0))
    masked = PIL.Image.composite(img, black, mask)

    palette = PIL.Image.new('P', (1, 1))
    palette.putpalette(
        [0,   0,   0,   # black
         255, 0,   0,   # red
         255, 255, 0,   # yellow
         0,   255, 0])  # green

    quantized = masked.quantize(palette=palette)
    colors = quantized.getcolors()

    if DEBUG_DUMP_DIR is not None:
        img.save(path.join(DEBUG_DUMP_DIR, 'img.png'))
        mask.save(path.join(DEBUG_DUMP_DIR, 'mask.png'))
        black.save(path.join(DEBUG_DUMP_DIR, 'black.png'))
        masked.save(path.join(DEBUG_DUMP_DIR, 'masked.png'))
        quantized.save(path.join(DEBUG_DUMP_DIR, 'quantized.png'))
        with open(path.join(DEBUG_DUMP_DIR, 'colors.txt'), 'w') as f:
            f.write(colors.__repr__())

    r = next((c[0] for c in colors if c[1] == 1), 0)
    y = next((c[0] for c in colors if c[1] == 2), 0)
    g = next((c[0] for c in colors if c[1] == 3), 0)

    return r, y, g
