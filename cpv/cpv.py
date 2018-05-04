import json
import csv
from datetime import datetime, time

ROTATIONS_DATA = '../data/rotations.csv'
SPOTS_DATA = '../data/spots.csv'

DATE_FMT = "%m/%d/%Y"
TIME_FMT = "%I:%M %p"
DATE_TIME_FMT = " ".join(
    [DATE_FMT, TIME_FMT]
)


# ASSUMPTIONS:
#   TIMEZONE? UTC?
#   Overlapping times for rotations
#   12pm on the dot could be two rotations
#   15-16:00 is two rotations?
#   Any other time window is 'Other'


class DefaultEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime) or isinstance(o, time):
            return o.isoformat()
        if isinstance(o, list) or isinstance(o, tuple):
            return ", ".join(o)

        return json.JSONEncoder.default(self, o)


def get_rotations_data():
    with open(ROTATIONS_DATA) as f:
        reader = csv.reader(f)

        # Pop the header
        next(reader)

        # Go through the rotations file,
        # pull out the name and time ranges
        rotations = {}
        errors = []

        for line in reader:
            if not all(line):
                errors.append(line)
                continue

            # Make complex key:
            dt_start = datetime.strptime(line[0], TIME_FMT).time()
            dt_end = datetime.strptime(line[1], TIME_FMT).time()

            # The rotation name
            v = line[2]

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

        return rotations, errors


def get_spots_data(rotations):
    with open(SPOTS_DATA) as f:
        reader = csv.reader(f)

        # Pop the header
        next(reader)

        spots = []
        errors = []

        for line in reader:
            if not all(line):
                errors.append(line)
                continue

            # Convert strings to dt
            dt_aired = datetime.strptime(
                "%s %s" % (line[0], line[1]),
                DATE_TIME_FMT
            )

            # Do the lookup for the rotation
            rotation = rotations.get(
                str(dt_aired.hour), ['Other']
            )

            line.append(rotation)
            spots.append(line)

        return spots, errors


def pprint(data):
    print(
        json.dumps(
            data,
            indent=2,
            cls=DefaultEncoder
        )
    )


if __name__ == "__main__":
    rotations, errors = get_rotations_data()
    #pprint(rotations)

    #print('\n')

    spots, errors = get_spots_data(rotations)
    pprint(spots)
