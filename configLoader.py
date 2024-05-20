
import configparser

class configLoader:
    def read_config(self, section, key):
        config = configparser.ConfigParser()
        config.read('/opt/WAFX/config/waf_config.ini')
        return config[section][key]