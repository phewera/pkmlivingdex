from configparser import ConfigParser, SectionProxy
from typing import Optional


def read_config(section: str) -> Optional[SectionProxy]:
    config = ConfigParser()
    config.read('../config.ini')

    if section not in config.sections():
        return None

    return config[section]
