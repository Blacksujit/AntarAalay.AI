# AntarAalay.ai - Deployment Guide

## Prerequisites

- Docker installed
- Firebase project with Authentication & Storage enabled
- Supabase account with PostgreSQL database
- Stability AI API key (for Stable Diffusion)

## Architecture

**Backend Stack:**
- Python 3.11 + FastAPI
- PostgreSQL (Supabase)
- Firebase Storage (image uploads)
- Firebase Auth (authentication)

**Frontend Stack:**
- Vite + React + TypeScript
- Tailwind CSS
- Zustand + React Query

## Quick Start - Docker Compose

```bash
# Clone repo
git clone https://github.com/yourusername/AntarAalay.ai.git
cd AntarAalay.ai

# Create .env file
cp Backend/.env.example .env
# Edit .env with your credentials

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f backend
```

## Backend Deployment (Render)

### 1. Environment Variables

Create `.env` file:
```
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_API_KEY=your-firebase-api-key
STABLE_DIFFUSION_API_KEY=your-stability-api-key
```

### 2. Deploy to Render

1. Create new **Web Service** on Render
2. Connect your GitHub repo
3. Set environment variables (copy from .env)
4. Build command: `pip install -r Backend/requirements.txt`
5. Start command: `cd Backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Frontend Deployment (Vercel)

### 1. Environment Setup

Create `.env.local`:
```
VITE_FIREBASE_API_KEY=...
VITE_FIREBASE_PROJECT_ID=...
VITE_API_URL=https://your-backend-url.onrender.com
```

### 2. Deploy

```bash
cd Frontend
npm install
vercel --prod
```

Or connect GitHub repo to Vercel for auto-deploy.

## Database Setup (Supabase)

1. Create new project at supabase.com
2. Go to **Database** → **New table**
3. Run migrations (or use SQL):
```sql
-- Users table
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    photo_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);

-- Rooms table
CREATE TABLE rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    room_type TEXT NOT NULL,
    direction TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);

-- Designs table
CREATE TABLE designs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    style TEXT NOT NULL,
    budget INTEGER,
    image_1_url TEXT,
    image_2_url TEXT,
    image_3_url TEXT,
    estimated_cost FLOAT,
    budget_match_percentage FLOAT,
    furniture_breakdown JSONB,
    vastu_score INTEGER,
    vastu_suggestions JSONB,
    vastu_warnings JSONB,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

## Firebase Setup

### 1. Authentication
1. Go to Firebase Console → Authentication
2. Enable **Google** sign-in
3. Add authorized domains (localhost, your-vercel-domain)

### 2. Storage
1. Go to Storage
2. Create bucket (default: `{project-id}.appspot.com`)
3. Set rules:
```rules
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

### 3. Get Credentials
1. Project Settings → General → Project ID
2. Project Settings → Service Accounts → Generate new private key (for backend)

## Post-Deployment Checklist

- [ ] Backend health check: `GET /health` returns 200
- [ ] Database connected (no errors in logs)
- [ ] Firebase auth works (test login)
- [ ] Image upload works (test room upload)
- [ ] CORS configured for frontend domain
- [ ] Vastu API responding

## Local Development

```bash
# Backend
cd Backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd Frontend
npm install
npm run dev
```

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL format
- Check Supabase connection string includes password

### Firebase Storage Issues
- Verify FIREBASE_PROJECT_ID matches bucket name
- Check Firebase Storage rules allow writes

### CORS Errors
- Add frontend domain to CORS origins in `app/main.py`
