import requests
import weatherpy as wp

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
    def __init__(self, id: str):
        self._id = id
        self._headers = {
            'Accept': 'application/ld+json',
            'User-Agent': f'({wp.user_agent_client}, {wp.user_agent_email})'
        }
    
    def query(self):
        """Runs the API request to fully initialize the Station object"""
        endpoint = wp.api_url + '/stations/' + self.id
        r = requests.get(endpoint, headers=self._headers, timeout=wp.request_timeout)
        if r.status_code != 200:
            raise Exception('API returned code ' + str(r.status_code))
        else:
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
    def _from_json(input: dict) -> list:
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
            station = Station(item.get('stationIdentifier'))
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
            state: str | list = None,
            limit: int = 500,
            cursor: str = None,
            raw: bool = False,
    ) -> dict | list:
        """
        Requests a list of all observation stations available
        
        This function queries the NWS API for a list of observation stations. It
        can also query for stations by ID or state/marine region.

        Parameters:
        -----------
        id : str, list, None, default None
            Specific station ID(s) to query for. If :const:`None`, will not query
            for specific ID(s)
        state : str, list, None, default None
            Specific state(s) or maritime region(s) to query for. if :const:`None`,
            will not query for specific state(s) or maritime region(s)
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

        endpoint = wp.api_url + '/stations'
        params = {}
        if state:
            params['state'] = state
        if cursor:
            params['cursor'] = cursor
        params['limit'] = limit

        headers = {
            'Accept': 'application/ld+json',
            'User-Agent': f'({wp.user_agent_client}, {wp.user_agent_email})'
        }
        if raw: # Users pulling raw data probably want GeoJSON
            headers['Accept'] = 'application/geo+json'

        r = requests.get(
            endpoint,
            headers=headers,
            params=params,
            timeout=wp.request_timeout
        )
        if raw:
            return r.text
        else:
            return Station._from_json(r.json())
    
    # Getters and setters
    @property
    def id(self):
        return self._id
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