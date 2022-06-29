from django.test import TestCase

from units.helpers import get_converted_value


class UnitAppTest(TestCase):

    def test_get_converted_value(self):
        val = get_converted_value(
            value=7,
            user_unit="None",
            group="volume",
        )
        self.assertEqual(val, "")

        val = get_converted_value(
            value=7,
            user_unit="gal",
            group="volume",
        )
        self.assertEqual(val, "1.8 Gallon")
