import json


class Spot(object):
    # "01/02/2016","8:30 AM","TEST001H",120.50,100

    __slots__ = [
        'date', 'time',
        'creative', 'spend', 'views',
        'rotation'
    ]

    def __str__(self):
        return json.dumps({
            'date': self.date,
            'time': self.time,
            'creative': self.creative,
            'spend': self.spend,
            'views': self.views,
            'rotation': self.rotation
        })


class Metadata(object):
    __slots__ = [
        'rotations_names',
        'creative_names',
        'spot_days'
    ]

