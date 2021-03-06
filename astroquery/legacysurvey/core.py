# Licensed under a 3-clause BSD style license - see LICENSE.rst


# put all imports organized as shown below
# 1. standard library imports

# 2. third party imports
import astropy.units as u
import astropy.coordinates as coord
import astropy.io.votable as votable
import requests
from astropy.table import Table
from astropy.io import fits

import io

# 3. local imports - use relative imports
# commonly required local imports shown below as example
# all Query classes should inherit from BaseQuery.
from ..query import BaseQuery
# has common functions required by most modules
from ..utils import commons
# prepend_docstr is a way to copy docstrings between methods
from ..utils import prepend_docstr_nosections
# async_to_sync generates the relevant query tools from _async methods
from ..utils import async_to_sync
# import configurable items declared in __init__.py
from . import conf


# export all the public classes and methods
__all__ = ['LegacySurvey', 'LegacySurveyClass']

# declare global variables and constants if any


# Now begin your main class
# should be decorated with the async_to_sync imported previously
@async_to_sync
class LegacySurveyClass(BaseQuery):

    """
    Not all the methods below are necessary but these cover most of the common
    cases, new methods may be added if necessary, follow the guidelines at
    <http://astroquery.readthedocs.io/en/latest/api.html>
    """
    # use the Configuration Items imported from __init__.py to set the URL,
    # TIMEOUT, etc.
    URL = conf.server
    TIMEOUT = conf.timeout

    # all query methods are implemented with an "async" method that handles
    # making the actual HTTP request and returns the raw HTTP response, which
    # should be parsed by a separate _parse_result method.   The query_object
    # method is created by async_to_sync automatically.  It would look like
    # this:
    """
    def query_object(object_name, get_query_payload=False)
        response = self.query_object_async(object_name,
                                           get_query_payload=get_query_payload)
        if get_query_payload:
            return response
        result = self._parse_result(response, verbose=verbose)
        return result
    """

    def query_object_async(self, object_name, get_query_payload=False,
                           cache=True, data_release=9):
        """
        This method is for services that can parse object names. Otherwise
        use :meth:`astroquery.template_module.TemplateClass.query_region`.
        Put a brief description of what the class does here.

        Parameters
        ----------
        object_name : str
            name of the identifier to query.
        get_query_payload : bool, optional
            This should default to False. When set to `True` the method
            should return the HTTP request parameters as a dict.
        verbose : bool, optional
           This should default to `False`, when set to `True` it displays
           VOTable warnings.
        any_other_param : <param_type>
            similarly list other parameters the method takes

        Returns
        -------
        response : `requests.Response`
            The HTTP response returned from the service.
            All async methods should return the raw HTTP response.

        Examples
        --------
        While this section is optional you may put in some examples that
        show how to use the method. The examples are written similar to
        standard doctests in python.

        """
        # the async method should typically have the following steps:
        # 1. First construct the dictionary of the HTTP request params.
        # 2. If get_query_payload is `True` then simply return this dict.
        # 3. Else make the actual HTTP request and return the corresponding
        #    HTTP response
        # All HTTP requests are made via the `BaseQuery._request` method. This
        # use a generic HTTP request method internally, similar to
        # `requests.Session.request` of the Python Requests library, but
        # with added caching-related tools.

        # See below for an example:

        # first initialize the dictionary of HTTP request parameters
        request_payload = dict()

        # Now fill up the dictionary. Here the dictionary key should match
        # the exact parameter name as expected by the remote server. The
        # corresponding dict value should also be in the same format as
        # expected by the server. Additional parsing of the user passed
        # value may be required to get it in the right units or format.
        # All this parsing may be done in a separate private `_args_to_payload`
        # method for cleaner code.

        #request_payload['object_name'] = object_name
        # similarly fill up the rest of the dict ...

        if get_query_payload:
            return request_payload
        # BaseQuery classes come with a _request method that includes a
        # built-in caching system

        # TODO: implement here http query as needed
        # e.g. I suspect we get files like this one: https://portal.nersc.gov/cfs/cosmo/data/legacysurvey/dr9/north/tractor/000/tractor-0001m002.fits
        # to confirm with AG, AN
        # if so:
         
        URL = f"{self.URL}/dr{data_release}/north/tractor/000/tractor-0001m002.fits"

        response = self._request('GET', URL, params={},
                                 timeout=self.TIMEOUT, cache=cache)
        return response

    def query_brick_list_async(self, data_release=9, get_query_payload=False, emisphere="north",
                           cache=True):
        """

        """
        request_payload = dict()

        if get_query_payload:
            return request_payload
        URL = f"{self.URL}/dr{data_release}/{emisphere}/survey-bricks-dr{data_release}-{emisphere}.fits.gz"
        # TODO make it work with the original request
        # response = self._request('GET', URL, params={},
        #                          timeout=self.TIMEOUT, cache=cache)

        response = requests.get(URL)

        print("completed fits file request")

        return response

    # For services that can query coordinates, use the query_region method.
    # The pattern is similar to the query_object method. The query_region
    # method also has a 'radius' keyword for specifying the radius around
    # the coordinates in which to search. If the region is a box, then
    # the keywords 'width' and 'height' should be used instead. The coordinates
    # may be accepted as an `astropy.coordinates` object or as a string, which
    # may be further parsed.

    # similarly we write a query_region_async method that makes the
    # actual HTTP request and returns the HTTP response

    def query_region_async(self, coordinates, radius,
                           get_query_payload=False, cache=True, data_release=9):
        """
        Queries a region around the specified coordinates.

        Parameters
        ----------
        coordinates : str or `astropy.coordinates`.
            coordinates around which to query
        radius : str or `astropy.units.Quantity`.
            the radius of the cone search
        get_query_payload : bool, optional
            Just return the dict of HTTP request parameters.
        verbose : bool, optional
            Display VOTable warnings or not.

        Returns
        -------
        response : `requests.Response`
            The HTTP response returned from the service.
            All async methods should return the raw HTTP response.
        """
        # call the brick list
        table_north = self.query_brick_list(data_release=data_release, emisphere="north")
        table_south = self.query_brick_list(data_release=data_release, emisphere="south")
        # # needed columns: ra1, ra2, dec1, dec2 (corners of the bricks), and also brickname
        # ra1 = table_north['ra1']
        # ra2 = table_north['ra2']
        # dec1 = table_north['dec1']
        # dec2 = table_north['dec2']
        ra = coordinates.ra.deg
        # radius not used for the moment, but it will be in the future
        # must find the brick within ra1 and ra2
        dec = coordinates.dec.deg
        # must find the brick within dec1 and dec2
        row_north = None
        row_south = None

        response_north = None
        response_south = None

        for r in table_north:
            ra1 = r['ra1']
            ra2 = r['ra2']
            dec1 = r['dec1']
            dec2 = r['dec2']
            if ra1 <= ra <= ra2 and dec1 <= dec <= dec2:
                row_north = r
                break
        for r in table_south:
            ra1 = r['ra1']
            ra2 = r['ra2']
            dec1 = r['dec1']
            dec2 = r['dec2']
            if ra1 <= ra <= ra2 and dec1 <= dec <= dec2:
                row_south = r
                break

        if row_north is not None:
            brickname = row_north['brickname']
            raIntPart = "{0:03}".format(int(row_north['ra1']))

            # to get then the brickname of the line of the table
            # extract the integer part of ra1, and in string format (eg 001)
            URL = f"{self.URL}/dr{data_release}/north/tractor/{raIntPart}/tractor-{brickname}.fits"

            response_north = requests.get(URL)
            return response_north

        if row_south is not None:
            brickname = row_south['brickname']
            raIntPart = "{0:03}".format(int(row_south['ra1']))

            # to get then the brickname of the line of the table
            # extract the integer part of ra1, and in string format (eg 001)
            URL = f"{self.URL}/dr{data_release}/south/tractor/{raIntPart}/tractor-{brickname}.fits"

            response_south = requests.get(URL)
            return response_south

        return None

    # as we mentioned earlier use various python regular expressions, etc
    # to create the dict of HTTP request parameters by parsing the user
    # entered values. For cleaner code keep this as a separate private method:

    def _args_to_payload(self, *args, **kwargs):
        request_payload = dict()
        # code to parse input and construct the dict
        # goes here. Then return the dict to the caller

        return request_payload

    # the methods above call the private _parse_result method.
    # This should parse the raw HTTP response and return it as
    # an `astropy.table.Table`. Below is the skeleton:

    def _parse_result(self, response, verbose=False):
        # if verbose is False then suppress any VOTable related warnings
        if not verbose:
            commons.suppress_vo_warnings()
        # try to parse the result into an astropy.Table, else
        # return the raw result with an informative error message.
        try:
            # do something with regex to get the result into
            # astropy.Table form. return the Table.
            # data = io.BytesIO(response.content)

            # TODO figure out on how to avoid writing in a file
            with open('/tmp/file_content', 'wb') as fin:
                fin.write(response.content)

            table = Table.read('/tmp/file_content', hdu=1)

            # table = Table.read(data)
        except ValueError:
            # catch common errors here, but never use bare excepts
            # return raw result/ handle in some way
            pass

        return table

 
# the default tool for users to interact with is an instance of the Class
LegacySurvey = LegacySurveyClass()

# once your class is done, tests should be written
# See ./tests for examples on this

# Next you should write the docs in astroquery/docs/module_name
# using Sphinx.
