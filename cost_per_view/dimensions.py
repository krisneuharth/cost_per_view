from cost_per_view.settings import *


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
