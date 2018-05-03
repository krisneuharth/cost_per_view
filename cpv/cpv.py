import json
import csv
from datetime import datetime, time

ROTATIONS_DATA = '../data/rotations.csv'
SPOTS_DATA = '../data/spots.csv'


class DefaultEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, time):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def get_rotations_data():
    with open(ROTATIONS_DATA) as f:
        reader = csv.reader(f)

        # Pop the header
        header = next(reader)
        print(header)

        # Go through the rotations file,
        # pull out the name and time ranges
        rotations = {}
        for line in reader:
            # Time name = {Afternoon, Morning, Prime}
            k = line[2]

            # Start and end times
            v = (
                # String, time
                line[0], datetime.strptime(line[0], "%I:%M %p").time(),
                line[1], datetime.strptime(line[1], "%I:%M %p").time(),
            )

            # Store for lookup later
            rotations[k] = v

        return rotations


def get_spots_data():
    with open(SPOTS_DATA) as f:
        reader = csv.reader(f)

        # Pop the header
        header = next(reader)
        print(header)

        spots = []
        for line in reader:
            print(line)
            # DO LOOKUP FOR TIME RANGE
            spots.append(line)

        return spots


def pprint(data):
    print(
        json.dumps(
            data,
            indent=2,
            cls=DefaultEncoder
        )
    )


if __name__ == "__main__":
    rotations = get_rotations_data()
    pprint(rotations)

    print('\n')

    spots = get_spots_data()
    pprint(spots)

