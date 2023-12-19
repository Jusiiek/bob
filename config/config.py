import os
import json
from typing import Union

from config.environment import SERVERS_DIR


class Config:

    def __get_config_path(self, guild_id: int) -> Union[str]:
        guild_path = os.path.join(SERVERS_DIR, str(guild_id))
        if not os.path.exists(guild_path):
            os.makedirs(guild_path)

        return os.path.join(SERVERS_DIR, str(guild_id), 'config.json')

    def get_config(self, guild_id: int) -> dict:
        with open(self.__get_config_path(guild_id), 'r') as json_data:
            return json.load(json_data)

    def save_config(self, guild_id: int, data: dict):
        with open(self.__get_config_path(guild_id), 'w') as json_data:
            json.dump(data, json_data, indent=2)

    def set_config(self, guild_id: int, key: str, value: Union[str, bool, float, int, list]):
        data = self.get_config(guild_id)
        data[key] = value
        self.save_config(guild_id, data)

    def add_value_to_array_config_value(self, guild_id: int, key: str, value: Union[str, bool, float, int]):
        data = self.get_config(guild_id)
        if key in data.keys():
            if isinstance(data[key], list):
                data[key].append(value)

            self.save_config(guild_id, data)

    def get_config_value(self, guild_id: int, key: str) -> Union[str, bool, float, int]:
        data = self.get_config(guild_id)
        if key in data.keys():
            return data[key]
        else:
            return None
