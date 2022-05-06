from configparser import ConfigParser
import json

class IniLoader:
    def __init__(self, file_path: str) -> None:
        self.config = ConfigParser()
        self.config.read(file_path, encoding='utf-8')
    def get(self, section_name: str, key_name: str) -> str:
        return self.config[section_name][key_name]
    def getArray(self, section_name: str, key_name: str) -> list:
        return json.loads(self.config[section_name][key_name])