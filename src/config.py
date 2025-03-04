import json
import os.path


class Config:
    _config = None

    @staticmethod
    def load_config_if_needed():
        config_path = ""

        if Config._config is None:
            try:
                config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
                with open(config_path, 'r') as file:
                    Config._config = json.load(file)
            except Exception as e:
                raise Exception(f"Could not load config file at {config_path}\n{str(e)}")

    @staticmethod
    def get(field_name):
        Config.load_config_if_needed()

        if field_name in Config._config:
            return Config._config[field_name]
        else:
            raise KeyError(f"Field '{field_name}' not found in config")
