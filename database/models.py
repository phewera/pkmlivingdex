from typing import Dict, Union, TypedDict

from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, relationship, DeclarativeBase
from sqlalchemy.orm.relationships import Relationship


# noinspection PyTypedDict
class TPokedexData(TypedDict):
    id: int
    title: str


# noinspection PyTypedDict
class TGenerationData(TPokedexData):
    id: int
    number: int
    name: str
    sprite: str
    pokedex_id: int


# noinspection PyTypedDict
class TDexEntryData(TPokedexData):
    id: int
    number: int
    name: str
    generation_id: str


# noinspection PyTypedDict
class TPokemonData(TPokedexData):
    id: int
    form: int
    sprite: str
    caught: bool
    shiny_caught: bool
    lgplge: bool
    swsh: bool
    bdsp: bool
    sv: bool
    dexentry_id: str


class Base(DeclarativeBase):

    def __data__(self, json_friendly: bool = False) -> Dict[str, Union[int, str, bool, Relationship]]:
        data = dict()

        # noinspection PyTypeChecker
        for column in self.__mapper__.attrs:
            value = getattr(self, column.key)

            if json_friendly:

                if isinstance(column, Relationship):
                    continue

            data[column.key] = value

        return data


class Pokedex(Base):
    __tablename__ = 'pokedex'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    # metadata
    title = mapped_column(String)
    # children
    generations = relationship("Generation", back_populates="pokedex")


class Generation(Base):
    __tablename__ = 'generation'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Metadata
    number = mapped_column(Integer)
    name = mapped_column(String)
    sprite = mapped_column(String)
    # parent
    pokedex_id = mapped_column(ForeignKey("pokedex.id"))
    pokedex = relationship("Pokedex", back_populates="generations")
    # children
    dexentries = relationship("DexEntry", back_populates="generation")


class DexEntry(Base):
    __tablename__ = 'dexentry'
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
