import os
from typing import Optional, NoReturn
from unittest import TestCase

from database.manager import DatabaseManager
from database.models import Base, Pokedex
from database.models import TPokedexData

POKEDEX_DATA = {
    'title': 'test-pokedex'
}


class DatabaseTestCase(TestCase):
    db: DatabaseManager

    def setUp(self) -> None:
        self.db = DatabaseManager(env='testing')

    def tearDown(self) -> None:
        os.remove(self.db.db_path)

    def clear_tables(self) -> NoReturn:
        self.db.session.expire_all()
        tables = Base.metadata.sorted_tables
        for tbl in reversed(tables):
            self.db.session.execute(tbl.delete())
        self.db.session.commit()

    def create_pokedex(self, data: Optional[TPokedexData] = None) -> Pokedex:
        if not data:
            data = POKEDEX_DATA
        obj = Pokedex(**data)
        self.db.session.add(obj)
        self.db.session.commit()
        return obj
