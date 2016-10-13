import PIL.Image
import PIL.ImageMath
import urllib.request


def load_img_url(url):
    req = urllib.request.urlopen(url)
    data = req.read()
    return PIL.Image.fromarray(data)


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

    return colors[1][0], colors[2][0], colors[3][0]
