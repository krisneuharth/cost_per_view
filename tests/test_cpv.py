from unittest import TestCase, mock

from cost_per_view.data import (Spot, Metadata)

from cost_per_view.cpv import (
    get_spots_data,
    get_rotations_data,
    calculate,
    make_results
)

from cost_per_view.dimensions import (
    filter_sum, calc_cpv,
    cpv_by_creative, cpv_by_rotation,
    cpv_by_day, cpv_by_rotation_by_day,
    cpv_by_rotation_by_creative_by_day
)

from cost_per_view.settings import *


class TestCPV(TestCase):

    def test_get_rotations_data(self):
        meta = Metadata()
        rotations, meta = get_rotations_data(meta)

        self.assertTrue(isinstance(rotations, dict))

        self.assertEqual(len(rotations), 15)
        self.assertEqual(len(meta.rotations_names), 3)

    def test_get_spots_data(self):
        meta = Metadata()
        rotations, meta = get_rotations_data(meta)

        spots, meta = get_spots_data(rotations, meta)

        self.assertTrue(isinstance(spots[0], Spot))

        self.assertEqual(len(spots), 10)
        self.assertEqual(len(meta.spot_days), 2)
        self.assertEqual(len(meta.creative_names), 2)

    def test_filter_sum(self):
        meta = Metadata()
        rotations, meta = get_rotations_data(meta)

        spots, meta = get_spots_data(rotations, meta)

        # None, with made up fx never true
        sum_spend, sum_views = filter_sum(lambda x: x.creative is None, spots)
        self.assertEqual(sum_spend,  0)
        self.assertEqual(sum_views, 0)

        # All, with made up fx always true
        sum_spend, sum_views = filter_sum(lambda x: len(x.creative) > 3, spots)
        self.assertEqual(sum_spend, 4361.0)
        self.assertEqual(sum_views, 1270.0)

    def test_calc_cpv(self):
        # Zero division
        self.assertEqual(calc_cpv(4361.0, 0), 0)

        # Real numbers
        self.assertEqual(calc_cpv(4361.0, 1270), 3.43)

    @mock.patch('cost_per_view.cpv.cpv_by_creative')
    @mock.patch('cost_per_view.cpv.cpv_by_rotation')
    @mock.patch('cost_per_view.cpv.cpv_by_day')
    @mock.patch('cost_per_view.cpv.cpv_by_rotation_by_day')
    @mock.patch('cost_per_view.cpv.cpv_by_rotation_by_creative_by_day')
    def test_calculate(self,
                       mock_cpv_by_creative,
                       mock_cpv_by_rotation,
                       mock_cpv_by_day,
                       mock_cpv_by_rotation_by_day,
                       mock_cpv_by_rotation_by_creative_by_day):

        meta = Metadata()

        rotations, meta = get_rotations_data(meta)
        spots, meta = get_spots_data(rotations, meta)

        results = calculate(spots, meta)

        self.assertEqual(mock_cpv_by_creative.call_count, 1)
        self.assertEqual(mock_cpv_by_rotation.call_count, 1)
        self.assertEqual(mock_cpv_by_day.call_count, 1)
        self.assertEqual(mock_cpv_by_rotation_by_day.call_count, 1)
        self.assertEqual(mock_cpv_by_rotation_by_creative_by_day.call_count, 1)

        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[ROOT_KEY]), 5)


class TestDimensions(TestCase):

    def setUp(self):
        # Before each test, get required data
        self.meta = Metadata()

        self.rotations, self.meta = get_rotations_data(self.meta)
        self.spots, self.meta = get_spots_data(self.rotations, self.meta)

        self.results = make_results()

    def test_cpv_by_creative(self):
        cpv_by_creative(self.spots, self.meta, self.results)
        self.assertEqual(len(self.results[ROOT_KEY][CREATIVE]), 2)

    def test_cpv_by_rotation(self):
        cpv_by_rotation(self.spots, self.meta, self.results)
        self.assertEqual(len(self.results[ROOT_KEY][ROTATION]), 3)

    def test_cpv_by_day(self):
        cpv_by_day(self.spots, self.meta, self.results)
        self.assertEqual(len(self.results[ROOT_KEY][DAY]), 2)

    def test_cpv_by_rotation_by_day(self):
        cpv_by_rotation_by_day(self.spots, self.meta, self.results)

        self.assertEqual(
            len(self.results[ROOT_KEY][ROTATION_BY_DAY]), 5
        )

    def test_cpv_by_rotation_by_creative_by_day(self):
        cpv_by_rotation_by_creative_by_day(self.spots, self.meta, self.results)

        self.assertEqual(
            len(self.results[ROOT_KEY][ROTATION_BY_CREATIVE_BY_DAY]), 7
        )


class TestMakeResults(TestCase):

    def test_results(self):
        results = make_results()
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[ROOT_KEY]), 5)

        for key in DIMENSION_KEYS:
            self.assertTrue(key in results[ROOT_KEY])

