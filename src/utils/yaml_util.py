import yaml


def load(file_path: str):
    with open(file_path, encoding='UTF-8') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def dump(file_path: str, data: dict):
    """ A function to write YAML file"""
    with open(file_path, 'w', encoding='UTF-8') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)
