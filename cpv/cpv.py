import csv
import logging
import json

from collections import defaultdict
from datetime import datetime, time

from copy import deepcopy

# Settings
ROTATIONS_DATA = '../data/rotations.csv'
SPOTS_DATA = '../data/spots.csv'

DATE_FMT = "%m/%d/%Y"
TIME_FMT = "%I:%M %p"
DATE_TIME_FMT = " ".join(
    [DATE_FMT, TIME_FMT]
)

BASE_STR = " - "

# Setup our results
ROOT_KEY = 'cpv'
CREATIVE = "creative"
ROTATION = "rotation"
DAY = "day"
ROTATION_BY_DAY = "rotation_by_day"
ROTATION_BY_CREATIVE_BY_DAY = "rotation_by_creative_by_day"

# Logging
logging.basicConfig(
    format='%(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger()


class DefaultEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime) or isinstance(o, time):
            return o.isoformat()
        if isinstance(o, list) or isinstance(o, tuple):
            return ", ".join(o)

        return json.JSONEncoder.default(self, o)


class Spot(object):
    __slots__ = ['date', 'time', 'creative', 'spend', 'views', 'rotation']

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
    __slots__ = ['rotations_names', 'creative_names', 'spot_days']


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


def get_rotations_data(meta):
    """
    Read up the rotations file
    Store the rotations key by time hour ranges
    Save the names in meta

    :param meta: Metadata object
    :return: dict, Metadata object
    """

    logger.info('Reading CSV: `%s`' % ROTATIONS_DATA)

    with open(ROTATIONS_DATA) as f:
        reader = csv.reader(f)

        # Pop the header
        header = next(reader)
        logger.info('CSV header: %s' % header)

        # Go through the rotations file,
        # pull out the name and time ranges
        rotations = {}
        rotations_names = set()

        for line in reader:
            if not all(line):
                logger.error('Bad line: %s' % line)
                continue

            # Get time range for this rotation
            dt_start = datetime.strptime(line[0], TIME_FMT).time()
            dt_end = datetime.strptime(line[1], TIME_FMT).time()

            # Get rotation name
            v = line[2]

            # Save for later
            rotations_names.add(v)

            # Save the key and name, for quicker lookup later
            for k in range(dt_start.hour, dt_end.hour + 1):
                key = str(k)

                if key in rotations:
                    # We've seen this before
                    values = rotations[key]

                    if isinstance(values, list):
                        values.append(v)

                        # Re-save with the update
                        rotations[key] = values
                else:
                    # Have not seen this before
                    rotations[key] = [v]

        # Save for later
        meta.rotations_names = rotations_names

        return rotations, meta


def get_spots_data(rotations, meta):
    """
    Read up the spots file
    Convert them to Spot objects
    Save some information in meta


    :param rotations: dict
    :param meta: Metadata
    :return: list of Spots, Metadata
    """

    logger.info('Reading CSV: `%s`' % SPOTS_DATA)

    with open(SPOTS_DATA) as f:
        reader = csv.reader(f)

        # Pop the header
        header = next(reader)
        logger.info('CSV header: %s' % header)

        # Things to track
        spots = []
        creative_names = set()
        spot_days = set()

        for line in reader:
            if not all(line):
                logger.error('Bad line: %s' % line)
                continue

            # Create spot
            spot = Spot()

            # Convert strings to dt
            dt_aired = datetime.strptime(
                "%s %s" % (line[0], line[1]),
                DATE_TIME_FMT
            )

            # Save the date in the YYYY-MM-DD
            spot.date = str(dt_aired.date())
            spot.time = str(dt_aired.time())

            spot.creative = line[2]
            spot.spend = float(line[3])
            spot.views = int(line[4])

            # Save for later:
            creative_names.add(spot.creative)
            spot_days.add(spot.date)

            # Do the lookup for the rotation
            rotation = rotations.get(
                str(dt_aired.hour), ['Other']
            )

            # If spot is in two rotations,
            # duplicate the spot for each rotation
            for r in rotation:
                spot = deepcopy(spot)
                spot.rotation = r

                # Save it
                spots.append(spot)

        # Save for later
        meta.creative_names = creative_names
        meta.spot_days = spot_days

        return spots, meta


def calc_cpv(spend, views):
    """
    Use spend and views to calculate
    the Cost Per View metric

    :param spend: float
    :param views: int
    :return: float
    """

    try:
        cost = round(float(spend / views), 2)
    except ZeroDivisionError:
        cost = 0

    return cost


def filter_sum(fx, spots):
    """
    Helper method to find spots matching
    the filter criteria

    :param fx: lambda
    :param spots: list of Spots
    :return: tuple (spend, views)
    """

    sum_spend = 0
    sum_views = 0

    for spot in filter(fx, spots):
        sum_spend += float(spot.spend)
        sum_views += float(spot.views)

    return sum_spend, sum_views


def cpv_by_creative(spots, meta, results):
    """
    Filter spots and calculate CPV by creative

    :param spots: list
    :param meta: Metadata object
    :param results: dict
    :return: None
    """

    for name in meta.creative_names:
        fx = lambda x: x.creative == name
        costs, views = filter_sum(fx, spots)
        cpv = calc_cpv(costs, views)

        if cpv:
            results[ROOT_KEY][CREATIVE][name] = cpv


def cpv_by_rotation(spots, meta, results):
    """
    Filter spots and calculate CPV by rotation

    :param spots: list
    :param meta: Metadata object
    :param results: dict
    :return: None
    """

    for rotation in meta.rotations_names:
        fx = lambda x: x.rotation == rotation
        costs, views = filter_sum(fx, spots)
        cpv = calc_cpv(costs, views)

        if cpv:
            results[ROOT_KEY][ROTATION][rotation] = cpv


def cpv_by_day(spots, meta, results):
    """
    Filter spots and calculate CPV by day

    :param spots: list
    :param meta: Metadata object
    :param results: dict
    :return: None
    """

    for day in meta.spot_days:
        fx = lambda x: x.date == day
        costs, views = filter_sum(fx, spots)
        cpv = calc_cpv(costs, views)

        if cpv:
            results[ROOT_KEY][DAY][day] = cpv


def cpv_by_rotation_by_day(spots, meta, results):
    """
    Filter spots and calculate CPV by rotation by day

    :param spots: list
    :param meta: Metadata object
    :param results: dict
    :return: None
    """

    for rotation in meta.rotations_names:
        for day in meta.spot_days:
            DIM_KEY = BASE_STR.join([rotation, day])

            fx = lambda x: x.rotation == rotation and x.date == day
            costs, views = filter_sum(fx, spots)
            cpv = calc_cpv(costs, views)

            if cpv:
                results[ROOT_KEY][ROTATION_BY_DAY][DIM_KEY] = cpv


def cpv_by_rotation_by_creative_by_day(spots, meta, results):
    """
    Filter spots and calculate CPV by rotation by creative by day

    :param spots: list
    :param meta: Metadata object
    :param results: dict
    :return: None
    """

    for rotation in meta.rotations_names:
        for creative in meta.creative_names:
            for day in meta.spot_days:
                DIM_KEY = BASE_STR.join([rotation, creative, day])

                fx = lambda x: x.rotation == rotation and x.creative == creative and x.date == day
                costs, views = filter_sum(fx, spots)
                cpv = calc_cpv(costs, views)

                if cpv:
                    results[ROOT_KEY][ROTATION_BY_CREATIVE_BY_DAY][DIM_KEY] = cpv


def calculate(spots, meta):
    """
    Go through spots and combine with
    metadata in order to calculate the
    desired CPV metric in several dimensions

    :param spots: list of Spots
    :param meta: Metadata object
    :return: results dict
    """

    # Prepare our results
    results = {ROOT_KEY: {}}
    for key in [CREATIVE, ROTATION, DAY, ROTATION_BY_DAY, ROTATION_BY_CREATIVE_BY_DAY]:
        results[ROOT_KEY][key] = defaultdict(dict)

    # 1: CPV by creative
    cpv_by_creative(spots, meta, results)

    # 2: CPV by rotation
    cpv_by_rotation(spots, meta, results)

    # 3: CPV by day
    cpv_by_day(spots, meta, results)

    # 4: CPV by rotation by day
    cpv_by_rotation_by_day(spots, meta, results)

    # 5: CPV by rotation by creative by day
    cpv_by_rotation_by_creative_by_day(spots, meta, results)

    return results


def main():
    """
    Encapsulate all the core methods required
    in the parsing and calculations

    :return: None
    """

    # Neater way to pass required data around
    meta = Metadata()

    # Get the rotations
    rotations, meta = get_rotations_data(meta)

    # Get the spots
    spots, meta = get_spots_data(rotations, meta)

    # Calculate!
    costs = calculate(spots, meta)
    pprint(costs)


if __name__ == "__main__":
    """
    Driver
    """

    main()
