import os
import logging

DIR_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        os.path.pardir
    )
)

ROTATIONS_FILE = os.path.join(DIR_PATH, 'data/rotations.csv')
SPOTS_FILE = os.path.join(DIR_PATH, 'data/spots.csv')

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

DIMENSION_KEYS = [
    CREATIVE, ROTATION, DAY,
    ROTATION_BY_DAY,
    ROTATION_BY_CREATIVE_BY_DAY
]

# Logging
logging.basicConfig(
    format='%(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger()
