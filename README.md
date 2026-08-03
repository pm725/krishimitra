# 🌾 KrishiMitra — AI-Powered Agricultural Advisory System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.14-blue)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139-green)](#)
[![React](https://img.shields.io/badge/React-19-blue)](#)
[![Tailwind](https://img.shields.io/badge/Tailwind-3.4-cyan)](#)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](#)

KrishiMitra provides localized, AI-driven weather forecasts and crop advisory to smallholder farmers through accessible delivery channels (SMS, WhatsApp, voice). It is designed for low-bandwidth contexts and multilingual support with a focus on village-level precision.

---

## 🌍 Problem

Nepal is among the top climate-vulnerable countries and farmers face high uncertainty from extreme rainfall and temperature variability. Smallholder farmers need timely, localized, actionable advice delivered over channels they already use.

## 🎯 Solution

KrishiMitra aggregates historical weather, observational, and crop data, runs forecasting and advisory models, and delivers personalized guidance to farmers (via SMS/WhatsApp/voice). It also provides a web dashboard for monitoring farmers, crops, and delivery analytics.

---

## ✨ Key features

- Village-level weather forecasts (3-day, 7-day, seasonal outlooks)
- AI-based advisory tailored to crop and local conditions
- Multi-channel delivery: SMS, WhatsApp, and voice calls
- Multilingual UI: Nepali + English (extensible)
- Analytics dashboard for farmer & crop trends
- Modular architecture: frontend, backend, ML models, and messaging integrations

---

## 🧰 Tech stack

- Frontend: React 19 + Vite, Tailwind CSS, Chart.js, i18next
- Backend: Python 3.14, FastAPI, SQLAlchemy
- Database: PostgreSQL
- ML: LSTM / XGBoost for forecasting and yield prediction; Hugging Face Transformers for advisory NLP
- Integrations: OpenWeatherMap, wttr.in (fallback), Twilio (SMS/Voice), WhatsApp APIs

---

## 📁 Project structure

krishimitra/
├── backend/                # FastAPI backend (app, services, models)
├── frontend/               # React + Vite frontend
├── ml_models/              # Training & inference pipelines for weather and yield models
├── database/               # DB migrations / schema
├── docker-compose.yml      # Orchestration for local dev
├── .env                    # Example env file (do not commit credentials)
└── README.md

---

## 🚀 Quick start (Docker)

The easiest way to run KrishiMitra locally is with Docker Compose.

1. Copy the example env:
   cp .env.example .env

2. Start services:
   docker compose up --build

3. Backend API: http://localhost:8000
   Frontend: http://localhost:3000

(Adjust ports in .env or docker-compose.yml as needed.)

---

## 🛠 Development setup (manual)

Prerequisites:
- Python 3.14
- Node.js 18+ (or as required by your frontend)
- PostgreSQL 16

Backend
1. cd backend
2. python -m venv .venv && source .venv/bin/activate
3. pip install -r requirements.txt
4. copy .env and set DB and API keys
5. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Frontend
1. cd frontend
2. npm install
3. npm run dev

---

## ⚙️ Environment variables (example)

Create .env (or .env.local) with these values:

DATABASE_URL=postgresql://user:pass@db:5432/krishimitra
SECRET_KEY=change_me
OPENWEATHER_API_KEY=your_key
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_FROM_NUMBER=+1234567890

Do NOT commit real secrets.

---

## 🔌 Messaging integrations

- Twilio (SMS & voice) — configured in backend/services/sms_service.py
- WhatsApp — use provider/A.P.I. in integrations folder (or Twilio WhatsApp)
- Fallback to SMS where WhatsApp isn't available

---

## 📡 API — selected endpoints

- GET /               — API info / root
- GET /health         — Health check
- POST /api/weather/free       — Get weather (free provider, no key)
- POST /api/weather/current    — Get current weather (OpenWeather)
- POST /api/advisory/generate  — Generate farming advice (input: farmer, location, crop, weather forecast)
- POST /api/farmers/register   — Register a farmer
- GET  /api/farmers/list       — List registered farmers

Request/response schemas live in backend/app/schemas.py (or equivalent). Use the OpenAPI docs at /docs when the server is running.

---

## 🔬 Models & Data

- ml_models/weather_prediction_xgboost.py — example model pipeline
- Historical weather: OpenWeather + local observational datasets (where available)
- NLP advisor uses fine-tuned transformer models to generate crop-specific advice in target languages.

If you intend to train models, use the ml_models/ folder and ensure training data is stored outside the repo (or in a secure data bucket).

---

## 🧪 Tests & linting

Run backend tests (if provided):

pytest -q

Linting (example):

black backend && flake8 backend
npm run lint (frontend)

---

## 🤝 Contributing

Contributions are welcome! Suggested workflow:
1. Open an issue to discuss a feature or bug.
2. Fork the repository and create a branch: feature/your-feature
3. Add tests where appropriate and update docs.
4. Submit a pull request referencing the issue.

Please follow the code style used in the repository and include unit/integration tests for new features.

---

## 🗺 Roadmap

- v0.2: Improved forecasting models and plugin system
- v0.3: Additional delivery channels & offline-first features
- v1.0: Stable API and production-ready scaling & monitoring

---

## ⚖️ License

MIT — see LICENSE file.

---

## 📬 Contact & maintainers

Maintainer: pm725 (GitHub)
Project email: mahatpriyanshu7@gmail.com

---

## 📝 Notes & next steps

- Add a short demo GIF or screenshots in docs/ or a /public demo.
- Provide a .env.example file with placeholder values.
- Add automated CI for tests and linting (GitHub Actions).
