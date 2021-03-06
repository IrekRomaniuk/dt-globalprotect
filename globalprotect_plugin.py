import requests, xmltodict, json, urllib3
from ruxit.api.base_plugin import RemoteBasePlugin
import logging

logger = logging.getLogger(__name__)

class GPPluginRemote(RemoteBasePlugin):
    PATH = "/api/?type=op&cmd=<show><global-protect-gateway><current-user/></global-protect-gateway></show>&key="
    def initialize(self, **kwargs):
        # logger.info("Config: %s", self.config)
        # self.path= self.config["path"]
        self.api= self.config.get("API", '')
        self.url= self.config.get("url", "https://10.1.3.6")
        self.name= self.config.get("name", "paneastusprod1")
        logger.info("API: %s, URL: %s, NAME: %s", self.api, self.url, self.name)
        

    def query(self, **kwargs):
        # Create the group/device entities in Dynatrace
        group_name = "GlobalProtect User count"
        group = self.topology_builder.create_group(group_name, group_name)
        device_name = self.name
        device = group.create_device(device_name, device_name)
        logger.info("Topology: group name=%s, device name=%s", group.name, device.name)
        # Provide user count
        # logger.info("URL = %s", self.url + self.PATH)
        userscount = self.users_count(self.url + self.PATH)
        logger.info("Number of users = %s", userscount)
        device.absolute(key='userscount', value=userscount)

    def users_count(self, url):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        r = requests.get(url = url + self.api, verify=False)
        doc = json.loads(json.dumps(xmltodict.parse(r.text))) 
        entries = []
        if 'success' in doc['response']['@status']:
            entries = doc['response']['result']['entry']   
        return len(entries)    
                  