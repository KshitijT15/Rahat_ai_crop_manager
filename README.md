# 🌱 Rahat-AI — Crop Manager v1.0

> An AI-powered precision agriculture platform for tomato farmers — combining real-time weather, disease detection, price forecasting, crop recommendation, and smart fertilizer planning in one dark-themed dashboard.

![Status](https://img.shields.io/badge/Status-All%20Systems%20Operational-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0-blue)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19-orange?logo=tensorflow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Screenshots

### 🏠 Weather & Advisory
![Weather & Advisory](screenshots/weather_advisory.png)
> Real-time weather for any city with 5-day forecast and Grok-powered AI crop advisory

---

### 🍃 Disease Detection
![Disease Detection](screenshots/disease_detection.png)
> Upload a tomato leaf → ResNet50 diagnosis → AI treatment recommendation

---

### 📊 Tomato Price Forecast
![Price Forecast](screenshots/price_forecast.png)
> ML-powered price prediction with min / avg / max and a 7-day trend chart

---

### 🌿 Crop Recommender
![Crop Recommender](screenshots/crop_recommender.png)
> Enter soil & climate parameters → best crop from 22 varieties with confidence scores

---

### 🧪 Fertilizer AI
![Fertilizer AI](screenshots/fertilizer_ai.png)
> Soil deficiency detection → fertilizer plan with stage-wise schedule and cost estimate

---

## 🚀 Features

### 🍅 Tomato Tools

| Feature | Description |
|---|---|
| **Disease Detection** | Upload a tomato leaf image for ResNet50-based diagnosis across 10 disease classes. Returns top-3 predictions, confidence score, and Grok AI treatment advice. |
| **Price Forecast** | Scikit-learn regression model predicts tomato market prices (INR/Quintal) for a single date or a 7-day range with a min/avg/max trend chart. |

### 🌾 Farm Intelligence

| Feature | Description |
|---|---|
| **Crop Recommender** | Input soil NPK, pH, temperature, humidity, and rainfall — get the best crop from 22 varieties using a trained classification model with probability scores. |
| **Fertilizer AI** | Grok LLM (`llama-3.3-70b-versatile`) generates a detailed fertilizer plan with deficiency analysis, dosage, application schedule, and INR cost estimate. |
| **Weather & Advisory** | Live weather via OpenWeather API + Grok-powered crop advisory with irrigation, pest risk, and harvest guidance. |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10, Flask 3.0 |
| **Frontend** | HTML5, CSS3, JavaScript (Jinja2 templates) |
| **Disease Model** | TensorFlow 2.19 — ResNet50 + custom dense head trained on 10 tomato disease classes |
| **Price Model** | Scikit-learn — regression model (joblib serialized) |
| **Crop Model** | Scikit-learn — multi-class classifier (joblib serialized) |
| **AI Advisory** | [Groq API](https://groq.com/) — `llama-3.3-70b-versatile` for fertilizer & crop advisory |
| **Weather** | [OpenWeather API](https://openweathermap.org/api) — current weather + 5-day forecast |
| **Image Processing** | Pillow, OpenCV |
| **Containerization** | Docker (HuggingFace Spaces compatible, port 7860) |

---

## 📁 Project Structure

```
Rahat_ai_crop_manager/
├── app.py                                 # Flask app — all routes & API endpoints
├── inspect_weights.py                     # Utility to inspect model weight shapes
├── requirements.txt                       # Python dependencies
├── Dockerfile                             # Docker config (HuggingFace Spaces ready)
├── .gitignore
├── templates/                             # Jinja2 HTML templates
│   ├── index.html                         # Dashboard
│   ├── disease.html                       # Disease Detection page
│   ├── price.html                         # Price Forecast page
│   ├── crop.html                          # Crop Recommender page
│   ├── fertilizer.html                    # Fertilizer AI page
│   └── weather.html                       # Weather & Advisory page
├── models/                                # ML model files (not committed — see below)
│   ├── model.weights.h5                   # ResNet50 disease model weights
│   ├── tomato_price_model.pkl             # Price prediction model
│   ├── crop_recommendation_model.joblib   # Crop classifier
│   └── crop_scaler.pkl                    # Feature scaler for crop model
└── screenshots/                           # UI screenshots for README
```

> **Note:** The `models/` directory is not committed to the repo due to file size. Download the model files separately and place them in the `models/` folder before running. The app runs in **demo mode** (random predictions) if model files are missing.

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10+
- Groq API key — [console.groq.com](https://console.groq.com)
- OpenWeather API key — [openweathermap.org/api](https://openweathermap.org/api)

### 1. Clone the repository

```bash
git clone https://github.com/KshitijT15/Rahat_ai_crop_manager.git
cd Rahat_ai_crop_manager
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
```
flask==3.0.0
tensorflow==2.19.0
numpy==1.26.4
scikit-learn==1.4.2
pandas==2.2.2
pillow
opencv-python
joblib
requests
groq
```

### 3. Configure environment variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

### 4. Add model files

Place your trained model files in the `models/` directory:

```
models/
├── model.weights.h5
├── tomato_price_model.pkl
├── crop_recommendation_model.joblib
└── crop_scaler.pkl
```

### 5. Run the app

```bash
python app.py
```

Open [http://localhost:7860](http://localhost:7860) in your browser.

---

## 🐳 Docker / HuggingFace Spaces

The app is pre-configured for Docker and HuggingFace Spaces on **port 7860**.

```bash
# Build
docker build -t rahat-ai .

# Run
docker run -p 7860:7860 \
  -e GROQ_API_KEY=your_key \
  -e OPENWEATHER_API_KEY=your_key \
  rahat-ai
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/predict-disease` | Upload leaf image → disease diagnosis |
| `POST` | `/api/predict-price` | Single date → min / avg / max price |
| `POST` | `/api/predict-price-range` | Date range → multi-day price forecast |
| `POST` | `/api/recommend-crop` | Soil & climate params → crop recommendation |
| `POST` | `/api/fertilizer-recommendation` | NPK + crop → Grok AI fertilizer plan |
| `POST` | `/api/weather` | City or lat/lon → weather data + forecast |
| `POST` | `/api/crop-advisory` | Weather + crop → Grok AI advisory |

---

## 🔬 Module Details

### 🍃 Disease Detection
- Accepts leaf image uploads up to 16 MB
- Architecture: ResNet50 → GlobalAveragePooling2D → Dense(512, ReLU) → Dense(256, ReLU) → Dropout(0.5) → Dense(10, Softmax)
- **10 detectable classes:** Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy
- Returns top-3 predictions with confidence %, severity rating, and AI treatment recommendation

### 📊 Price Forecast
- **Input features:** day, month, year, day-of-week, day-of-year, quarter, is_weekend
- **Output:** min / avg / max price in **INR/Quintal**
- Supports single-date prediction or a multi-day range with trend chart

### 🌿 Crop Recommender
- **Input:** N, P, K (kg/ha), temperature (°C), humidity (%), soil pH, rainfall (mm)
- **22 crop classes:** rice, maize, chickpea, kidney beans, pigeon peas, moth beans, mung bean, black gram, lentil, pomegranate, banana, mango, grapes, watermelon, muskmelon, apple, orange, papaya, coconut, cotton, jute, coffee
- Returns top-5 crop matches with confidence %

### 🧪 Fertilizer AI
- Powered by **Groq API** (`llama-3.3-70b-versatile`)
- **Input:** crop type, farm area, current soil NPK, pH, issue/goal
- **Output (structured JSON):** summary, identified deficiencies, primary fertilizers with dosage & timing, organic options, stage-wise application schedule (Sowing → Fruiting → Fruit Development), precautions, estimated INR cost

### 🌤️ Weather & Advisory
- Supports city name search **or** GPS coordinates (lat/lon)
- **Live metrics:** temperature, feels-like, humidity, pressure, wind speed, cloud cover, visibility, sunrise/sunset
- **5-day forecast:** daily high/low, description, rain data
- **Grok AI advisory:** suitability rating (Excellent/Good/Fair/Poor), immediate actions, irrigation advice, pest/disease risk, harvest & storage tips

---

## 🌐 Quick Cities Supported

Mumbai · Delhi · Bengaluru · Pune · Hyderabad · Chennai · Kolkata · Ahmedabad · Nagpur · Nashik

*(Any city worldwide is supported via search or GPS)*

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Kshitij T.** — [@KshitijT15](https://github.com/KshitijT15)

---

## 🙏 Acknowledgements

- [Groq](https://groq.com/) — ultra-fast LLM inference powering all AI advisory features
- [OpenWeather API](https://openweathermap.org/) — real-time weather data
- [ResNet50](https://arxiv.org/abs/1512.03385) — backbone for disease classification
- [TensorFlow](https://tensorflow.org/) & [Scikit-learn](https://scikit-learn.org/) — ML frameworks
- [HuggingFace Spaces](https://huggingface.co/spaces) — deployment platform

---

> *Rahat-AI — Bringing precision agriculture to every farmer's fingertips.* 🌾
