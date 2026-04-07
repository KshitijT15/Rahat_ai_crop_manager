# 🌱 Rahat-AI — Crop Manager v1.0

> An AI-powered precision agriculture platform for tomato farmers, combining real-time weather data, disease detection, price forecasting, and smart fertilizer recommendations.

![Dashboard Preview](https://img.shields.io/badge/Status-All%20Systems%20Operational-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Features

### 🍅 Tomato Tools
| Feature | Description |
|---|---|
| **Disease Detection** | Upload a tomato leaf image and get AI-powered diagnosis using a ResNet50 model. Detects 10 disease classes including Late Blight, Bacterial Spot, Mosaic Virus, and more. |
| **Price Forecast** | ML-based tomato market price prediction (INR/Quintal). Supports single-date and 7-day range forecasts with trend charts. |

### 🌾 Farm Intelligence
| Feature | Description |
|---|---|
| **Crop Recommender** | Input soil NPK, pH, temperature, humidity, and rainfall to get the best-fit crop from 22 varieties. |
| **Fertilizer AI** | AI-driven fertilizer recommendations based on crop type, farm area, soil NPK, and pH. Includes application schedule and cost estimate. |
| **Weather & Advisory** | Real-time weather via OpenWeather API + AI crop advisory for any city. Includes 5-day forecast and irrigation/pest risk insights. |

---

## 📸 Screenshots

| Module | Preview |
|---|---|
| Weather & Advisory | Live weather data, 5-day forecast, and AI crop advisory for your city |
| Disease Detection | Upload leaf → ResNet50 diagnosis → Treatment recommendation |
| Price Forecast | ML price prediction with min/avg/max and trend chart |
| Crop Recommender | Soil & climate parameters → Best crop match from 22 varieties |
| Fertilizer AI | NPK deficiency detection → Fertilizer plan with application schedule |

---

## 🛠️ Tech Stack

- **Frontend:** React.js / Next.js (dark-themed dashboard UI)
- **AI/ML Models:**
  - ResNet50 — Tomato disease classification (10 classes)
  - ML regression model — Tomato price forecasting
  - Claude API (Anthropic) — Natural language advisory & recommendations
- **APIs:**
  - OpenWeather API — Real-time weather & 5-day forecast
- **Styling:** Tailwind CSS / custom dark theme

---

## ⚙️ Installation & Setup

### Prerequisites

- Node.js ≥ 18
- Python ≥ 3.9 (if running ML model locally)
- OpenWeather API key
- Anthropic API key

### 1. Clone the repository

```bash
git clone https://github.com/KshitijT15/Rahat_ai_crop_manager.git
cd Rahat_ai_crop_manager
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configure environment variables

Create a `.env.local` file in the root directory:

```env
OPENWEATHER_API_KEY=your_openweather_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

> Get your OpenWeather API key at [openweathermap.org](https://openweathermap.org/api)  
> Get your Anthropic API key at [console.anthropic.com](https://console.anthropic.com)

### 4. Run the development server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧭 Navigation

```
Rahat-AI
├── Overview
│   └── Dashboard
├── Tomato Tools
│   ├── Disease Detection
│   └── Price Forecast
└── Farm Intelligence
    ├── Crop Recommender
    ├── Fertilizer AI
    └── Weather & Advisory
```

---

## 🔬 Module Details

### 🍃 Disease Detection
- Upload a tomato leaf image
- ResNet50 model classifies among 10 disease categories:
  - Bacterial Spot, Early Blight, Late Blight, Leaf Mold
  - Septoria Leaf Spot, Spider Mites, Target Spot
  - Yellow Leaf Curl Virus, Mosaic Virus, Healthy
- Displays confidence score and top-3 predictions
- AI treatment recommendation with precautions

### 📊 Price Forecast
- Predicts tomato prices in **INR/Quintal**
- Single-date prediction: select any date
- 7-day forecast: generates min, avg, max price trend
- Visual trend chart for easy interpretation

### 🌿 Crop Recommender
- Input parameters: N, P, K (kg/ha), temperature (°C), humidity (%), soil pH, rainfall (mm)
- Recommends best crop from 22 varieties
- Shows top-5 crop matches with confidence scores
- Quick presets for common climate profiles

### 🧪 Fertilizer AI
- Input: crop type, farm area, current soil NPK, pH, issue/goal
- Identifies soil deficiencies automatically
- Recommends fertilizers (Urea, DAP, MOP, FYM, Vermicompost) with dosage
- Provides a stage-wise application schedule (Sowing → Fruiting → Fruit Development)
- Estimated cost range in INR

### 🌤️ Weather & Advisory
- Search by city name or use GPS location
- Real-time data: temperature, humidity, wind, cloud cover, visibility, pressure
- Sunrise/sunset times
- 5-day weather forecast
- AI crop advisory: immediate actions, irrigation tips, pest/disease risk, harvest advice

---

## 🗂️ Project Structure

```
Rahat_ai_crop_manager/
├── components/          # Reusable UI components
├── pages/               # Next.js page routes
│   ├── dashboard/
│   ├── disease-detection/
│   ├── price-forecast/
│   ├── crop-recommender/
│   ├── fertilizer-ai/
│   └── weather-advisory/
├── public/              # Static assets
├── styles/              # Global CSS / Tailwind config
├── utils/               # Helper functions & API calls
├── models/              # ML model inference scripts
├── .env.local           # Environment variables (not committed)
├── package.json
└── README.md
```

---

## 🌐 Quick Cities Supported

Mumbai · Delhi · Bengaluru · Pune · Hyderabad · Chennai · Kolkata · Ahmedabad · Nagpur · Nashik

(Any city worldwide is supported via search)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Kshitij T.** — [@KshitijT15](https://github.com/KshitijT15)

---

## 🙏 Acknowledgements

- [OpenWeather API](https://openweathermap.org/) for real-time weather data
- [Anthropic Claude](https://www.anthropic.com/) for AI-powered advisory
- [ResNet50](https://arxiv.org/abs/1512.03385) architecture for disease classification
- All contributors and the open-source community

---

> *Rahat-AI — Bringing precision agriculture to every farmer's fingertips.* 🌾
