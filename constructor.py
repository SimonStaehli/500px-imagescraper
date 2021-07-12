import requests
from bs4 import BeautifulSoup
import sys, json, os
import pandas as pd
import random


class UserAgentConstructor(object):
    """Constructs User Agents to use as headers in requests."""

    def __init__(self, user_agent_path='user_agents.json'):
        """
        User Agents which can be used for the HTTP-Request headers.

        arguments:
        -----------------
        user_agent_path:
            Path where to save the user_agents.json. This is already predefined in same dir.

        user_agents:
            List of possible user agents.

        """
        self.user_agent_path = user_agent_path
        if user_agent_path not in os.listdir():
            self.load_user_agents()
        self.user_agents = self.read_user_agents()

    def load_user_agents(self):
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
        return {'User-Agent':random.choice(self.user_agents)}


class ProxyConstructor(object):
    """Constructs Proxies to use in requests."""

    def __init__(self, proxy_path='proxy.json'):
        """
        Proxies which can be used for the HTTP-Request.

        Website Souce: https://geonode.com/free-proxy-list

        arguments:
        -----------------
        proxy_path:
            Path where to save the proxies. This is already predefined in same dir.

        proxies:
            List of possible proxies.
        """
        self.proxy_path = proxy_path
        if self.proxy_path not in os.listdir():
            self.load_proxies()

        self.proxies = self.read_proxies()

    def load_proxies(self):
        """(None)  ---> JSON

        Loads proxies from the website : 'https://free-proxy-list.net/'

        returns:
        ------------
        JSON
            Saves JSON File with different proxies to local directory
        """
        response = requests.get(
            "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&google=true&speed=medium&protocols=http%2Chttps")
        json_file = json.loads(response.text)

        free_proxies = pd.DataFrame(json_file['data'])[['ip', 'port', 'protocols']]
        free_proxies['protocols'] = free_proxies['protocols'].apply(lambda x: ', '.join(x))
        free_proxies = free_proxies[free_proxies['protocols'].isin(['http', 'https'])]

        free_proxies['proxy'] = free_proxies['ip'].astype(str) + ':' + free_proxies['port'].astype(str)
        proxies_dict = dict(proxies=free_proxies['proxy'].to_list())

        with open(self.proxy_path, 'w') as json_file:
            json.dump(proxies_dict, json_file)

        print(f'{self.proxy_path} created in directory.')

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

        return json_file['proxies']

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
        ProxyConstructor.__init__(self)
        UserAgentConstructor.__init__(self)

    def _check_json(self):
        """
        Checks if json file exist in the working dir.
        """
        if self.proxy_path in os.listdir() and self.user_agent_path in os.listdir():
            pass
        else:
            raise Exception(f'One of the Files {self.proxy_path}, {self.user_agent_path} not exists')


if __name__ == '__main__':
    constructor = HTTPHeaderConstructor()

    print(constructor.proxies)
    print(constructor.user_agents)

