# AAROHAN BGMI ELIMS - Points Table System

A beautiful web-based points table system for AAROHAN BGMI Tournament with 3 groups.

## Features

- ✨ Modern minimalistic dark design with blue accents
- 🎮 Custom AAROHAN branding and logo
- 📊 Separate points tables for 3 groups (A, B, C)
- 🎮 Easy match data entry with auto-complete
- 💾 Automatic data saving for each match
- 🏆 Combined leaderboard across all groups
- 📱 Responsive design for mobile and desktop
- 📄 PDF export for all leaderboards

## Quick Start

### Option 1: Run with start.bat
Simply double-click `start.bat` to install dependencies and start the server.

### Option 2: Manual Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## How to Use

1. **Dashboard**: View overview of all groups and match counts
2. **Add Match Data**: Enter results for each match (team names and kills)
3. **View Standings**: Check individual group leaderboards
4. **Combined Leaderboard**: See overall rankings across all groups

## Groups

- **Group A**: 16 teams
- **Group B**: 16 teams  
- **Group C**: 15 teams

## Point System

Official BGMI point system:
- Rank 1: 10 points + WWCD
- Rank 2: 6 points
- Rank 3: 5 points
- Rank 4: 4 points
- Rank 5: 3 points
- Rank 6: 2 points
- Rank 7-8: 1 point each
- Plus kills for additional points

## Data Storage

Match data is stored in separate folders:
- `Group_A_Data/` - All Group A match CSV files
- `Group_B_Data/` - All Group B match CSV files
- `Group_C_Data/` - All Group C match CSV files

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Data**: Pandas, CSV storage
- **PDF Generation**: ReportLab
- **Design**: GitHub-style dark theme with modern UI

## Features

✅ Individual group leaderboards
✅ Combined rankings
✅ Match-by-match tracking
✅ Automatic point calculation
✅ WWCD tracking
✅ Tie-breaker rules (Total → Kills → WWCD)
✅ Beautiful responsive design
✅ Real-time updates
✅ PDF export functionality

## Deployment

### Deploy to Render (Recommended - Free)

1. Fork/Push this repository to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `aarohan-bgmi-points`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Add to requirements.txt: `gunicorn`
7. Click "Create Web Service"

### Deploy to Railway (Alternative - Free)

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Railway auto-detects Flask and deploys
6. Add environment variable: `PORT=5000`

### Deploy to PythonAnywhere (Free Tier Available)

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your code or clone from GitHub
3. Create a virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements.txt
   ```
4. Configure WSGI file:
   ```python
   import sys
   path = '/home/yourusername/bgmi-points-table'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```
5. Reload the web app

### Deploy to Heroku

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Add `gunicorn` to requirements.txt
4. Deploy:
   ```bash
   heroku create aarohan-bgmi-points
   git push heroku main
   ```

### Local Development with Production Settings

For production environments, add `gunicorn` to requirements.txt:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

Run with Gunicorn:
```bash
gunicorn app:app --bind 0.0.0.0:5000
```

## Environment Variables (Production)

For production deployment, you may want to set:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secret-key-here`
- `PORT=5000` (or as required by hosting platform)

---

Created for AAROHAN BGMI ELIMS Tournament

