# Licensed under a 3-clause BSD style license - see LICENSE.rst


# performs similar tests as test_module.py, but performs
# the actual HTTP request rather than monkeypatching them.
# should be disabled or enabled at will - use the
# remote_data decorator from astropy:

import pytest
from astropy.table import Table


@pytest.mark.remote_data
class TestLegacySurveyClass:
    # now write tests for each method here
    def test_query_object(self):
        import astroquery.legacysurvey

        # TODO: add other parameters
        table = astroquery.legacysurvey.LegacySurvey.query_object("Mrk421") # type: Table

        print(table)

        assert len(table) > 10

    def test_query_region(self):
        import astroquery.legacysurvey
        from astropy.coordinates import SkyCoord
        from astropy.coordinates import Angle, Latitude, Longitude  # Angles

        ra = Angle('11h10m55s', unit='hourangle').degree
        dec = Angle('+28d32m37s', unit='hourangle').degree
        radius_input = 3.0  # arcmin

        coordinates = SkyCoord(ra, dec, unit='degree')
        radius = Angle(radius_input, unit='arcmin')

        query1 = astroquery.legacysurvey.LegacySurvey.query_region(coordinates=coordinates, radius=radius, data_release=9)

        print(query1)

    def test_query_brick_list(self):
        import astroquery.legacysurvey

        # TODO: add other parameters
        table = astroquery.legacysurvey.LegacySurvey.query_brick_list(data_release=9) # type: Table

        print(table)

        assert len(table) > 10
