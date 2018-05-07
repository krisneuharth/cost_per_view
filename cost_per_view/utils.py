import json
from datetime import datetime, time

from cost_per_view.settings import logger


class DefaultEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime) or isinstance(o, time):
            return o.isoformat()
        if isinstance(o, list) or isinstance(o, tuple):
            return ", ".join(o)

        return json.JSONEncoder.default(self, o)


def pprint(data):
    """
    Log to the console, after
    converting to json and formatting

    :param data: Any
    :return: None
    """

    s = json.dumps(
        data,
        indent=2,
        cls=DefaultEncoder
    )

    logger.info(s)
