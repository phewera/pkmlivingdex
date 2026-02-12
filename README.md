# Pokémon Living Dex Tracker

A modern web application to track your progress in building a "Living Dex" (collecting every Pokémon).

## Features

- **Comprehensive Tracking**: Track both Normal and Shiny variants for all Pokémon generations.
- **Generation Filtering**: View progress for specific generations or all at once.
- **Statistics**: Detailed statistics on capture progress, including shiny collection rates.
- **Manual Database Update:** Trigger a refresh of Pokemon data from PokeAPI directly via the Settings menu.
- **Future-Proof Generations:** Automatically detects and displays new Pokemon generations from the database/PokeAPI without requiring application updates. Simply run the "Database Update" to fetch them.
- **Import/Export**: Backup and restore your collection data easily via CSV files.
- **Progress Reset**: Reset your entire progress if you want to start fresh.
- **Offline Support**: Caches Pokémon sprites for offline viewing after initial load.
- **Multi-language**: Supports both English and German (switchable in settings).
- **Search & Filter**: Quickly find Pokémon by name or ID, and filter by "Missing" or "Shiny Missing".
- **Responsive Design**: Optimization for both desktop and mobile usage.

## Screenshots

### Desktop View
<p align="center">
  <a href="screenshots/desktop_collection_view_1.png"><img src="screenshots/desktop_collection_view_1.png" alt="Desktop Collection View 1" width="45%"></a>
  <a href="screenshots/desktop_collection_view_2.png"><img src="screenshots/desktop_collection_view_2.png" alt="Desktop Collection View 2" width="45%"></a>
</p>

### Management & Statistics
<p align="center">
  <a href="screenshots/desktop_settings_view.png"><img src="screenshots/desktop_settings_view.png" alt="Settings Modal" width="45%"></a>
  <a href="screenshots/desktop_statistics_view.png"><img src="screenshots/desktop_statistics_view.png" alt="Statistics Modal" width="45%"></a>
</p>

### Mobile View
<p align="center">
  <a href="screenshots/mobile_collection_view_1.png"><img src="screenshots/mobile_collection_view_1.png" alt="Mobile Collection View 1" width="30%"></a>
  <a href="screenshots/mobile_collection_view_2.png"><img src="screenshots/mobile_collection_view_2.png" alt="Mobile Collection View 2" width="30%"></a>
</p>

## Getting Started

Follow these instructions to start the application locally.

### Prerequisites
- Python 3.8+
- Node.js 16+

### 1. Backend Setup
The backend is built with FastAPI.

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn main:app --reload
```
*The API will be available at http://127.0.0.1:8000*

### 2. Frontend Setup
The frontend is built with React and Vite.

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev

# Or run in production mode
npm run build
npm run preview
```
*The application will optionally run at http://localhost:5173*

### 3. Deployment (Frontend)
To deploy the frontend to a static host (e.g., Vercel, Netlify, GitHub Pages, or a web server like Nginx):

1. **Build the application**:
   ```bash
   npm run build
   ```
   This creates a `dist` folder containing the compiled assets.

2. **Upload/Serve the `dist` folder**:
   - **Static Host**: Point your hosting service to the `dist` directory.
   - **Web Server**: Copy the contents of `dist` to your server's public web folder.

*Note: Ensure your frontend is configured to communicate with the production URL of your backend API.*

### 4. Docker Setup

You have two options for running with Docker:

#### Option A: Local Development (Build from Disk)
Use this if you want to test changes locally before pushing to GitHub.
1.  **Build and Start**:
    ```bash
    docker compose up --build -d
    ```
2.  **Access**: [http://localhost](http://localhost) (or [http://pokemon.local](http://pokemon.local))

#### Option B: Production (Pull from GitHub)
Use this for the final "product" installation. It pulls the latest code directly from the GitHub repository.

1.  **Build the Image**:
    ```bash
    # Build a specific version (e.g., v1.0.0) or branch (main)
    docker build -f Dockerfile.prod -t pkmlivingdex --build-arg APP_VERSION=v1.0.0 .
    ```
    *If no version is specified, it defaults to `main`.*

2.  **Run the Container**:
    ```bash
    docker run -d -p 80:80 --name pkmlivingdex pkmlivingdex
    ```

3.  **Access**: [http://localhost](http://localhost) (or [http://pokemon.local](http://pokemon.local))

#### Stopping
- For Option A: `docker compose down`
- For Option B: `docker rm -f pkmlivingdex`

## Custom Domain Setup

To access the app via a custom domain like `http://pokemon.local`:

1.  **Edit Hosts File:**
    - Open Notepad as Administrator.
    - Open `C:\Windows\System32\drivers\etc\hosts`.
    - Add the following line at the end:
        ```
        127.0.0.1 pokemon.local
        ```
    - Save the file.

2.  **Access:**
    - You can now access the app at [http://pokemon.local](http://pokemon.local).

## Running Tests

Unit tests are provided for the backend logic.

```bash
# Ensure you are in the backend directory and your venv is activated
cd backend
venv\Scripts\activate

# Run tests using pytest
python -m pytest
```

## Troubleshooting
### Windows: Script Execution Disabled
If you see an error like `cannot be loaded because running scripts is disabled on this system`, you need to update your PowerShell execution policy. Run this command in PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
```

Then try activating the virtual environment again:
```bash
venv\Scripts\activate
```

Alternatively, you can run the commands directly using the virtual environment's Python executable without activating it first:

```bash
# Run server
venv\Scripts\python -m uvicorn main:app --reload

# Run tests
venv\Scripts\python -m pytest
```

## Credits

- **[PokeAPI](https://pokeapi.co/)**: Huge thanks to PokeAPI for providing the extensive Pokémon data, sprites, and information used in this project.
