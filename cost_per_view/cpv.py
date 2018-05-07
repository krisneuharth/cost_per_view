import csv

from collections import defaultdict
from datetime import datetime

from copy import deepcopy

from cost_per_view.data import Spot, Metadata
from cost_per_view.dimensions import *
from cost_per_view.settings import *
from cost_per_view.utils import pprint


def get_rotations_data(meta):
    """
    Read up the rotations file
    Store the rotations key by time hour ranges
    Save the rotation names in meta

    :param meta: Metadata object
    :return: dict, Metadata object
    """

    logger.debug('Reading CSV: `%s`' % ROTATIONS_DATA)

    with open(ROTATIONS_DATA) as f:
        reader = csv.reader(f)

        # Pop the header
        header = next(reader)
        logger.debug('CSV header: %s' % header)

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
    Convert lines to Spot objects
    Save some information in meta as we go

    :param rotations: dict
    :param meta: Metadata
    :return: list of Spots, Metadata
    """

    logger.debug('Reading CSV: `%s`' % SPOTS_DATA)

    with open(SPOTS_DATA) as f:
        reader = csv.reader(f)

        # Pop the header
        header = next(reader)
        logger.debug('CSV header: %s' % header)

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


def make_results():
    """
    Prepare the results dict

    :return: dict
    """

    results = {ROOT_KEY: {}}
    for key in DIMENSION_KEYS:
        results[ROOT_KEY][key] = defaultdict(dict)

    return results


def calculate(spots, meta):
    """
    Go through spots and combine with
    metadata in order to calculate the
    desired CPV metric in several dimensions

    :param spots: list of Spots
    :param meta: Metadata object
    :return: results dict
    """

    # Construct our result set
    results = make_results()

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
