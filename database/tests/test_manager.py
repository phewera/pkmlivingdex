from database.models import Pokedex
from database.tests.base import DatabaseTestCase


class TestDatabaseManager(DatabaseTestCase):

    def test_create_pokedex(self):
        # setup
        data = {
            'title': 'pokedex-1'
        }

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 0)

        # do it
        result = self.db.create_pokedex(data)

        # post condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)
        self.assertIsInstance(result, Pokedex)
        self.assertEqual(pokedexes[0].title, data['title'])

    def test_create_pokedex__title_already_taken(self):
        # setup
        data = {
            'title': 'pokedex-1'
        }
        self.create_pokedex(data)

        # pre condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)

        # do it
        result = self.db.create_pokedex(data)

        # post condition
        pokedexes = self.db.session.query(Pokedex).all()
        self.assertEqual(len(pokedexes), 1)
        self.assertIsNone(result)

    def test_create_generation(self):
        self.skipTest('ToDo')

    def test_create_dexentry(self):
        self.skipTest('ToDo')

    def test_create_pokemon(self):
        self.skipTest('ToDo')

    def test__create(self):
        self.skipTest('ToDo')

    def test__get__by_id(self):
        self.skipTest('ToDo')

    def test__get__all(self):
        self.skipTest('ToDo')

    def test__format_data(self):
        self.skipTest('ToDo')