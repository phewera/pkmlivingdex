import os
from typing import Optional, NoReturn, Dict, Type, Any
from unittest import TestCase

from database.manager import DatabaseManager, ModelInstance
from database.models import Base, TPokedexData, TGenerationData

POKEDEX_DATA: TPokedexData = {
    'title': 'test-pokedex'
}

GENERATION_DATA: TGenerationData = {
    'number': 1,
    'sprite': 'gen_1.png',
    'pokedex_id': ''
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

    def create_obj(self, model: Type[Base], data: Dict[str, Any]) -> Optional[ModelInstance]:
        obj = model(**data)
        self.db.session.add(obj)
        self.db.session.commit()
        return obj
