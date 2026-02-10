from sqlmodel import Session
from models import Pokemon, UserProgress

def test_get_stats(client, session: Session):
    # Setup Data
    p1 = Pokemon(id=1, name="Bulbasaur", generation=1, name_en="Bulbasaur", image_url="img.png", shiny_image_url="shiny.png")
    p2 = Pokemon(id=4, name="Charmander", generation=1, name_en="Charmander", image_url="img.png", shiny_image_url="shiny.png")
    p3 = Pokemon(id=152, name="Chikorita", generation=2, name_en="Chikorita", image_url="img.png", shiny_image_url="shiny.png")
    
    session.add(p1)
    session.add(p2)
    session.add(p3)
    
    # Progress: Caught 1 normal, 1 shiny
    prog1 = UserProgress(pokemon_id=1, caught_normal=True)
    prog2 = UserProgress(pokemon_id=4, caught_shiny=True)
    
    session.add(prog1)
    session.add(prog2)
    session.commit()

    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    
    # Should have stats for Gen 1 and Gen 2
    gen1_stats = next(s for s in data if s["generation"] == 1)
    assert gen1_stats["total"] == 2
    assert gen1_stats["caught_any"] == 2 # Both have at least one type caught?
    # Wait, caught_any logic in backend: sum(1 for p in pokes_in_gen if p.caught_normal or p.caught_shiny)
    # p1 has caught_normal=True -> 1
    # p2 has caught_shiny=True -> 1
    # So caught_any = 2
    
    assert gen1_stats["caught_normal"] == 1
    assert gen1_stats["caught_shiny"] == 1
    
    gen2_stats = next(s for s in data if s["generation"] == 2)
    assert gen2_stats["total"] == 1
    assert gen2_stats["caught_any"] == 0
