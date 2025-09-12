# Brawny Originals

Personal business website (Brawny Originals) for Doug Lafon. All rights reserved.

A modern full-stack web application with Vite (TypeScript) frontend and FastAPI backend.

## Project Structure

```
brawnyoriginals/
├── frontend/          # Vite + TypeScript frontend
├── backend/           # FastAPI backend
├── .gitignore         # Git ignore file
└── README.md          # Project documentation
```

## Getting Started

### Prerequisites

- Node.js (v22+)
- Python (3.13+)
- npm or yarn

### Installation

1. Clone the repository
2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

### Development

1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open your browser to `http://localhost:5173`

## API Documentation

Once the backend server is running, you can access:
- API Docs: `http://localhost:8000/docs`
- Alternative API Docs: `http://localhost:8000/redoc`
