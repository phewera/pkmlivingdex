import asyncio
import os
import httpx
import anyio
from sqlmodel import Session

from database import engine, create_db_and_tables
from models import Pokemon, SQLModel


REGIONAL_SUFFIXES = ["-alola", "-galar", "-hisui", "-paldea"]


def get_generation_by_id(pokemon_id):
    if pokemon_id <= 151:
        return 1
    elif pokemon_id <= 251:
        return 2
    elif pokemon_id <= 386:
        return 3
    elif pokemon_id <= 493:
        return 4
    elif pokemon_id <= 649:
        return 5
    elif pokemon_id <= 721:
        return 6
    elif pokemon_id <= 809:
        return 7
    elif pokemon_id <= 905:
        return 8
    else:
        return 9


def get_regional_generation(name):
    if "-alola" in name:
        return 7
    if "-galar" in name:
        return 8
    if "-hisui" in name:
        return 8
    if "-paldea" in name:
        return 9
    return None


base_dir = os.path.dirname(os.path.abspath(__file__))
SPRITES_DIR = os.path.join(base_dir, "static", "sprites")
SHINY_SPRITES_DIR = os.path.join(SPRITES_DIR, "shiny")


async def download_image(client, url, path):
    if os.path.exists(path):
        return
    try:
        response = await client.get(url)
        if response.status_code == 200:
            async with await anyio.open_file(path, "wb") as f:
                await f.write(response.content)
    except Exception as e:
        print(f"Error downloading {url}: {e}")


async def fetch_pokemon_variety(client, variety_data, species_names, default_gen):
    try:
        name = variety_data["pokemon"]["name"]
        pokemon_url = variety_data["pokemon"]["url"]
        pokemon_id = int(pokemon_url.split("/")[-2])
        is_default = variety_data["is_default"]

        # Only process default forms or specific regional forms
        is_regional = any(suffix in name for suffix in REGIONAL_SUFFIXES)
        if not is_default and not is_regional:
            return None

        # Determine Names
        german_name = next((n["name"] for n in species_names if n["language"]["name"] == "de"), name.capitalize())
        english_name = next((n["name"] for n in species_names if n["language"]["name"] == "en"), name.capitalize())

        if is_regional:
            # Format regional name like "Alola-Sleima"
            region = next(s[1:] for s in REGIONAL_SUFFIXES if s in name)
            german_name = f"{region.capitalize()}-{german_name}"
            english_name = f"{region.capitalize()} {english_name}"
            generation = get_regional_generation(name)
        else:
            generation = default_gen

        # Sprites
        original_image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
        original_shiny_image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{pokemon_id}.png"

        local_image_path = os.path.join(SPRITES_DIR, f"{pokemon_id}.png")
        local_shiny_image_path = os.path.join(SHINY_SPRITES_DIR, f"{pokemon_id}.png")

        # Download in background (parallelized by gather in fetch_species_data)
        await asyncio.gather(
            download_image(client, original_image_url, local_image_path),
            download_image(client, original_shiny_image_url, local_shiny_image_path)
        )

        # Store local URL for frontend
        image_url = f"/static/sprites/{pokemon_id}.png"
        shiny_image_url = f"/static/sprites/shiny/{pokemon_id}.png"

        return Pokemon(
            id=pokemon_id,
            name=german_name,
            name_en=english_name,
            generation=generation,
            image_url=image_url,
            shiny_image_url=shiny_image_url
        )
    except Exception as e:
        print(f"Error fetching variety {variety_data['pokemon']['name']}: {e}")
        return None


async def fetch_species_data(client, species_url):
    try:
        response = await client.get(species_url)
        species_data = response.json()
        species_id = species_data["id"]

        # Determine Generation
        gen_url = species_data.get("generation", {}).get("url", "")
        default_gen = int(gen_url.split("/")[-2]) if gen_url else get_generation_by_id(species_id)

        names = species_data["names"]
        varieties = species_data["varieties"]

        tasks = [fetch_pokemon_variety(client, v, names, default_gen) for v in varieties]
        return await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error fetching species {species_url}: {e}")
        return []


async def seed_pokemon_async(progress_callback=None):
    # Create tables if they don't exist (idempotent)
    create_db_and_tables()

    if progress_callback:
        await progress_callback(0, 100, "status_init")

    async with httpx.AsyncClient(timeout=30.0) as client:
        print("Fetching Pokemon species list...")
        if progress_callback:
            await progress_callback(5, 100, "status_fetching_species")
            
        url = "https://pokeapi.co/api/v2/pokemon-species?limit=1025"
        response = await client.get(url)
        base_data = response.json()
        results = base_data.get("results", [])

        total_species = len(results)
        print(f"Found {total_species} species. Starting parallel fetch...")

        batch_size = 50
        all_pokemon = []

        for i in range(0, total_species, batch_size):
            batch = results[i:i + batch_size]
            tasks = [fetch_species_data(client, item["url"]) for item in batch]

            batch_results = await asyncio.gather(*tasks)
            for species_varieties in batch_results:
                for p in species_varieties:
                    if p:
                        all_pokemon.append(p)
            
            # Calculate progress (10% to 90% reserved for fetching)
            current_progress = 10 + int((min(i + batch_size, total_species) / total_species) * 80)
            if progress_callback:
                # Send key with dynamic data separated by |
                await progress_callback(current_progress, 100, f"status_fetched_varieties|{len(all_pokemon)}")

            print(f"Processed {min(i + batch_size, total_species)}/1025 species...")

        if progress_callback:
            await progress_callback(90, 100, "status_updating_db")

        with Session(engine) as session:
            print(f"Upserting {len(all_pokemon)} Pokemon entries to database...")
            
            # Fetch existing IDs to decide between insert and update
            # Note: For strict correctness/speed in huge datasets, we'd use bulk operations or ON CONFLICT.
            # But here we iterate to keep it simple with SQLModel.
            
            for p in all_pokemon:
                existing_pokemon = session.get(Pokemon, p.id)
                if existing_pokemon:
                    # Update fields
                    existing_pokemon.name = p.name
                    existing_pokemon.name_en = p.name_en
                    existing_pokemon.generation = p.generation
                    existing_pokemon.image_url = p.image_url
                    existing_pokemon.shiny_image_url = p.shiny_image_url
                    session.add(existing_pokemon)
                else:
                    # Insert new
                    session.add(p)
            
            session.commit()
            
    if progress_callback:
        await progress_callback(100, 100, "status_complete")

    print("Seeding complete! User progress preserved.")


if __name__ == "__main__":
    asyncio.run(seed_pokemon_async())
