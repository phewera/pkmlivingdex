from sqlmodel import Session
from models import Pokemon

def test_filter_pokemon_by_generation(client, session: Session):
    pokemon_1 = Pokemon(id=1, name="Bulbasaur", name_en="Bulbasaur", generation=1, image_url="img.png", shiny_image_url="shiny.png")
    pokemon_152 = Pokemon(id=152, name="Chikorita", name_en="Chikorita", generation=2, image_url="img.png", shiny_image_url="shiny.png")
    session.add(pokemon_1)
    session.add(pokemon_152)
    session.commit()

    response = client.get("/pokemon?generation=1")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["name"] == "Bulbasaur"

    response = client.get("/pokemon?generation=2")
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Chikorita"
