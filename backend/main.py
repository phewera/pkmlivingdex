import csv
import io
import os
import logging
from datetime import datetime
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Pokemon, UserProgress, PokemonResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Mount static files for sprites
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Pokemon Living Dex API is running"}

@app.get("/pokemon", response_model=List[PokemonResponse])
def read_pokemon(generation: Optional[int] = None, session: Session = Depends(get_session)):
    """Fetch list of Pokemon, optionally filtered by generation."""
    # Efficient query with join
    statement = select(Pokemon, UserProgress).outerjoin(UserProgress, Pokemon.id == UserProgress.pokemon_id)
    
    if generation:
        statement = statement.where(Pokemon.generation == generation)
    
    results = session.exec(statement).all()
    
    response = []
    for pokemon, progress in results:
        # Create response object, defaulting to False if no progress record found
        p_res = PokemonResponse(
            **pokemon.model_dump(),
            caught_normal=progress.caught_normal if progress else False,
            caught_shiny=progress.caught_shiny if progress else False
        )
        response.append(p_res)
        
    return response


@app.post("/pokemon/{pokemon_id}/capture")
def update_capture_status(
    pokemon_id: int, 
    caught_normal: Optional[bool] = None, 
    caught_shiny: Optional[bool] = None, 
    session: Session = Depends(get_session)
):
    progress = session.exec(select(UserProgress).where(UserProgress.pokemon_id == pokemon_id)).first()
    if not progress:
        # Should ideally exist if seeded, but create if needed
        progress = UserProgress(pokemon_id=pokemon_id)
        session.add(progress)
    
    if caught_normal is not None:
        progress.caught_normal = caught_normal
    if caught_shiny is not None:
        progress.caught_shiny = caught_shiny
    
    session.add(progress)
    session.commit()
    session.refresh(progress)
    return progress


@app.post("/progress/reset")
def reset_progress(session: Session = Depends(get_session)):
    progress_items = session.exec(select(UserProgress)).all()
    for item in progress_items:
        session.delete(item)
    session.commit()
    return {"message": "All progress reset successfully"}


@app.get("/stats")
def get_stats(session: Session = Depends(get_session)):
    # Group by generation
    # Simplified stats for now: just counts per generation
    # Alternatively, fetch all and calculate in frontend, but backend is better
    
    gens = session.exec(select(Pokemon.generation).distinct()).all()
    stats = []
    
    for gen in gens:
        total = session.exec(select(Pokemon).where(Pokemon.generation == gen)).all()
        total_count = len(total)
        
        # Count progress via join
        caught_normal_count = 0
        caught_shiny_count = 0
        
        # A more efficient query exists, but iterating is fine for < 100 per gen
        # Let's do a join count for better performance
        # Count where generation matches AND caught is true
        
        # This is getting complex in raw SQLModel/SQLAlchemy core, simplified loop for now
        # Actually proper query:
        # session.query(func.count(UserProgress.id)).join(Pokemon).filter(Pokemon.generation == gen, UserProgress.caught_normal == True).scalar()
        
        pokes_in_gen = session.exec(select(UserProgress).join(Pokemon).where(Pokemon.generation == gen)).all()
        
        caught_any = sum(1 for p in pokes_in_gen if p.caught_normal or p.caught_shiny)
        caught_normal = sum(1 for p in pokes_in_gen if p.caught_normal)
        caught_shiny = sum(1 for p in pokes_in_gen if p.caught_shiny)
        
        stats.append({
            "generation": gen,
            "total": total_count,
            "caught_any": caught_any,
            "caught_normal": caught_normal,
            "caught_shiny": caught_shiny,
            "percentage_any": round((caught_any / total_count) * 100, 1) if total_count > 0 else 0,
            "percentage_normal": round((caught_normal / total_count) * 100, 1) if total_count > 0 else 0,
            "percentage_shiny": round((caught_shiny / total_count) * 100, 1) if total_count > 0 else 0
        })
            
    return stats


@app.get("/export/csv")
def export_progress(session: Session = Depends(get_session)):
    # Fetch all progress
    statement = select(Pokemon.name, UserProgress.caught_normal, UserProgress.caught_shiny).outerjoin(UserProgress, Pokemon.id == UserProgress.pokemon_id)
    results = session.exec(statement).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Pokemon", "Caught Normal", "Caught Shiny"])
    
    for name, normal, shiny in results:
        writer.writerow([name, 1 if normal else 0, 1 if shiny else 0])
    
    output.seek(0)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pokemon_progress_{timestamp}.csv"
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.post("/import/csv")
async def import_progress(file: UploadFile = File(...), session: Session = Depends(get_session)):
    content = await file.read()
    decoded = content.decode("utf-8")
    stream = io.StringIO(decoded)
    reader = csv.DictReader(stream)
    
    # Pre-fetch all pokemon and progress records to optimize
    all_pokemon = {p.name: p.id for p in session.exec(select(Pokemon)).all()}
    all_progress = {pr.pokemon_id: pr for pr in session.exec(select(UserProgress)).all()}
    
    count = 0
    for row in reader:
        pokemon_name = row.get("Pokemon")
        caught_normal = row.get("Caught Normal") == "1"
        caught_shiny = row.get("Caught Shiny") == "1"
        
        if not pokemon_name:
            continue
            
        pokemon_id = all_pokemon.get(pokemon_name)
        if pokemon_id:
            progress = all_progress.get(pokemon_id)
            if not progress:
                progress = UserProgress(pokemon_id=pokemon_id)
                session.add(progress)
            
            progress.caught_normal = caught_normal
            progress.caught_shiny = caught_shiny
            count += 1
            
    session.commit()
    session.commit()
    return {"status": "success", "count": count}


# --- System Update Endpoints ---

from fastapi import BackgroundTasks
from seed import seed_pokemon_async

# Global status object (simple in-memory state)
UPDATE_STATUS = {
    "state": "idle", # idle, running, complete, error
    "progress": 0,
    "current": 0,
    "total": 100,
    "message": ""
}

async def run_update_task():
    global UPDATE_STATUS
    UPDATE_STATUS["state"] = "running"
    UPDATE_STATUS["progress"] = 0
    UPDATE_STATUS["message"] = "Starting update..."
    
    async def progress_callback(current, total, message):
        UPDATE_STATUS["current"] = current
        UPDATE_STATUS["total"] = total
        UPDATE_STATUS["progress"] = int((current / total) * 100) if total > 0 else 0
        UPDATE_STATUS["message"] = message
        
    try:
        await seed_pokemon_async(progress_callback)
        UPDATE_STATUS["state"] = "complete"
        UPDATE_STATUS["progress"] = 100
        UPDATE_STATUS["message"] = "Update complete!"
    except Exception as e:
        UPDATE_STATUS["state"] = "error"
        UPDATE_STATUS["message"] = str(e)
        logging.error(f"Update failed: {e}")

@app.post("/system/update-database")
async def start_database_update(background_tasks: BackgroundTasks):
    if UPDATE_STATUS["state"] == "running":
        return {"status": "already_running", "message": "Update is already in progress"}
    
    background_tasks.add_task(run_update_task)
    return {"status": "started", "message": "Database update started in background"}

@app.get("/system/update-status")
def get_update_status():
    return UPDATE_STATUS


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

