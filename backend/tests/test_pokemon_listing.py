from sqlmodel import Session
from models import Pokemon

def test_read_pokemon_empty(client):
    response = client.get("/pokemon")
    assert response.status_code == 200
    assert response.json() == []

def test_read_pokemon_data(client, session: Session):
    pokemon_1 = Pokemon(id=1, name="Bulbasaur", name_en="Bulbasaur", generation=1, image_url="img.png", shiny_image_url="shiny.png")
    pokemon_2 = Pokemon(id=2, name="Ivysaur", name_en="Ivysaur", generation=1, image_url="img.png", shiny_image_url="shiny.png")
    session.add(pokemon_1)
    session.add(pokemon_2)
    session.commit()

    response = client.get("/pokemon")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == "Bulbasaur"
    assert data[1]["name"] == "Ivysaur"
