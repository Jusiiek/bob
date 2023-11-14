import os
import json
from typing import Union

from config.environment import HERE
from config.config_keys import ConfigKeys


class Config:
    data_path = os.path.join(HERE, "config", "config.json")

    def get_config(self) -> dict:
        with open(self.data_path, 'r') as json_data:
            return json.load(json_data)

    def save_config(self, data: dict):
        with open(self.data_path, 'w') as json_data:
            json.dump(data, json_data, indent=2)

    def set_config(self, key: str, value: Union[str, bool, float, int, list]):
        data = self.get_config()
        data[key] = value
        self.save_config(data)

    def add_value_to_array_config_value(self, key: str, value: Union[str, bool, float, int]):
        data = self.get_config()
        if key in data.keys():
            if isinstance(data[key], list):
                data[key].append(value)

            self.save_config(data)

    def get_config_value(self, key: str):
        data = self.get_config()
        if key in data.keys():
            return data[key]
        else:
            return None

    async def create_setup(self):
        for value in ConfigKeys.__members__.values():
            data = self.get_config()
            if not value.value in data.keys():
                self.set_config(value.value, "")
