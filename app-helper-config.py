import yaml

class Config:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            configs = yaml.safe_load(file)
            for key, value in configs.items():
                setattr(self, key, value)

# Usage
config = Config('config.yaml')
