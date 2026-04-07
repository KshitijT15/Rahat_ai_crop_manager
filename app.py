from flask import Flask, render_template, request, jsonify
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
from dotenv import load_dotenv
import os

load_dotenv()

# Windows consoles often default to cp1252; emoji in print() can raise UnicodeEncodeError.
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import numpy as np
import tensorflow as tf
import pickle
import requests
from PIL import Image
import io
import base64
from groq import Groq
from datetime import datetime, timedelta
import pandas as pd
from sklearn.preprocessing import StandardScaler
import warnings
import joblib
import json
import re
warnings.filterwarnings('ignore')

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# ─── CONFIG ───────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# ─── DISEASE CLASSES ──────────────────────────────────────────────────────────
DISEASE_CLASSES = [
    "Tomato__Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites Two-spotted_spider_mite",
    "Tomato_Target_Spot",
    "Tomato_Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato_Tomato_mosaic_virus",
    "Tomato__healthy"
]

DISEASE_INFO = {
    "Tomato__Bacterial_spot": {
        "description": "Bacterial spot is caused by Xanthomonas species. It appears as small, water-soaked spots on leaves, stems, and fruits.",
        "severity": "High",
        "color": "#e74c3c"
    },
    "Tomato_Early_blight": {
        "description": "Early blight is caused by Alternaria solani fungus. Dark, concentric rings form target-like spots on lower leaves.",
        "severity": "Medium",
        "color": "#e67e22"
    },
    "Tomato_Late_blight": {
        "description": "Late blight caused by Phytophthora infestans. Water-soaked lesions appear on leaves and stems, rapidly turning brown.",
        "severity": "Critical",
        "color": "#c0392b"
    },
    "Tomato_Leaf_Mold": {
        "description": "Leaf mold caused by Passalora fulva fungus. Pale green/yellow spots appear on upper leaf surface.",
        "severity": "Medium",
        "color": "#f39c12"
    },
    "Tomato_Septoria_leaf_spot": {
        "description": "Septoria leaf spot caused by Septoria lycopersici. Small, circular spots with dark borders and lighter centers.",
        "severity": "Medium",
        "color": "#d35400"
    },
    "Tomato_Spider_mites Two-spotted_spider_mite": {
        "description": "Spider mites cause stippling, bronzing, and webbing on leaves. They thrive in hot, dry conditions.",
        "severity": "High",
        "color": "#e74c3c"
    },
    "Tomato_Target_Spot": {
        "description": "Target spot caused by Corynespora cassiicola. Circular lesions with concentric rings resembling a target.",
        "severity": "Medium",
        "color": "#e67e22"
    },
    "Tomato_Tomato_Yellow_Leaf_Curl_Virus": {
        "description": "TYLCV is spread by whiteflies. Leaves curl upward, turn yellow, and plants are stunted.",
        "severity": "Critical",
        "color": "#c0392b"
    },
    "Tomato_Tomato_mosaic_virus": {
        "description": "ToMV causes mosaic patterns of light and dark green on leaves. Spread by contact and infected tools.",
        "severity": "High",
        "color": "#e74c3c"
    },
    "Tomato__healthy": {
        "description": "The plant appears healthy with no visible signs of disease or pest damage.",
        "severity": "None",
        "color": "#27ae60"
    }
}

CROP_CLASSES = [
    'rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
    'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
    'banana', 'mango', 'grapes', 'watermelon', 'muskmelon',
    'apple', 'orange', 'papaya', 'coconut', 'cotton',
    'jute', 'coffee'
]

# ─── LOAD MODELS ──────────────────────────────────────────────────────────────
disease_model = None
price_model = None
crop_model = None
crop_scaler = None


def load_models():
    global disease_model, price_model, crop_model, crop_scaler

    disease_model = None
    price_model = None
    crop_model = None
    crop_scaler = None

    # ------------------- Disease Model (ResNet50 + weights.h5) -------------------
    weights_path = "models/model.weights.h5"
    if os.path.exists(weights_path):
        try:
            base = tf.keras.applications.ResNet50(
                weights=None,
                include_top=False,
                input_shape=(224, 224, 3)
            )
            x = tf.keras.layers.GlobalAveragePooling2D()(base.output)
            x = tf.keras.layers.Dense(512, activation="relu")(x)   # dense   → (2048, 512)
            x = tf.keras.layers.Dense(256, activation="relu")(x)   # dense_1 → (512, 256)
            x = tf.keras.layers.Dropout(0.5)(x)
            output = tf.keras.layers.Dense(10, activation="softmax")(x)  # dense_2 → (256, 10)

            disease_model = tf.keras.Model(inputs=base.input, outputs=output)
            disease_model.load_weights(weights_path)
            print("[OK] Disease model loaded from model.weights.h5")
        except Exception as e:
            print(f"[ERR] Error loading disease model: {e}")
    else:
        print(f"[WARN] Disease model not found at {weights_path}")

    # ------------------- Price Model -------------------
    if os.path.exists("models/tomato_price_model.pkl"):
        try:
            price_model = joblib.load("models/tomato_price_model.pkl")
            print("[OK] Price model loaded")
        except Exception as e:
            print(f"[ERR] Error loading price model: {e}")
    else:
        print("[WARN] Price model not found at models/tomato_price_model.pkl")

    # ------------------- Crop Model -------------------
    if os.path.exists("models/crop_recommendation_model.joblib"):
        try:
            crop_model = joblib.load("models/crop_recommendation_model.joblib")
            print("[OK] Crop model loaded")
        except Exception as e:
            print(f"[ERR] Error loading crop model: {e}")
    else:
        print("[WARN] Crop model not found at models/crop_recommendation_model.joblib")

    # ------------------- Crop Scaler -------------------
    if os.path.exists("models/crop_scaler.pkl"):
        try:
            crop_scaler = joblib.load("models/crop_scaler.pkl")
            print("[OK] Crop scaler loaded")
        except Exception as e:
            print(f"[ERR] Error loading crop scaler: {e}")
    else:
        print("[WARN] Crop scaler not found (optional)")


# ─── ROUTES ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return "", 204

@app.route("/disease")
def disease():
    return render_template("disease.html")

@app.route("/price")
def price():
    return render_template("price.html")

@app.route("/crop")
def crop():
    return render_template("crop.html")

@app.route("/fertilizer")
def fertilizer():
    return render_template("fertilizer.html")

@app.route("/weather")
def weather():
    return render_template("weather.html")


# ─── API ENDPOINTS ────────────────────────────────────────────────────────────

@app.route("/api/predict-disease", methods=["POST"])
def predict_disease():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        if disease_model is None:
            # Demo mode with random predictions
            probs = np.random.dirichlet(np.ones(10))
            predicted_idx = np.argmax(probs)
        else:
            preds = disease_model.predict(img_array)
            probs = preds[0]
            predicted_idx = np.argmax(probs)

        disease_name = DISEASE_CLASSES[predicted_idx]
        confidence = float(probs[predicted_idx]) * 100
        info = DISEASE_INFO[disease_name]

        top3 = sorted(
            [{"name": DISEASE_CLASSES[i], "confidence": float(probs[i]) * 100} for i in range(len(DISEASE_CLASSES))],
            key=lambda x: x["confidence"], reverse=True
        )[:3]

        return jsonify({
            "disease": disease_name,
            "confidence": round(confidence, 2),
            "description": info["description"],
            "severity": info["severity"],
            "color": info["color"],
            "top3": top3
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/predict-price", methods=["POST"])
def predict_price():
    try:
        data = request.json
        date_str = data.get("date")

        if not date_str:
            return jsonify({"error": "Date required"}), 400

        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        features = {
            "day": date_obj.day,
            "month": date_obj.month,
            "year": date_obj.year,
            "day_of_week": date_obj.weekday(),
            "day_of_year": date_obj.timetuple().tm_yday,
            "quarter": (date_obj.month - 1) // 3 + 1,
            "is_weekend": 1 if date_obj.weekday() >= 5 else 0
        }

        feature_array = np.array([[
            features["day"], features["month"], features["year"],
            features["day_of_week"], features["day_of_year"],
            features["quarter"], features["is_weekend"]
        ]])

        if price_model is None:
            base = 25 + (date_obj.month % 6) * 3
            noise = np.random.uniform(-3, 3)
            min_price = round(base + noise - 5, 2)
            avg_price = round(base + noise, 2)
            max_price = round(base + noise + 5, 2)
        else:
            predictions = price_model.predict(feature_array)
            if hasattr(predictions[0], '__len__') and len(predictions[0]) == 3:
                min_price, avg_price, max_price = predictions[0]
            else:
                avg_price = float(predictions[0])
                min_price = avg_price * 0.85
                max_price = avg_price * 1.15

        return jsonify({
            "date": date_str,
            "min_price": round(float(min_price), 2),
            "avg_price": round(float(avg_price), 2),
            "max_price": round(float(max_price), 2),
            "currency": "INR/Quintal"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/predict-price-range", methods=["POST"])
def predict_price_range():
    try:
        data = request.json
        start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d")
        days = int(data.get("days", 7))

        results = []
        for i in range(days):
            d = start_date + timedelta(days=i)
            feature_array = np.array([[
                d.day, d.month, d.year,
                d.weekday(), d.timetuple().tm_yday,
                (d.month - 1) // 3 + 1,
                1 if d.weekday() >= 5 else 0
            ]])

            if price_model is None:
                base = 25 + (d.month % 6) * 3
                noise = np.random.uniform(-3, 3)
                min_p = round(base + noise - 5, 2)
                avg_p = round(base + noise, 2)
                max_p = round(base + noise + 5, 2)
            else:
                preds = price_model.predict(feature_array)
                if hasattr(preds[0], '__len__') and len(preds[0]) == 3:
                    min_p, avg_p, max_p = preds[0]
                else:
                    avg_p = float(preds[0])
                    min_p = avg_p * 0.85
                    max_p = avg_p * 1.15

            results.append({
                "date": d.strftime("%Y-%m-%d"),
                "min_price": round(float(min_p), 2),
                "avg_price": round(float(avg_p), 2),
                "max_price": round(float(max_p), 2)
            })

        return jsonify({"predictions": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/recommend-crop", methods=["POST"])
def recommend_crop():
    try:
        data = request.json
        N = float(data.get("N", 0))
        P = float(data.get("P", 0))
        K = float(data.get("K", 0))
        temperature = float(data.get("temperature", 0))
        humidity = float(data.get("humidity", 0))
        ph = float(data.get("ph", 0))
        rainfall = float(data.get("rainfall", 0))

        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

        if crop_scaler is not None:
            features = crop_scaler.transform(features)

        if crop_model is None:
            crop = np.random.choice(CROP_CLASSES)
            probabilities = {c: round(np.random.uniform(0, 0.3), 3) for c in CROP_CLASSES}
            probabilities[crop] = round(np.random.uniform(0.6, 0.95), 3)
        else:
            prediction = crop_model.predict(features)[0]
            crop = prediction if isinstance(prediction, str) else CROP_CLASSES[int(prediction)]

            if hasattr(crop_model, "predict_proba"):
                proba = crop_model.predict_proba(features)[0]
                if hasattr(crop_model, "classes_"):
                    classes = crop_model.classes_
                else:
                    classes = CROP_CLASSES
                probabilities = {str(classes[i]): round(float(proba[i]), 3) for i in range(len(classes))}
            else:
                probabilities = {crop: 1.0}

        top5 = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:5]

        return jsonify({
            "recommended_crop": crop,
            "top5": [{"crop": k, "confidence": round(v * 100, 1)} for k, v in top5],
            "input_summary": {
                "N": N, "P": P, "K": K,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/fertilizer-recommendation", methods=["POST"])
def fertilizer_recommendation():
    try:
        if not GROQ_API_KEY:
            return jsonify({
                "error": "Groq API key not configured. Please add GROQ_API_KEY to your .env file."
            }), 503

        data = request.json
        crop = data.get("crop", "tomato")
        soil_n = data.get("soil_n", 0)
        soil_p = data.get("soil_p", 0)
        soil_k = data.get("soil_k", 0)
        ph = data.get("ph", 7)
        issue = data.get("issue", "general recommendation")
        area = data.get("area", "1 acre")

        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""You are an expert agricultural scientist specializing in soil nutrition and fertilizer management in India.

Provide a detailed fertilizer recommendation for:
- Crop: {crop}
- Current Soil NPK: N={soil_n} kg/ha, P={soil_p} kg/ha, K={soil_k} kg/ha
- Soil pH: {ph}
- Farm Area: {area}
- Issue/Goal: {issue}

Respond in a structured JSON format with these keys:
{{
  "summary": "2-3 sentence overview",
  "deficiencies": ["list of identified deficiencies"],
  "primary_fertilizers": [
    {{"name": "fertilizer name", "quantity": "amount with units", "timing": "when to apply", "method": "how to apply"}}
  ],
  "organic_options": [
    {{"name": "organic fertilizer", "quantity": "amount", "benefit": "key benefit"}}
  ],
  "application_schedule": [
    {{"stage": "crop stage", "week": "timing", "fertilizers": "what to apply"}}
  ],
  "precautions": ["list of important precautions"],
  "estimated_cost": "approximate cost in INR"
}}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500
        )

        raw = response.choices[0].message.content

        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {"summary": raw, "error": "Could not parse structured response"}

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _openweather_cod_ok(cod):
    """OpenWeather returns cod as int 200 or str '200' depending on endpoint."""
    return cod == 200 or str(cod) == "200"


@app.route("/api/weather", methods=["POST"])
def get_weather():
    try:
        if not OPENWEATHER_API_KEY:
            return jsonify({
                "error": "OpenWeather API key not configured. Please add OPENWEATHER_API_KEY to your .env file."
            }), 503

        data = request.json
        city = data.get("city", "")
        lat = data.get("lat")
        lon = data.get("lon")

        if lat is not None and lon is not None:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        elif str(city).strip():
            q = requests.utils.quote(str(city).strip())
            url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={OPENWEATHER_API_KEY}&units=metric"
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={q}&appid={OPENWEATHER_API_KEY}&units=metric"
        else:
            return jsonify({"error": "Enter a city name or use GPS coordinates."}), 400

        current = requests.get(url, timeout=15).json()
        forecast = requests.get(forecast_url, timeout=15).json()

        if not _openweather_cod_ok(current.get("cod")):
            msg = current.get("message", "Weather request failed")
            oc = str(current.get("cod", ""))
            status = 404 if oc in ("404", "400") else 502
            return jsonify({"error": msg}), status

        weather_data = {
            "city": current["name"],
            "country": current["sys"]["country"],
            "temperature": round(current["main"]["temp"], 1),
            "feels_like": round(current["main"]["feels_like"], 1),
            "humidity": current["main"]["humidity"],
            "pressure": current["main"]["pressure"],
            "wind_speed": round((current.get("wind") or {}).get("speed", 0) * 3.6, 1),
            "description": current["weather"][0]["description"].title(),
            "icon": current["weather"][0]["icon"],
            "visibility": current.get("visibility", 0) // 1000,
            "clouds": current["clouds"]["all"],
            "sunrise": datetime.fromtimestamp(current["sys"]["sunrise"]).strftime("%H:%M"),
            "sunset": datetime.fromtimestamp(current["sys"]["sunset"]).strftime("%H:%M"),
            "forecast": []
        }

        # 5-day forecast (every 24h)
        if _openweather_cod_ok(forecast.get("cod")):
            seen_dates = set()
            for item in forecast["list"]:
                date = item["dt_txt"].split(" ")[0]
                if date not in seen_dates and len(weather_data["forecast"]) < 5:
                    seen_dates.add(date)
                    weather_data["forecast"].append({
                        "date": date,
                        "temp_max": round(item["main"]["temp_max"], 1),
                        "temp_min": round(item["main"]["temp_min"], 1),
                        "description": item["weather"][0]["description"].title(),
                        "icon": item["weather"][0]["icon"],
                        "humidity": item["main"]["humidity"],
                        "rain": item.get("rain", {}).get("3h", 0)
                    })

        return jsonify(weather_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/crop-advisory", methods=["POST"])
def crop_advisory():
    """Get crop-specific advisory based on weather"""
    try:
        if not GROQ_API_KEY:
            return jsonify({
                "error": "Groq API key not configured. Please add GROQ_API_KEY to your .env file."
            }), 503

        data = request.json
        weather = data.get("weather", {})
        crop = data.get("crop", "tomato")

        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""As an agricultural expert, provide farming advisory for {crop} based on:
- Temperature: {weather.get('temperature')}°C
- Humidity: {weather.get('humidity')}%
- Wind Speed: {weather.get('wind_speed')} km/h
- Weather: {weather.get('description')}
- Clouds: {weather.get('clouds')}%

Provide concise, actionable advice in JSON:
{{
  "overall_suitability": "Excellent/Good/Fair/Poor",
  "immediate_actions": ["action1", "action2"],
  "irrigation_advice": "specific advice",
  "pest_disease_risk": "Low/Medium/High with brief explanation",
  "harvesting_advice": "advice if applicable",
  "storage_advice": "brief advice"
}}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=600
        )

        raw = response.choices[0].message.content
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {"overall_suitability": "Good", "immediate_actions": [raw]}

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    load_models()
    app.run(debug=True, host="0.0.0.0", port=7860)