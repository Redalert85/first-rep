# 🚀 Quick Start - macOS

## For Your MacBook

### 1️⃣ Open Terminal on your Mac

### 2️⃣ Navigate to project:
```bash
cd ~/Documents/first-rep/web
# (or wherever you cloned/downloaded this)
```

### 3️⃣ Make script executable (first time only):
```bash
chmod +x start.sh
```

### 4️⃣ Run the app:
```bash
./start.sh
```

### 5️⃣ Open browser:
```
http://localhost:3000
```

---

## ⚠️ Common macOS Issue

**Port 5000 Conflict with AirPlay:**

If you see "Port 5000 already in use":

**Option A:** Disable AirPlay (Recommended)
```
System Preferences → Sharing → Uncheck "AirPlay Receiver"
```

**Option B:** Use different port

Edit `backend/app.py`, change line:
```python
app.run(port=5001)  # Changed from 5000
```

Then in `frontend/vite.config.js`, update:
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:5001',  // Changed from 5000
  }
}
```

---

## ✅ Success Signs

Backend running:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

Frontend running:
```
  VITE ready in XXX ms
  ➜  Local:   http://localhost:3000/
```

---

**Now open http://localhost:3000 and start studying! 📚**
