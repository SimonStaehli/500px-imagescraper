import requests
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import random
import tqdm
import datetime as dt


class UserAgentConstructor(object):
    """Constructs User Agents to use as headers in requests."""

    def __init__(self, user_agent_path='user_agents.json'):
        """
        User Agents which can be used for the HTTP-Request headers.

        Usage:
        1. Initiate class
        2. call method load()
        3. Extract one random user agent: get_user_agent()

        arguments:
        -----------------
        user_agent_path:
            Path where to save the user_agents.json. This is already predefined in same dir.

        user_agents:
            List of possible user agents.

        """
        self.user_agent_path = user_agent_path
        self.user_agents = None

    def load_ua(self):
        """(None)  ---> JSON

        Loads user agents from the website : 'https://deviceatlas.com/blog/list-of-user-agent-strings'

        returns:
        ------------
        JSON
            Saves JSON File with different user agents to local directory
        """
        response = requests.get(
            'https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/')
        soup = BeautifulSoup(response.text, 'html.parser')
        parsed_user_agents = dict(user_agents=[i.text for i in soup.find_all('td')])

        with open(self.user_agent_path, 'w') as json_file:
            json.dump(parsed_user_agents, json_file)

        self.user_agents = self.read_user_agents()

        print('user_agents.json created in directory.')

    def read_user_agents(self):
        """(None) ---> list

        This function returns a user agent from the class.

        returns:
        ------------
        json_file['user_agents']:
            list of user_agents

        """
        with open(self.user_agent_path, 'r') as json_file:
            json_file = json.load(json_file)

        return json_file['user_agents']

    def get_user_agent(self):
        """(None) ---> str

        Returns a random user agent from the list defined as class attribute.

        returns:
        --------------
        random_user_agent:
            a randomly picked user agent from a list of possible user agents.
        """
        return {'User-Agent': random.choice(self.user_agents)}


class ProxyConstructor(object):
    """Constructs Proxies to use in requests."""

    def __init__(self, proxy_path='proxy.json', proxy_endpoint='ProxyScrape'):
        """
        Proxies which can be used for the HTTP-Request.

        Usage:
        1. Call method load()
        2. If you want to check proxies then call google_check()
        3. To get a proxy call the method get_proxy()

        arguments:
        -----------------
        proxy_path:
            Path where to save the proxies. This is already predefined in same dir.

        proxies:
            List of possible proxies.

        proxy_endpoint:
            Which proxy endpoint should be used to get the proxy addresses. Further endpoints to be added..
            Options: "ProxyScrape", "Geonode", ...

        """
        self.proxy_path = proxy_path
        self.proxies = None
        self.proxy_endpoint = proxy_endpoint

    def load(self):
        """
        Main script to call class method by the endpoint provided as class object.

        """
        if self.proxy_endpoint == 'ProxyScrape':
            self.load_proxies_proxyscrape()

        elif self.proxy_endpoint == 'Geonode':
            self.load_proxies_geonode()

    def load_proxies_proxyscrape(self):
        """(None) --> JSON

        Loads proxies from the website : Proxyscrape.com
        Gets Textfile with proxies from the adress and saves it locally in a JSON.

        returns:
        ------------
        JSON
            Saves JSON File with different proxies to local directory
        """
        try:
            response = requests.get(
                'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=2500&country=all&ssl=all&anonymity=all&simplified=true')
        except Exception as e:
            raise (e, f'HTTP-Statuscode: {response.status_code}')

        response = response.text.split('\r\n')
        proxies_dict = dict(proxies=response)

        with open(self.proxy_path, 'w') as json_file:
            json.dump(proxies_dict, json_file)

        self.read_proxies()

        print(f'{self.proxy_path} created in directory.')

    def load_proxies_geonode(self):
        """(None)  ---> JSON

        Loads proxies from the website :https://proxylist.geonode.com/
        It is also possible to use this method to load new proxies and save it as JSON. The old Json
        will be overwritten by this process.

        returns:
        ------------
        JSON
            Saves JSON File with different proxies to local directory
        """
        endpoint = 'https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&google=true&speed=medium&protocols=http%2Chttps'
        try:
            response = requests.get(endpoint)
            json_file = json.loads(response.text)
        except Exception as e:
            raise (e, f'HTTP-Statuscode: {response.status_code}')

        free_proxies = pd.DataFrame(json_file['data'])[['ip', 'port', 'protocols']]
        free_proxies['protocols'] = free_proxies['protocols'].apply(lambda x: ', '.join(x))
        free_proxies = free_proxies[free_proxies['protocols'].isin(['http', 'https'])]

        free_proxies['proxy'] = free_proxies['ip'].astype(str) + ':' + free_proxies['port'].astype(str)
        proxies_dict = dict(proxies=free_proxies['proxy'].to_list())

        with open(self.proxy_path, 'w') as json_file:
            json.dump(proxies_dict, json_file)

        self.read_proxies()

        print(f'{self.proxy_path} created in directory.')

    def google_check(self, timeout_limit=15, keep_good=True):
        """(int, bool, bool) ----> self.proxies

        Checks if the given proxies of the class object do respond in a certain amount of time. If not then
        the corresponding proxy will be kicked from the list.

        args:
        ------------
        timeout_limit:
            Seconds to respond for the proxy if higher than this limit, the proxy will be kicked.

        keep_good:
            If true then only the good proxy were kept.

        print_times:
            if true then prints times of each proxy to respond and for a simple request.

        """
        times = []
        i = 1
        for proxy in tqdm(self.proxies):
            proxy = {'http': proxy, 'https': proxy}
            start = dt.datetime.now()
            try:
                requests.get('https://www.google.ch/', proxies=proxy, timeout=timeout_limit)
                end = dt.datetime.now() - start
                times.append(end)
            except:
                times.append(None)
            finally:
                i += 1

        # Filter proxies with None and set new proxies
        checked_proxies = [i for i, _ in enumerate(times) if _ != None]
        checked_proxies = [self.proxies[i] for i in checked_proxies]
        print(f'Reachable: {len(checked_proxies)} of {len(self.proxies)}')
        if keep_good:
            self.proxies = checked_proxies
            proxies_dict = dict(proxies=self.proxies)
            with open(self.proxy_path, 'w') as json_file:
                json.dump(proxies_dict, json_file)

    def read_proxies(self):
        """(None) ---> list

        This method reads proxies from json file.

        returns:
        ------------
        json_file['proxies']:
            list of proxies

        """
        with open(self.proxy_path, 'r') as json_file:
            json_file = json.load(json_file)

        self.proxies = json_file['proxies']

    def get_proxy(self):
        """(None) ---> dict

        Returns a random proxy from the list defined as class attribute.

        returns:
        --------------
        random_proxy:
            a randomly picked proxy from a list of possible proxies.
        """
        proxy = random.choice(self.proxies)

        return {'http': proxy, 'https': proxy}

class HTTPHeaderConstructor(ProxyConstructor, UserAgentConstructor):

    def __init__(self):
        ProxyConstructor.__init__(self, proxy_path='proxy.json', proxy_endpoint='ProxyScrape')
        UserAgentConstructor.__init__(self, user_agent_path='user_agents.json')

    def _check_json(self):
        """
        Checks if json file exist in the working dir.
        """
        files = os.listdir()
        if self.proxy_path in files and self.user_agent_path in files:
            pass
        else:
            raise Exception(f'One of the Files {self.proxy_path}, {self.user_agent_path} not exists')


if __name__ == '__main__':
    constructor = HTTPHeaderConstructor()
    # Load Proxies
    constructor.load_proxy()
    # Load User Agents
    constructor.load_ua()

    print('Successfully initiated Proxies and UserAgents')

