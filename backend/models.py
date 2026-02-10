from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from pydantic import ConfigDict


class PokemonBase(SQLModel):
    name: str = Field(index=True)
    name_en: str = Field(index=True)
    generation: int
    image_url: str
    shiny_image_url: str


class Pokemon(PokemonBase, table=True):
    id: int = Field(default=None, primary_key=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Relationship to progress
    progress: Optional["UserProgress"] = Relationship(back_populates="pokemon")


class UserProgress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pokemon_id: int = Field(foreign_key="pokemon.id")
    caught_normal: bool = Field(default=False)
    caught_shiny: bool = Field(default=False)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    pokemon: Optional[Pokemon] = Relationship(back_populates="progress")


class PokemonResponse(PokemonBase):
    id: int
    caught_normal: bool = False
    caught_shiny: bool = False
