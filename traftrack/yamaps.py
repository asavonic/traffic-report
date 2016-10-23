import image


def make_map_url(ty, coord, area_size, zoom):
    return \
        ('https://static-maps.yandex.ru/1.x/?lang=ru_RU'
         '&ll={lat}%2C{lon}'
         '&z={zoom}&l={ty}&size={size_x},{size_y}'
         ).format(
            ty=ty,
            lat=coord[0], lon=coord[1],
            size_x=area_size[0], size_y=area_size[1],
            zoom=zoom)


traffic_levels = [
    'AllGreen',   # no traffic at all
    'Minor',      # no red, just a moderate amount of yellow
    'BeCareful',  # yellow, a few red segments
    'NoWay',      # many red segments
    'GetTheHellOutOfHere'  # almost all red
]


def decide_traffic_level(red, yellow, green):
    '''Translate traffic colors given in percents to the one of the
    `traffic_levels` constants

    '''

    if red < 5:
        # AllGreen or Minor
        if yellow < 10:
            return 'AllGreen'
        else:
            return 'Minor'
    else:
        if red < 15:
            return 'BeCareful'
        elif red < 30:
            return 'NoWay'
        else:
            return 'GetTheHellOutOfHere'
    assert False, \
        'Cannot decide traffic for RYG: {}%, {}%, {}%'.format(
            red, yellow, green)


def get_traffic(mask_path, coord, area_size, zoom):
    # area_name = client['area_name']

    map_img = image.load_img_url(make_map_url('trf', coord, area_size, zoom))
    mask_img = image.load_img_file(mask_path)

    red, yellow, green = image.compute_histo_RYG(map_img, mask_img)
    total = red + yellow + green

    red = 100 * red / total
    yellow = 100 * yellow / total
    green = 100 * green / total

    return decide_traffic_level(red, yellow, green)
