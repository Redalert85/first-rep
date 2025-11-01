# 🖥️ Run MBE Study System on Your MacBook

## Quick Setup for macOS

### Step 1: Clone/Download the Repository

If you haven't already, get the code on your Mac:

```bash
# If you have git
cd ~/Documents
git clone https://github.com/Redalert85/first-rep.git
cd first-rep

# OR download the ZIP from GitHub and extract it
```

### Step 2: Navigate to web directory

```bash
cd web
```

### Step 3: Install Prerequisites (One-time setup)

#### Install Homebrew (if not installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Install Python 3:
```bash
brew install python@3.11
```

#### Install Node.js:
```bash
brew install node
```

### Step 4: Start the Application

```bash
chmod +x start.sh
./start.sh
```

The script will:
- Create Python virtual environment
- Install backend dependencies
- Start Flask server on port 5000
- Install frontend dependencies
- Start Vite dev server on port 3000

### Step 5: Open in Browser

Open Safari or Chrome:
```
http://localhost:3000
```

---

## Manual Setup (if start.sh doesn't work)

### Terminal 1 - Backend:

```bash
cd web/backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install Flask Flask-CORS Flask-Session python-dotenv

# Run server
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Terminal 2 - Frontend:

Open a NEW terminal tab/window:

```bash
cd web/frontend

# Install dependencies (one time)
npm install

# Run development server
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:3000/
```

### Open Browser:

```
http://localhost:3000
```

---

## Troubleshooting on Mac

### Port 5000 already in use:

macOS AirPlay uses port 5000. Disable it:
1. System Preferences → Sharing
2. Uncheck "AirPlay Receiver"

Or use different port - edit `web/backend/app.py`:
```python
app.run(port=5001)  # Change from 5000 to 5001
```

### Python not found:

```bash
# Check Python
python3 --version

# If missing, install:
brew install python@3.11
```

### Node not found:

```bash
# Check Node
node --version

# If missing, install:
brew install node
```

### Permission errors:

```bash
# Don't use sudo, use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Success! 🎉

Once both servers are running:
1. Backend: http://localhost:5000 ✅
2. Frontend: http://localhost:3000 ✅

Open **http://localhost:3000** in your browser to use the app!

---

## Quick Commands Reference

### Start Everything:
```bash
cd ~/Documents/first-rep/web
./start.sh
```

### Stop Everything:
Press `Ctrl+C` in the terminal

### Check if servers are running:
```bash
# Check backend
curl http://localhost:5000/api/health

# Check frontend (open in browser)
open http://localhost:3000
```

---

## Need Help?

Common issues:
- **Port 5000 busy:** Disable AirPlay or use port 5001
- **npm install fails:** Clear cache: `npm cache clean --force`
- **Python errors:** Use virtual environment: `python3 -m venv venv && source venv/bin/activate`

---

**Ready to study! 📚✨**
