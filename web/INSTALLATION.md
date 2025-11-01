# 🚀 Installation & Setup Guide

## Prerequisites Check

Before you begin, make sure you have:

- [ ] **Python 3.8 or higher**
  ```bash
  python3 --version
  ```

- [ ] **Node.js 16 or higher**
  ```bash
  node --version
  ```

- [ ] **npm** (comes with Node.js)
  ```bash
  npm --version
  ```

---

## 📦 Installation

### Method 1: Automated (Recommended)

**Single command to start everything:**

```bash
cd web
chmod +x start.sh  # Make script executable (one time only)
./start.sh
```

This will:
1. ✅ Create Python virtual environment
2. ✅ Install backend dependencies
3. ✅ Start Flask server on port 5000
4. ✅ Install frontend dependencies
5. ✅ Start Vite dev server on port 3000

**Then open:** http://localhost:3000

---

### Method 2: Manual Setup

#### Step 1: Backend Setup

```bash
# Navigate to backend
cd web/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
python app.py
```

✅ Backend running on **http://localhost:5000**

#### Step 2: Frontend Setup (New Terminal)

```bash
# Navigate to frontend
cd web/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

✅ Frontend running on **http://localhost:3000**

---

## 🧪 Verify Installation

### 1. Check Backend Health

Open in browser or use curl:
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-...",
  "version": "1.0.0"
}
```

### 2. Check Frontend

Open browser: http://localhost:3000

You should see the MBE Study System dashboard.

### 3. Test API Connection

In the browser console (F12):
```javascript
fetch('http://localhost:5000/api/subjects')
  .then(r => r.json())
  .then(console.log)
```

Should return list of subjects.

---

## 🐛 Troubleshooting

### Problem: Port 5000 already in use

**Solution:**
```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9

# Or use different port
# Edit web/backend/app.py, change:
app.run(port=5001)
```

### Problem: Port 3000 already in use

**Solution:**
```bash
# Find and kill process
lsof -ti:3000 | xargs kill -9

# Or Vite will automatically suggest port 3001
```

### Problem: Python not found

**Solution:**
```bash
# Try python instead of python3
python --version

# Or install Python 3.8+
# macOS:
brew install python@3.11

# Ubuntu/Debian:
sudo apt-get install python3.11
```

### Problem: Node not found

**Solution:**
```bash
# Install Node.js
# macOS:
brew install node

# Ubuntu/Debian:
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Problem: npm install fails

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and try again
cd web/frontend
rm -rf node_modules package-lock.json
npm install
```

### Problem: Backend dependencies fail

**Solution:**
```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall
cd web/backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: CORS errors in browser console

**Solution:**

1. Verify backend is running on port 5000
2. Check `web/frontend/vite.config.js`:
   ```javascript
   proxy: {
     '/api': {
       target: 'http://localhost:5000',
       changeOrigin: true
     }
   }
   ```
3. Restart both servers

### Problem: "Cannot find module" errors

**Solution:**
```bash
# Backend
cd web/backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd web/frontend
npm install
```

---

## 🔒 Environment Variables (Optional)

### Backend (.env file)

Create `web/backend/.env`:
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### Frontend (.env file)

Create `web/frontend/.env`:
```env
VITE_API_URL=http://localhost:5000
```

---

## 📱 First Time Usage

### 1. Explore the Dashboard

- View overall statistics
- Check available subjects
- See quick action cards

### 2. Create a Flashcard

- Click "Flashcards" in navigation
- Click "Create Flashcard"
- Fill in front/back
- Choose subject
- Save

### 3. Start Practice Session

- Click "Practice" in navigation
- Select subject (e.g., Contracts)
- Choose difficulty
- Set number of questions (5 recommended)
- Click "Start Practice Session"

### 4. Review Progress

- Click "Progress" in navigation
- View charts and analytics
- See subject breakdown

### 5. Study Materials

- Click "Materials" in navigation
- Select a subject (e.g., Property)
- Browse outlines, flowcharts, tables

---

## 🚀 Running in Production

### Build Frontend for Production

```bash
cd web/frontend
npm run build
```

This creates an optimized `dist/` folder.

### Deploy Backend (Example: Heroku)

```bash
cd web/backend

# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Install gunicorn
pip install gunicorn
pip freeze > requirements.txt

# Deploy
git push heroku main
```

### Deploy Frontend (Example: Vercel)

```bash
cd web/frontend
npm run build
vercel deploy dist/
```

---

## 📊 Monitoring

### Check Backend Logs

```bash
cd web/backend
tail -f ../../bar_tutor.log
```

### Check Frontend Dev Server

Vite shows logs in the terminal where you ran `npm run dev`.

---

## 🔄 Updating

### Update Backend Dependencies

```bash
cd web/backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Update Frontend Dependencies

```bash
cd web/frontend
npm update
```

---

## 🛑 Stopping the Application

### If using start.sh

Press `Ctrl+C` in the terminal where `start.sh` is running.

### If manual setup

Press `Ctrl+C` in both terminal windows (backend and frontend).

---

## ✅ Success Checklist

- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Dashboard loads with stats
- [ ] Can navigate between pages
- [ ] API health check returns "healthy"
- [ ] No errors in browser console

---

## 🎉 You're Ready!

The MBE Study System web application is now installed and running!

**Next Steps:**
1. Create your first flashcard
2. Start a practice session
3. Track your progress
4. Review study materials

**Need Help?**
- Check `web/README.md` for API documentation
- See `web/WEB_APP_GUIDE.md` for feature details
- Review troubleshooting section above

---

**Happy Studying! 📚✨**
