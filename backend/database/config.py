from typing import Literal, TypedDict, Dict

TAvailableEnvironments = Literal[
    'production',
    'testing'
]


class TEnvironmentSettings(TypedDict):
    db_name: str


Environments: Dict[str, TEnvironmentSettings] = {
    'production': {
        'db_name': 'database'
    },
    'testing': {
        'db_name': 'testing'
    }
}
