import requests

class Weatherpy:
    """Base class for Weatherpy API implementation, which is passed to other
    classes as part of their constructors"""
    def __init__(
            self,
            user_agent_client: str,
            user_agent_email: str,
            api_url: str = 'https://api.weather.gov',
            request_timeout: int = 15
    ):
        self._user_agent_client = user_agent_client
        self._user_agent_email = user_agent_email
        self._api_url = api_url
        self._request_timeout = request_timeout
    
    def query(self, endpoint: str, accept: str='application/ld+json', params: dict=None):
        full_endpoint = self.api_url + endpoint
        headers = {
            'User-Agent': self.user_agent,
            'Accept': accept
        }
        response = requests.get(
            full_endpoint,
            params=params,
            headers=headers,
            timeout=self.request_timeout
        )
        if response.status_code != 200: # Something went wrong
            raise Exception('API returned code ' + str(response.status_code))
        else:
            return response

    # Getters and setters
    @property
    def user_agent_client(self):
        return self._user_agent_client
    @property
    def user_agent_email(self):
        return self._user_agent_email
    @property
    def api_url(self):
        return self._api_url
    @property
    def request_timeout(self):
        return self._request_timeout
    @property
    def user_agent(self):
        """Returns a formatted User-Agent string"""
        return f'({self.user_agent_client}, {self.user_agent_email})'
    
    # Dunder methods
    def __repr__(self):
        return f'Weatherpy({self.user_agent_client}, {self.user_agent_email})'
    
if __name__ == '__main__':
    test = Weatherpy('Weatherpy API Testing', 'zaccheus.mcfarland@gmail.com')
    print(test)