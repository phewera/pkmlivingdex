from os import path
from database import logger
from typing import Optional


WORKING_DIR = path.dirname(path.abspath(__file__))


class Importer:
    file_name: str = 'dex-data.csv'
    file_path: str
    file: str

    def __init__(self, file_name: Optional[str] = None, file_path: Optional[str] = None) -> None:
        if file_name:
            self.file_name = file_name

        if file_path:
            self.file_path = file_path
        else:
            self.file_path = self._get_default_file_path()

        self.file = self._get_file()

    def import_data(self):
        pass

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

    def _load_csv(self):
        pass

    def _process_data(self):
        pass

    def _check_if_data_already_exists(self):
        pass
