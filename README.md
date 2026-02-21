# 🚨 AI-Based Disaster Early Warning Platform

## 🎯 Project Overview
AI-powered multi-disaster prediction and early warning system for communities at risk.
Covers **5 disaster types**: Flood, Earthquake, Cyclone, Landslide, and Heatwave.

## 🏗️ Architecture
- **ML Layer** (`src/ml/`): Random Forest classifiers for 5 disaster types
- **Backend** (`src/backend/`): FastAPI REST API + WeatherAPI integration
- **Frontend** (`src/frontend/`): Streamlit dashboard with multi-language support

## 🛠️ Tech Stack
- Python 3.9+
- Scikit-learn, Pandas, NumPy
- FastAPI + Uvicorn
- Streamlit + Plotly
- OpenWeatherMap API

## 📦 Installation
```bash
# Clone repository
git clone <your-repo-url>
cd disaster-warning-platform

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration
1. Copy `.env.example` to `.env`
2. Add your OpenWeatherMap API key (free at https://openweathermap.org/api)
```
OPENWEATHER_API_KEY=your_key_here
```
> The system works in demo mode without an API key, but real weather data requires one.

## 🚀 Quick Start

### Run the Streamlit Dashboard (Recommended)
```bash
python -m streamlit run src/frontend/multi_disaster_app.py
```
Or use the launcher:
```bash
python src/frontend/run_multi_disaster.py
```

### Run the FastAPI Backend
```bash
python src/backend/main.py
# API docs at: http://localhost:8000/docs
```

### Run Tests
```bash
python -m pytest tests/
```

## 📁 Project Structure
```
disaster-warning-platform/
├── config/              # App configuration
├── data/
│   ├── disaster_models/ # Trained ML models (.pkl)
│   ├── processed/       # Preprocessed datasets
│   └── raw/             # Raw datasets
├── src/
│   ├── backend/         # FastAPI, weather API, disaster prediction
│   ├── frontend/        # Streamlit dashboard
│   └── ml/              # Model training, evaluation, data generation
├── tests/               # Unit & integration tests
├── requirements.txt
└── README.md
```

## ✨ Features
- 🌊 **Flood** — AI-powered predictions using rainfall, river levels, soil moisture
- 🔥 **Earthquake** — Seismic zone risk assessment
- 🌪️ **Cyclone** — Storm tracking with wind speed and pressure data
- ⛰️ **Landslide** — Slope stability analysis
- 🌡️ **Heatwave** — Heat index monitoring
- 🌐 **Multi-language** — English & Hindi support
- 📊 **Historical Data** — Past disaster trend analysis
- 📝 **Community Reports** — Crowdsourced disaster reporting
- 🏥 **Emergency Resources** — Nearby hospitals, shelters, fire stations

## 👥 Team
Your hackathon team name

## 📄 License
MIT
