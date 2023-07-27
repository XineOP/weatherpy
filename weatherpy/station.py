from .weatherpy import Weatherpy

class Station:
    """
    Class to represent the data and functions of a NWS observation station

    Attributes:
    -----------
    id: str
        The station ID of the observation station
    geometry: str
        The lat/lon geolocation of the observation station
    elevation: str
        The elevation of the observation station in meters
    timezone: str
        A string representation of the observation station's timezone
        (e.g. 'US/Los Angeles')
    
    Methods:
    --------
    query()
        Initializes the object by querying the NWS API for the associated ID
    from_json(input: dict)
        Initializes a list of Station objects from a JSON dictionary
    """
    def __init__(self, api: Weatherpy, id: str):
        self._api = api
        self._id = id
    
    def query(self):
        """Runs the API request to fully initialize the Station object"""
        endpoint = '/stations/' + self.id
        r = self._api.query(endpoint)
        data = r.json()

        self._geometry = data.get('geometry')
        self._elevation = data.get('elevation')
        self._name = data.get('name')
        self._timezone = data.get('timeZone')
        self._forecast = data.get('forecast')
        self._county = data.get('county')
        self._fire_weather_zone = data.get('fireWeatherZone')

    # Static methods
    @staticmethod
    def _from_json(api: Weatherpy, input: dict) -> list:
        """
        Returns a list of Station objects from a JSON-LD object

        Used when initializing from Weatherpy.get_stations()

        Parameters:
        ----------
        input: dict
            The JSON-LD dictionary to initialize from
        
        Returns:
        ----------
        stations: list
            A list of Station objects
        """

        stations = []
        for item in input['@graph']:
            station = Station(api, item.get('stationIdentifier'))
            station._geometry = item.get('geometry')
            station._elevation = item.get('elevation')
            station._name = item.get('name')
            station._timezone = item.get('timeZone')
            station._forecast = item.get('forecast')
            station._county = item.get('county')
            station._fire_weather_zone = item.get('fireWeatherZone')
            
            stations.append(station)
        return stations

    @staticmethod
    def get_stations(
            api: Weatherpy,
            state: str | list = None,
            limit: int = 500,
            cursor: str = None,
            raw: bool = False,
    ) -> str | list:
        """
        Requests a list of all observation stations available
        
        This function queries the NWS API for a list of observation stations. It
        can also query for stations by state/marine region.

        Parameters:
        -----------
        state : str, list, None, default None
            Specific state(s) or maritime region(s) to query for. if
            :const:`None`, will not query for specific state(s) or maritime
            region(s)
        limit : int, default 500
            The maximum number of results to accept.
        cursor : str, None, default None
            Pagination cursor for continuing queries. If :const:`None`, will not
            use a pagination cursor.
        
        Returns:
        -----------
        dict
            If raw is :const:`True`, returns raw GeoJSON text
        list
            If raw is :const:`False`, returns a list of Station objects.
        """

        endpoint = '/stations'

        params = {}
        if state:
            params['state'] = state
        if cursor:
            params['cursor'] = cursor
        params['limit'] = limit

        accept = 'application/geo+json' if raw else 'application/ld+json'

        r = api.query(endpoint, accept, params)

        if raw:
            return r.text
        else:
            return Station._from_json(api, r.json())
    
    # Getters and setters
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
    @property
    def elevation(self):
        return self._elevation
    @property
    def name(self):
        return self._name
    @property
    def timezone(self):
        return self._timezone
    @property
    def geometry(self):
        return self._geometry
    
    # Magic methods
    def __repr__(self):
        return f'Station({self.id})'