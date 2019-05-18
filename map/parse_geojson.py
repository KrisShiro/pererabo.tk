import json
from .models import Place


def parse(filename):
    data = json.load(open(filename, 'r'))
    print(data.keys())
    print(data['features'][0])
    unique_data = dict()

    mask = {
        '#ed4543': 1,  # ok
        '#177bc9': 2,  # ok
        '#1bad03': 4,  # ok
        '#595959': 8,  # ok
    }

    for obj in data['features']:
        geom = obj['geometry']
        props = obj['properties']
        coords = tuple(geom['coordinates'])
        if coords not in unique_data:
            unique_data[coords] = {
                'address': props['description'],
                'type': mask[props['marker-color']]
            }
        else:
            unique_data[coords]['type'] |= mask[props['marker-color']]

    for key in unique_data:
        y,x = key
        Place.objects.create(
            address=unique_data[key]['address'],
            coordinate_x=x,
            coordinate_y=y,
            type_mask=unique_data[key]['type']
        )
