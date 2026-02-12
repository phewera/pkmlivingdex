from unittest.mock import AsyncMock, patch
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from fastapi import FastAPI
from contextlib import asynccontextmanager
from main import lifespan, app
from models import Pokemon

# Create a test engine
test_engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

@pytest.fixture(name="mock_db")
def mock_db_fixture():
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    SQLModel.metadata.drop_all(test_engine)

@pytest.mark.anyio
async def test_lifespan_seeds_when_empty(mock_db):
    # Mock the seed function
    with patch("main.seed_pokemon_async", new_callable=AsyncMock) as mock_seed:
        # Patch the engine used in main.py
        with patch("main.engine", test_engine):
            # Trigger lifespan
            async with lifespan(app):
                pass
            
            # Assert seed was called
            mock_seed.assert_called_once()

@pytest.mark.anyio
async def test_lifespan_skips_seed_when_populated(mock_db):
    # Populate the DB
    with Session(test_engine) as session:
        p = Pokemon(
            id=1, 
            name="Bulbasaur", 
            name_en="Bulbasaur",
            generation=1,
            image_url="http://fake.url/img.png",
            shiny_image_url="http://fake.url/shiny.png",
            caught_normal=False, 
            caught_shiny=False,
            display_name="Bulbasaur"
        )
        session.add(p)
        session.commit()

    # Mock the seed function
    with patch("main.seed_pokemon_async", new_callable=AsyncMock) as mock_seed:
        # Patch the engine used in main.py
        with patch("main.engine", test_engine):
            # Trigger lifespan
            async with lifespan(app):
                pass
            
            # Assert seed was NOT called
            mock_seed.assert_not_called()
