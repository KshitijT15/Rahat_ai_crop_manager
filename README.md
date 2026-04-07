# 🌱 Rahat-AI Crop Manager

AI-powered crop management system for Indian farmers — disease detection, price forecasting, crop recommendation & fertilizer advisory.

---

## 📁 Project Structure

```
rahat-ai/
├── app.py                    ← Flask backend (all API routes)
├── requirements.txt
├── Dockerfile                ← HuggingFace Spaces deployment
├── models/                   ← Place your trained model files here
│   ├── tomato_disease_model.h5
│   ├── tomato_price_model.pkl
│   ├── crop_recommendation_model.pkl
│   └── crop_scaler.pkl       (optional, if you saved a scaler)
└── templates/
    ├── base.html             ← Sidebar layout
    ├── index.html            ← Dashboard
    ├── disease.html          ← Disease detection
    ├── price.html            ← Price forecasting
    ├── crop.html             ← Crop recommender
    ├── fertilizer.html       ← Fertilizer AI
    └── weather.html          ← Weather & advisory
```

---

## ⚙️ Step-by-Step Setup in Cursor

### Step 1 — Clone/Create Project
Open Cursor, create a new folder `rahat-ai` and paste all files.

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Place Your Models
Copy your trained models into the `models/` folder:
- `tomato_disease_model.h5` — Your ResNet50 disease classifier
- `tomato_price_model.pkl` — Your price prediction model
- `crop_recommendation_model.pkl` — Your crop recommendation model
- `crop_scaler.pkl` — (optional) StandardScaler if you used one

### Step 4 — Set API Keys
Create a `.env` file or set environment variables:
```bash
export GROQ_API_KEY="gsk_your_groq_key_here"
export OPENWEATHER_API_KEY="your_openweather_key_here"
```

Or edit directly in `app.py` (lines 13-14) for testing:
```python
GROQ_API_KEY = "gsk_your_key"
OPENWEATHER_API_KEY = "your_key"
```

### Step 5 — Run Locally
```bash
python app.py
```
Open: http://localhost:7860

---

## 🤖 Model Integration Notes

### Disease Model (TensorFlow / Keras)
Your model should:
- Accept input shape: `(None, 224, 224, 3)` — normalized to [0,1]
- Output shape: `(None, 10)` — softmax over 10 disease classes
- Classes order must match `DISEASE_CLASSES` list in `app.py`

### Price Model (scikit-learn / pickle)
Your model should accept features:
```
[day, month, year, day_of_week, day_of_year, quarter, is_weekend]
```
Output: either `[min_price, avg_price, max_price]` or just `avg_price`

### Crop Recommendation Model (scikit-learn / pickle)
Your model should accept:
```
[N, P, K, temperature, humidity, ph, rainfall]
```
Output: crop name (string) or class index

---

## 🚀 Deploy to Hugging Face Spaces

### Step 1 — Create a Space
1. Go to https://huggingface.co/spaces
2. Create new Space → **Docker** SDK
3. Name it `rahat-ai-crop-manager`

### Step 2 — Push Files
```bash
git init
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/rahat-ai-crop-manager
git add .
git commit -m "Initial deployment"
git push origin main
```

### Step 3 — Add Secrets
In HuggingFace Space → Settings → Repository Secrets:
- `GROQ_API_KEY` = your Groq API key
- `OPENWEATHER_API_KEY` = your OpenWeather API key

### Step 4 — Upload Models
Since model files are large, upload them via:
```bash
git lfs install
git lfs track "*.h5" "*.pkl"
git add .gitattributes
git commit -m "Add model files"
git push
```
Or use the HuggingFace web interface to upload files directly.

---

## 🔑 API Keys

### Groq API (Free)
1. Sign up at https://console.groq.com
2. Create API Key → copy it

### OpenWeather API (Free tier)
1. Sign up at https://openweathermap.org/api
2. Create API key (takes ~10 min to activate)
3. Free tier: 60 calls/minute

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/predict-disease` | POST | Disease detection from image |
| `/api/predict-price` | POST | Single date price prediction |
| `/api/predict-price-range` | POST | Multi-day price forecast |
| `/api/recommend-crop` | POST | Crop recommendation from NPK |
| `/api/fertilizer-recommendation` | POST | Groq AI fertilizer advice |
| `/api/weather` | POST | OpenWeather current + forecast |
| `/api/crop-advisory` | POST | AI advisory based on weather |

---

## 📝 Notes

- **Demo mode**: If model files are missing, the app runs in demo mode with simulated predictions
- **Mobile responsive**: Sidebar collapses on mobile screens
- **No model training**: This repo is inference-only; train your models separately and place `.h5`/`.pkl` files in `models/`