import os
from typing import Dict, Any, List, Union, Optional, TypeVar, Type

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Session

from database.config import TAvailableEnvironments, Environments
from database.models import Base, Pokedex, Generation, DexEntry, Pokemon

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

    def create_pokedex(self, data) -> Pokedex:
        pass

    def create_generation(self) -> Generation:
        pass

    def create_dexentry(self, data: Dict[str, Any]) -> DexEntry:
        pass

    def create_pokemon(self) -> Pokemon:
        pass

    def _create(self, model: Type[Base], data: Dict[str, Any]) -> Optional[ModelInstance]:
        obj = model(**data)
        self.session.add(obj)
        self.session.commit()

        if not obj:
            return None

        return obj

    def _get(self, model: Type[Base], _id: str = None) -> Union[Optional[ModelInstance], List[Optional[ModelInstance]]]:
        if _id:
            return self.session.query(model).filter_by(id=_id).first() or None
        return self.session.query(model).all() or list()

    def _format_data(self, data: Dict[str, Any], model: DeclarativeBase):
        pass
