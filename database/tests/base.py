from unittest import TestCase
from database.manager import DatabaseManager
from database.models import Base
import os


class DatabaseTestCase(TestCase):
    db: DatabaseManager

    def setUp(self) -> None:
        self.db = DatabaseManager(env='testing')

    def tearDown(self) -> None:
        os.remove(self.db.db_path)

    def clear_tables(self):
        self.db.session.expire_all()
        tables = Base.metadata.sorted_tables
        for tbl in reversed(tables):
            self.db.session.execute(tbl.delete())
        self.db.session.commit()
