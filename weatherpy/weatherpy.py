import requests

class Weatherpy:
    """
    The base class for Weatherpy API access. Used mostly for setting headers and
    querying base-level endpoints.

    Attributes
    ----------
    request_timeout : int, default 15
        The number of seconds to wait for an API response before timeout
    api_url : str, default 'https://api.weather.gov'
        The URL of the NWS API. Should never need to change this manually.
    user_agent_client : str
        The first half of the User-Agent header, should ideally be the name of
        the executing application
    user_agent_email : str
        The second half of the User-Agent header, should ideally be the email
        of the developer or organization

    Methods
    -------
    get_stations(state, limit, cursor, raw)
        Get a list of all available NWS observation stations
    
    """

    request_timeout = 15 # By default, requests will timeout after 15 seconds
    api_url = 'https://api.weather.gov'
    user_agent_client = ''
    user_agent_email = ''

    def __init__(self):
        if self.user_agent_client == '' or self.user_agent_email == '':
            raise Exception(
                'user_agent_client and user_agent_email must be set before initializing Weatherpy.'
            )
        self._headers ={
            'User-Agent': self.user_agent,
            'Accept' : 'application/ld+json'
        }

    # Instance methods
    def get_stations(
            self,
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

        endpoint = self.api_url + '/stations'
        params = {}
        if state:
            params['state'] = state
        if cursor:
            params['cursor'] = cursor
        params['limit'] = limit

        headers = self._headers
        if raw: # Users pulling raw data probably want GeoJSON
            headers['Accept'] = 'application/geo+json'

        r = requests.get(endpoint, headers=headers, params=params, timeout=self.request_timeout)
        if raw:
            return r.text
        else:
            return Station.from_json(r.json())
    
    # Dynamic properties
    @property
    def user_agent(self):
        return f'({self.user_agent_client}, {self.user_agent_email})'
    
    # Magic methods
    def __repr__(self):
        return f"Weatherpy({self.user_agent})"

class Station(Weatherpy):
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
        super().__init__()
        self._id = id
    
    def query(self):
        """Runs the API request to fully initialize the Station object"""
        endpoint = self.api_url + '/stations/' + self.id
        r = requests.get(endpoint, headers=self._headers, timeout=self.request_timeout)
        if r.status_code != 200:
            raise Exception('API returned code ' + str(r.status_code))
        else:
            data = r.json()
            self._geometry = data['geometry']
            self._elevation = data['elevation']
            self._name = data['name']
            self._timezone=data['timeZone']
            self._forecast = data['forecast']
            self._county = data['county']
            self._fire_weather_zone = data['fireWeatherZone']

    # Static methods
    @staticmethod
    def from_json(input: dict) -> list:
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
            station = Station(item['stationIdentifier'])
            station._geometry = item['geometry']
            station._elevation = item['elevation']
            station._name = item['name']
            station._timezone = item['timeZone']
            station._forecast = item['forecast']
            station._county = item['county']
            station._fire_weather_zone = item['fireWeatherZone']
            
            stations.append(station)
        return stations

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