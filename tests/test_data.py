from unittest import TestCase

from cost_per_view.data import Spot, Metadata


class TestSpot(TestCase):

    def test_create(self):
        spot = Spot()
        spot.date = "01/02/2016"
        spot.time = "8:30 AM"
        spot.creative = "TEST001H"
        spot.spend = 120.50
        spot.views = 100
        spot.rotation = 'Morning'

        self.assertTrue(spot.rotation == 'Morning')

    def test_str(self):
        spot = Spot()
        spot.date = "01/02/2016"
        spot.time = "8:30 AM"
        spot.creative = "TEST001H"
        spot.spend = 120.50
        spot.views = 100
        spot.rotation = 'Morning'

        str_spot = str(spot)

        self.assertTrue('"rotation": "Morning"' in str_spot)


class TestMetadata(TestCase):

    def test_create(self):
        meta = Metadata()

        meta.rotations_names = ['Morning', 'Afternoon']
        meta.creative_names = ['TEST1', 'TEST2']
        meta.spot_days = [1, 2, 3]

        self.assertTrue(len(meta.rotations_names) == 2)
        self.assertTrue(len(meta.creative_names) == 2)
        self.assertTrue(len(meta.spot_days) == 3)
