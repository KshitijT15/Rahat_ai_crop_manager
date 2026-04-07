# 🌱 Rahat-AI Crop Manager

AI-powered crop management system designed for Indian farmers — combining **disease detection, price forecasting, crop recommendation, and fertilizer advisory** into one intelligent platform.

---

## 🚀 Features

* 🌿 **Tomato Disease Detection** (ResNet50 CNN)
* 📈 **Price Prediction** (ML model for market trends)
* 🌾 **Crop Recommendation** (based on soil + weather data)
* 🧪 **Fertilizer Advisory** (powered by Groq AI)
* 🌦️ **Weather Integration** (OpenWeather API)
* 📊 **Unified Dashboard UI**

---

## 📁 Project Structure

```
rahat-ai/
├── app.py
├── requirements.txt
├── Dockerfile
├── models/
│   ├── tomato_disease_model.h5
│   ├── tomato_price_model.pkl
│   ├── crop_recommendation_model.pkl
│   └── crop_scaler.pkl
└── templates/
    ├── base.html
    ├── index.html
    ├── disease.html
    ├── price.html
    ├── crop.html
    ├── fertilizer.html
    └── weather.html
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/KshitijT15/Rahat_ai_crop_manager.git
cd Rahat_ai_crop_manager
```

---

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Add Models

Place your trained models inside the `models/` folder:

* Disease model → `.keras` or `.h5`
* Price model → `.pkl`
* Crop model → `.joblib` / `.pkl`

---

### 5. Add API Keys

Create `.env` file:

```
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

---

### 6. Run Application

```
python app.py
```

Open in browser:

```
http://127.0.0.1:7860
```

---

## 🤖 Model Details

### 🌿 Disease Detection

* Model: ResNet50 (Transfer Learning)
* Input: 224x224 RGB image
* Output: 10 tomato disease classes

---

### 📈 Price Prediction

* Model: Gradient Boosting Regressor
* Input: Date features
* Output: Min / Avg / Max price

---

### 🌾 Crop Recommendation

* Input:

  ```
  N, P, K, temperature, humidity, ph, rainfall
  ```
* Output: Best crop suggestion

---

## 🌐 API Endpoints

| Endpoint                         | Method | Description            |
| -------------------------------- | ------ | ---------------------- |
| `/api/predict-disease`           | POST   | Predict tomato disease |
| `/api/predict-price`             | POST   | Predict price          |
| `/api/recommend-crop`            | POST   | Recommend crop         |
| `/api/fertilizer-recommendation` | POST   | AI fertilizer advice   |
| `/api/weather`                   | POST   | Weather data           |
| `/api/crop-advisory`             | POST   | AI advisory            |

---

## 🚀 Deployment (HuggingFace Spaces)

1. Create Space (Docker)
2. Push code
3. Add API keys in Secrets
4. Upload models (Git LFS or UI)

---

## 🔐 Security Notes

* `.env` is ignored (API keys protected)
* Models are excluded from Git (large files)

---

## 📌 Future Enhancements

* Multi-crop disease detection
* Real-time mandi price integration
* Mobile app version
* Voice-based farmer interface

---

## 👨‍💻 Author

**Kshitij T**
AI/ML & Data Analytics Enthusiast

---

## ⭐ If you like this project

Give it a star on GitHub ⭐
