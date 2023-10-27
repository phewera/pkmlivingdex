import os
from typing import Dict, Any, List, Union, Optional, TypeVar, Type

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Session

from database import logger
from database.config import TAvailableEnvironments, Environments
from database.models import Base, Pokedex, Generation, DexEntry, Pokemon
from database.models import TPokedexData, TGenerationData, TDexEntryData, TPokemonData

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
ModelInstance = TypeVar("ModelInstance", bound=Base)


class DatabaseManager:
    engine: Engine = None
    session: Session = None
    env: TAvailableEnvironments
    db_name: str
    db_path: str

    def __init__(self, env: TAvailableEnvironments = 'production') -> None:
        # load env settings
        self.env = env
        env_settings = Environments.get(env)
        if not env_settings:
            raise KeyError(f'Environment "{env}" not found.')
        self.db_name = env_settings.get('db_name')

        # init engine
        self.db_path = os.path.join(WORKING_DIR, '..', 'var', f'{self.db_name}.db')
        sqlite_path = f'sqlite:///{self.db_path}'
        self.engine = create_engine(sqlite_path, echo=False)

        # init session
        session = sessionmaker(bind=self.engine)
        self.session = session()

        # init db
        Base.metadata.create_all(self.engine)

    def create_pokedex(self, data: TPokedexData) -> Optional[Pokedex]:
        return self._create(Pokedex, data)

    def create_generation(self, data: TGenerationData) -> Optional[Generation]:
        if not self._validate_reference(model=Pokedex, _id=data.get('pokedex_id')):
            return None
        return self._create(Generation, data)

    def create_dexentry(self, data: TDexEntryData) -> Optional[DexEntry]:
        if not self._validate_reference(model=Generation, _id=data.get('generation_id')):
            return None
        return self._create(DexEntry, data)

    def create_pokemon(self, data: TPokemonData) -> Optional[Pokemon]:
        if not self._validate_reference(model=DexEntry, _id=data.get('dexentry_id')):
            return None
        return self._create(Pokemon, data)

    def _create(self, model: Type[Base], data: Dict[str, Any]) -> Optional[ModelInstance]:
        try:
            obj = model(**data)
            self.session.add(obj)
            self.session.commit()

        except IntegrityError as err:
            self.session.rollback()
            logger.error(f'Creating "{model.__name__}" failed ({err.orig})')
            return None

        return obj

    def _get(self, model: Type[Base], _id: str) -> Union[Optional[ModelInstance]]:
        return self.session.query(model).filter_by(id=_id).first() or None

    def _get_all(self, model: Type[Base]) -> List[Optional[ModelInstance]]:
        return self.session.query(model).all() or list()

    def _validate_reference(self, model: Type[Base], _id: str) -> bool:
        if not self._get(model=model, _id=_id):
            logger.error(f'Referenced "{model.__name__}" (ID: {_id}) object could not be found.')
            return False
        return True

    def _format_data(self, data: Dict[str, Any], model: DeclarativeBase):
        pass

        # columns = model.__table__.columns.keys()
        # for key, value in data.items():
        #     if not value:
        #         raise
        #     if key not in columns:
        #         raise
