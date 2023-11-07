from typing import Dict, Union, TypedDict, Any, List, NotRequired

from sqlalchemy import Integer, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship, DeclarativeBase
from sqlalchemy.orm.relationships import Relationship


class TPokedexData(TypedDict):
    id: NotRequired[int]
    title: str
    generations: NotRequired[Relationship]


class TGenerationData(TypedDict):
    id: NotRequired[int]
    number: int
    sprite: str
    pokedex_id: int
    pokedex: NotRequired[Relationship]
    dexentries: NotRequired[Relationship]


class TDexEntryData(TypedDict):
    id: NotRequired[int]
    number: int
    name: str
    generation_id: int
    generation: NotRequired[Relationship]
    pokemons: NotRequired[Relationship]


class TPokemonData(TypedDict):
    id: NotRequired[int]
    form: int
    sprite: str
    caught: bool
    shiny_caught: bool
    lgplge: bool
    swsh: bool
    bdsp: bool
    sv: bool
    dexentry_id: int
    dexentry: NotRequired[Relationship]


class Base(DeclarativeBase):

    def get_data(self, json_friendly: bool = False) -> Dict[str, Union[int, str, bool, Relationship]]:
        data = dict()

        # noinspection PyTypeChecker
        for column in self.__mapper__.attrs:
            value = getattr(self, column.key)

            if json_friendly:

                if isinstance(column, Relationship):
                    continue

            data[column.key] = value

        return data

    # noinspection PyTypeChecker
    def get_field_ids(self) -> List[str]:
        return [column.key for column in self.__mapper__.attrs]

    def update(self, data: Dict[str, Any]) -> bool:
        field_ids = self.get_field_ids()
        updated = False

        for key, value in data.items():
            if key not in field_ids:
                continue

            if value != getattr(self, key):
                setattr(self, key, value)
                updated = True

        return updated


class Pokedex(Base):
    __tablename__ = 'pokedex'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    # metadata
    title = mapped_column(String, unique=True)
    # children
    generations = relationship("Generation", back_populates="pokedex")


class Generation(Base):
    __tablename__ = 'generation'
    __table_args__ = (UniqueConstraint('number', 'pokedex_id'),)
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Metadata
    number = mapped_column(Integer)
    sprite = mapped_column(String)
    # parent
    pokedex_id = mapped_column(ForeignKey("pokedex.id"))
    pokedex = relationship("Pokedex", back_populates="generations")
    # children
    dexentries = relationship("DexEntry", back_populates="generation")


class DexEntry(Base):
    __tablename__ = 'dexentry'
    __table_args__ = (UniqueConstraint('number', 'generation_id'),)
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Metadata
    number = mapped_column(Integer)
    name = mapped_column(String)
    # parent
    generation_id = mapped_column(ForeignKey("generation.id"))
    generation = relationship("Generation", back_populates="dexentries")
    # children
    pokemons = relationship("Pokemon", back_populates="dexentry")


class Pokemon(Base):
    __tablename__ = 'pokemon'
    __table_args__ = (UniqueConstraint('form', 'dexentry_id'),)
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Metadata
    form = mapped_column(Integer)
    sprite = mapped_column(String)
    # Catch status
    caught = mapped_column(Boolean)
    shiny_caught = mapped_column(Boolean)
    # Catch information
    lgplge = mapped_column(Boolean)
    swsh = mapped_column(Boolean)
    bdsp = mapped_column(Boolean)
    sv = mapped_column(Boolean)
    # parent
    dexentry_id = mapped_column(ForeignKey("dexentry.id"))
    dexentry = relationship("DexEntry", back_populates="pokemons")
