from os import path
from typing import Optional, TypedDict, List, NoReturn

import pandas as pd

from database import logger
from database.manager import DatabaseManager, TAvailableEnvironments
from database.models import Generation, DexEntry, Pokemon

WORKING_DIR = path.dirname(path.abspath(__file__))


class TCSVData(TypedDict):
    number: int
    name: str
    form: int
    sprite: str
    generation: int
    lgplge: bool
    swsh: bool
    arceus: bool
    bdsp: bool
    sv: bool


class Importer:
    file_name: str = 'dex-data.csv'
    file_path: str
    file: str
    db: DatabaseManager

    updated: int
    imported: int

    def __init__(
            self,
            file_name: Optional[str] = None,
            file_path: Optional[str] = None,
            env: TAvailableEnvironments = 'production'
    ) -> None:
        if file_name:
            self.file_name = file_name

        if file_path:
            self.file_path = file_path
        else:
            self.file_path = self._get_default_file_path()

        self.db = DatabaseManager(env)
        self.file = self._get_file()

    def run_import(self, pokedex_id: int) -> NoReturn:
        data = self._parse_csv()
        if not data:
            return

        if not self.db.get_pokdex(pokedex_id):
            logger.error(f'Can not import data. Pokedex with id "{pokedex_id}" does not exist.')
            return

        self.updated = 0
        self.imported = 0
        for dataset in data:
            if self._check_missing_values(dataset):
                logger.warn(f'Can not create db entry because of missing values: {dataset}')
                continue

            # Generation
            generation = self._handle_generation(
                pokedex_id=pokedex_id,
                dataset=dataset
            )
            if not generation:
                continue

            # DexEntry
            dexentry = self._handle_dexentry(
                generation_id=generation.id,
                dataset=dataset
            )
            if not dexentry:
                continue

            # Pokemon
            pokemon = self._handle_pokemon(
                dexentry_id=dexentry.id,
                dataset=dataset
            )
            if not pokemon:
                continue

        logger.info(f'Import done: {self.imported} Objects imported and {self.updated} Objects updated.')

    def _handle_generation(self, pokedex_id: int, dataset: TCSVData) -> Optional[Generation]:
        data = {
            'number': dataset['generation'],
            'sprite': f'gen_{dataset["generation"]}.png',
            'pokedex_id': pokedex_id
        }

        generations = self.db.get_generations_by_filter({
            'pokedex_id': pokedex_id,
            'number': dataset['generation']
        })

        if len(generations) > 0:
            generation = generations[0]
            updated = generation.update(data)
            if updated:
                self.updated += 1

        else:
            generation = self.db.create_generation(data)
            if generation:
                self.imported += 1

        return generation

    def _handle_dexentry(self, generation_id: int, dataset: TCSVData) -> Optional[DexEntry]:
        data = {
            'generation_id': generation_id,
            'number': dataset['number'],
            'name': dataset['name'],
        }

        dexentries = self.db.get_dexentries_by_filter({
            'generation_id': generation_id,
            'number': dataset['number']
        })

        if len(dexentries) > 0:
            dexentry = dexentries[0]
            updated = dexentry.update(data)
            if updated:
                self.updated += 1

        else:
            dexentry = self.db.create_dexentry(data)
            if dexentry:
                self.imported += 1

        return dexentry

    def _handle_pokemon(self, dexentry_id: int, dataset: TCSVData) -> Optional[Pokemon]:
        data = {
            'dexentry_id': dexentry_id,
            'form': dataset['form'],
            'sprite': dataset['sprite'],
            'lgplge': dataset['lgplge'],
            'swsh': dataset['swsh'],
            'arceus': dataset['arceus'],
            'bdsp': dataset['bdsp'],
            'sv': dataset['sv'],
        }

        pokemons = self.db.get_pokemons_by_filter({
            'dexentry_id': dexentry_id,
            'form': dataset['form']
        })

        if len(pokemons) > 0:
            pokemon = pokemons[0]
            updated = pokemon.update(data)
            if updated:
                self.updated += 1

        else:
            pokemon = self.db.create_pokemon(data)
            if pokemon:
                self.imported += 1

        return pokemon

    @staticmethod
    def _get_default_file_path() -> str:
        return path.join(WORKING_DIR, '../var/import')

    def _get_file(self) -> str:
        return path.join(self.file_path, self.file_name)

    def _validate_file(self) -> bool:
        if not path.isfile(self.file):
            logger.error(f'Import file "${self.file}" does not exist.')
            return False

        if not self.file.endswith('.csv'):
            logger.error(f'Provided import file "${self.file_name}" ist not a .csv file.')
            return False

        return True

    def _parse_csv(self) -> Optional[List[TCSVData]]:
        if not self._validate_file():
            return None

        try:
            dataframe = pd.read_csv(
                filepath_or_buffer=self.file,
                dtype=TCSVData.__annotations__,
                usecols=list(TCSVData.__annotations__.keys())
            )
        except ValueError as err:
            logger.error(f'Could not parse "{self.file_name}": {err.args[0]}')
            return None

        return dataframe.to_dict(orient='records')

    @staticmethod
    def _check_missing_values(dataset: TCSVData) -> bool:
        return 'NA' in dataset.values()
