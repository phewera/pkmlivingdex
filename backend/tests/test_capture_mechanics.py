from sqlmodel import Session, select
from models import Pokemon, UserProgress

def test_update_capture_status(client, session: Session):
    # Setup Pokemon
    pokemon = Pokemon(id=1, name="Bulbasaur", name_en="Bulbasaur", generation=1, image_url="img.png", shiny_image_url="shiny.png")
    session.add(pokemon)
    session.commit()

    # Capture Normal
    response = client.post("/pokemon/1/capture", params={"caught_normal": True})
    assert response.status_code == 200
    data = response.json()
    assert data["caught_normal"] is True
    assert data["pokemon_id"] == 1

    # Verify Persistence
    progress = session.exec(select(UserProgress).where(UserProgress.pokemon_id == 1)).first()
    assert progress is not None
    assert progress.caught_normal is True

    # Capture Shiny (and uncapture normal)
    response = client.post("/pokemon/1/capture", params={"caught_normal": False, "caught_shiny": True})
    assert response.status_code == 200
    data = response.json()
    assert data["caught_normal"] is False
    assert data["caught_shiny"] is True
