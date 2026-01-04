# How to Run Backend and Frontend - Detailed Guide

This guide provides step-by-step instructions for running the Nexora SaaS backend and frontend locally.

---

## 📋 Prerequisites

Before running the application, ensure you have:

1. **Python 3.11+** installed
   - Check: `python --version` or `python -V`
   - Download: https://www.python.org/downloads/

2. **Node.js 18+ and npm** installed
   - Check: `node --version` and `npm --version`
   - Download: https://nodejs.org/

3. **Git** (optional, for cloning repositories)

---

## 🔧 Setup Instructions

### Step 1: Navigate to Project Directory

Open a terminal (PowerShell, Command Prompt, or Terminal) and navigate to the project root:

```bash
cd C:\Users\KIIT01\Nexora-Intelligence-Engine-2
```

### Step 2: Environment Files Setup

#### Backend Environment File

Create `backend/.env.local` file with the following content:

```bash
# Supabase Configuration
SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
SUPABASE_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnaHlwc25meWx4dmF6a2RpbHhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzMyMzE4NiwiZXhwIjoyMDgyODk5MTg2fQ.ZBbeLj5fZTTba29I08lZkv7srcbOgGjPEYhrsn1CCaw

# Dodo Payments Configuration
DODO_API_KEY=ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt
DODO_WEBHOOK_SECRET=whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz
DODO_PRODUCT_BRIEF=pdt_0NVOawMXoMB75Xo8Dbmbo
DODO_ENVIRONMENT=live_mode
DODO_API_URL=https://api.dodopayments.com
BRIEF_PRICE_USD=3.00

# App Configuration
ENVIRONMENT=development
DEBUG=true
API_URL=http://localhost:8000

# CORS (comma-separated, no spaces)
CORS_ORIGINS=http://localhost:3000
```

**Note**: The `.env.local` file should already exist. If not, create it in the `backend` directory.

#### Frontend Environment File

Create `frontend/.env.local` file with the following content:

```bash
NEXT_PUBLIC_SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Note**: The `.env.local` file should already exist. If not, create it in the `frontend` directory.

---

## 🚀 Running the Backend (FastAPI)

### Option 1: Run Backend Only

1. **Open a terminal/command prompt**

2. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

3. **Install Python dependencies (first time only):**
   ```bash
   python -m pip install -r requirements.txt
   ```
   
   Or if you have `pip` directly:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server:**
   ```bash
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

5. **Verify backend is running:**
   - Open browser: http://localhost:8000/health
   - Should return: `{"status":"healthy"}`
   - API Docs: http://localhost:8000/docs

### Backend Server Details

- **URL**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Host**: 127.0.0.1 (localhost)
- **Port**: 8000
- **Auto-reload**: Enabled (--reload flag)

**Note**: Keep this terminal window open. The server will restart automatically when you make code changes.

---

## 🎨 Running the Frontend (Next.js)

### Option 1: Run Frontend Only

1. **Open a NEW terminal/command prompt** (keep backend running in the first terminal)

2. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

3. **Install Node dependencies (first time only):**
   ```bash
   npm install
   ```
   
   This may take 2-5 minutes on first run.

4. **Start the frontend development server:**
   ```bash
   npm run dev
   ```

5. **Wait for compilation:**
   - You'll see compilation messages
   - Wait for: `✓ Ready on http://localhost:3000`
   - This typically takes 10-30 seconds

6. **Open the application:**
   - Open browser: http://localhost:3000
   - The app should load

### Frontend Server Details

- **URL**: http://localhost:3000
- **Host**: localhost
- **Port**: 3000
- **Hot Reload**: Enabled (changes refresh automatically)

**Note**: Keep this terminal window open. The app will auto-reload when you make changes.

---

## 🔥 Running Both Together

### Method 1: Using Batch Script (Windows)

1. **Double-click `start-dev.bat`** in the project root, OR

2. **Run from terminal:**
   ```bash
   start-dev.bat
   ```

This will open two separate command windows:
- One for backend (port 8000)
- One for frontend (port 3000)

**To stop**: Close both command windows.

### Method 2: Manual (Two Terminals)

1. **Terminal 1 - Backend:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Terminal 2 - Frontend (in a new terminal):**
   ```bash
   cd frontend
   npm run dev
   ```

### Method 3: Using PowerShell Script

1. **Run from PowerShell:**
   ```powershell
   .\run-both.ps1
   ```

---

## ✅ Verification Checklist

After starting both services, verify:

- [ ] Backend health check: http://localhost:8000/health returns `{"status":"healthy"}`
- [ ] Backend API docs: http://localhost:8000/docs loads successfully
- [ ] Frontend loads: http://localhost:3000 shows the application
- [ ] No errors in terminal/console windows
- [ ] Both services are running in separate windows/terminals

---

## 🛑 Stopping the Servers

### Method 1: Close Terminal Windows
- Simply close the terminal/command prompt windows running the servers
- Or press `Ctrl+C` in each terminal window

### Method 2: Stop Processes (if windows are closed)

**Windows (PowerShell):**
```powershell
Get-Process python,node -ErrorAction SilentlyContinue | Stop-Process -Force
```

**Windows (Command Prompt):**
```bash
taskkill /F /IM python.exe /IM node.exe
```

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError` or import errors
- **Solution**: Install dependencies: `pip install -r requirements.txt`

**Problem**: `pydantic_settings.sources.SettingsError` or environment variable errors
- **Solution**: Ensure `backend/.env.local` file exists and has all required variables

**Problem**: Port 8000 already in use
- **Solution**: 
  - Change port: `--port 8001` (and update CORS_ORIGINS if needed)
  - Or stop the process using port 8000

**Problem**: `python: command not found`
- **Solution**: Install Python or use `python3` instead of `python`

### Frontend Issues

**Problem**: `npm: command not found`
- **Solution**: Install Node.js from https://nodejs.org/

**Problem**: `npm install` fails or takes too long
- **Solution**: 
  - Clear npm cache: `npm cache clean --force`
  - Delete `node_modules` and `package-lock.json`, then run `npm install` again

**Problem**: Port 3000 already in use
- **Solution**: 
  - Next.js will automatically use port 3001, 3002, etc.
  - Or specify port: `npm run dev -- -p 3001`

**Problem**: Build errors or compilation failures
- **Solution**: 
  - Check for syntax errors in code
  - Delete `.next` folder and restart: `rm -r .next` (Linux/Mac) or `rmdir /s .next` (Windows)
  - Run: `npm run dev` again

**Problem**: "Conflicting app and page file" error
- **Solution**: This should already be fixed. If you see it, ensure `pages/index.tsx` doesn't exist (only `app/page.tsx` should exist)

### Connection Issues

**Problem**: Frontend can't connect to backend
- **Solution**: 
  - Ensure backend is running on http://localhost:8000
  - Check `frontend/.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`
  - Check browser console for CORS errors
  - Verify backend CORS_ORIGINS includes `http://localhost:3000`

**Problem**: API calls return 401/403 errors
- **Solution**: This is normal if you're not authenticated. Sign up/login first.

---

## 📝 Quick Reference Commands

### Backend Commands
```bash
# Navigate to backend
cd backend

# Install dependencies (first time)
pip install -r requirements.txt

# Run server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Run without auto-reload (production-like)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend Commands
```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time)
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Lint code
npm run lint
```

---

## 🌐 Access URLs

Once both services are running:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application |
| **Backend API** | http://localhost:8000 | API endpoints |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation (Swagger) |
| **Health Check** | http://localhost:8000/health | Backend health status |

---

## 💡 Tips

1. **Keep terminals open**: Both services need to keep running
2. **Check terminal output**: Errors and logs appear in the terminal windows
3. **Auto-reload**: Both servers auto-reload on code changes (no manual restart needed)
4. **First run is slower**: Initial `npm install` and Next.js compilation take time
5. **Use separate terminals**: Run backend and frontend in separate terminal windows for better visibility
6. **Bookmark URLs**: Save http://localhost:3000 and http://localhost:8000/docs for quick access

---

## 🎯 Summary

1. **Setup**: Create `.env.local` files in both `backend` and `frontend` directories
2. **Backend**: `cd backend` → `pip install -r requirements.txt` → `python -m uvicorn app.main:app --reload`
3. **Frontend**: `cd frontend` → `npm install` → `npm run dev`
4. **Access**: Open http://localhost:3000 in your browser
5. **Stop**: Close terminal windows or press `Ctrl+C`

---

**Need Help?** Check the terminal output for specific error messages and refer to the troubleshooting section above.

