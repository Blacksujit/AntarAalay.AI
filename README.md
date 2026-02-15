# AntarAalay.ai

AI-Powered Interior Design Platform with Vastu Integration

Transform your space with AI-generated interior designs that align with ancient Vastu principles. Perfect harmony between modern aesthetics and 5000-year-old Vastu Shastra science.

## Features

- **AI Design Generation**: Upload room photos and get 3 AI-generated design variations
- **Vastu Analysis**: Every design is analyzed for Vastu compliance with actionable suggestions
- **Budget Planning**: Accurate cost estimates and furniture breakdowns
- **Style Options**: Modern, Traditional Indian, Minimalist, Luxury, Bohemian, Scandinavian, Industrial, Contemporary
- **Direction Analysis**: Vastu scores based on room direction (North, South, East, West, etc.)

## Tech Stack

### Backend
- Python 3.11 + FastAPI
- SQLAlchemy + Supabase PostgreSQL
- Firebase cloud storage
- Firebase Authentication
- Stability AI (Stable Diffusion)

### Frontend
- Next.js + TypeScript + Vite
- Tailwind CSS
- Zustand (state management)
- React Query (data fetching)
- Firebase Auth
- Axios

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL (or Supabase account)
- Firebase storage bucket
- Firebase project
- Stability AI API key

### Backend Setup

```bash
cd Backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and fill environment variables
cp .env.example .env

# Run development server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd Frontend
npm install

# Copy and fill environment variables
cp .env.example .env.local

# Run development server
npm run dev
```

## API Endpoints

### Room Management
- `POST /api/room/upload` - Upload room image
- `GET /api/room/{room_id}` - Get room details
- `GET /api/room/user/rooms` - Get user's rooms

### Design Generation
- `POST /api/design/generate` - Generate AI designs
- `GET /api/design/{design_id}` - Get design details
- `GET /api/design/room/{room_id}` - Get room designs

### Vastu Analysis
- `POST /api/vastu/analyze` - Analyze Vastu compliance
- `GET /api/vastu/direction/{direction}` - Get direction info
- `GET /api/vastu/score/{direction}/{room_type}` - Get Vastu score
- `GET /api/vastu/remedies/{direction}/{room_type}` - Get remedies

## Project Structure

```
AntarAalay.ai/
├── Backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── room.py
│   │   │   └── design.py
│   │   ├── schemas/
│   │   │   ├── room.py
│   │   │   ├── design.py
│   │   │   └── vastu.py
│   │   ├── routes/
│   │   │   ├── room.py
│   │   │   ├── design.py
│   │   │   └── vastu.py
│   │   └── services/
│   │       ├── ai_engine.py
│   │       ├── vastu_engine.py
│   │       ├── storage.py
│   │       └── budget_engine.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── Frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Upload.tsx
│   │   │   ├── Designs.tsx
│   │   │   └── Vastu.tsx
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── upload.ts
│   │   │   ├── design.ts
│   │   │   └── vastu.ts
│   │   ├── store/
│   │   │   └── authStore.ts
│   │   ├── lib/
│   │   │   └── firebase.ts
│   │   └── App.tsx
│   ├── package.json
│   └── .env.example
└── DEPLOYMENT.md
```

<!-- ## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

**Backend**: Docker → Render/EC2
**Frontend**: Vercel
**Database**: Supabase
**Storage**: AWS S3 -->

## License

MIT License - Built for production use.

## Support

For issues or questions, please open a GitHub issue.

---

Built with ❤️ for the Indian home design market.
