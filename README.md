# 🌞 SDS-YOLO — Solar Panel Soiling Detection System

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&size=22&duration=3000&pause=1000&color=F5A623&center=true&vCenter=true&width=700&lines=Detect.+Analyze.+Maintain.;AI-Powered+Solar+Panel+Monitoring;SDS-YOLO+%7C+YOLOv5+%7C+Flask+%7C+Python" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white)
![YOLOv5](https://img.shields.io/badge/YOLOv5-Detection-00C853?style=for-the-badge&logo=github&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-ML%20Framework-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Logic-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

<br/>

> **A machine learning web application for real-time detection of dust and bird-dropping contamination on solar panels using a custom-trained SDS-YOLO model.**

</div>

---

## 📌 Overview

**SDS-YOLO Solar Panel Soiling Detection System** is an end-to-end machine learning solution that helps solar farm operators and maintenance engineers automatically identify panel contamination through image analysis.

Powered by a custom **SDS-YOLO** model (built on YOLOv5), the system processes uploaded solar panel images and returns:
- Annotated detection output with bounding boxes
- Soiling category and confidence scores
- Detection count and structured logs

> ✅ Ideal for **solar farm monitoring**, **predictive maintenance**, and **smart energy systems**.

---

## 🎯 Objectives

- 📷 Upload solar panel images via a clean web interface
- 🤖 Run automated SDS-YOLO inference on uploaded images
- 🔲 Highlight detected soiling areas with bounding boxes
- 📊 Report detection count, model name, and confidence values
- 🔁 Support iterative inspection for maintenance teams

---

## 🧠 ML Model

| Property     | Details                  |
|--------------|--------------------------|
| **Model**    | SDS-YOLO (YOLOv5-based)  |
| **File**     | `sds_yolo_best.pt`       |
| **Classes**  | Dust, Bird-Droppings     |
| **Framework**| PyTorch + OpenCV         |

### Detection Classes

| Class ID | Label            | Description                          |
|----------|------------------|--------------------------------------|
| `0`      | 🟡 Dust          | Granular particulate on panel surface |
| `1`      | 🟤 Bird-Droppings| Organic contamination from birds     |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        USER                             │
│                  Uploads Solar Image                    │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│               FRONTEND  (HTML + CSS + JS)               │
│         index.html  ·  style.css  ·  script.js          │
└────────────────────────┬────────────────────────────────┘
                         │  POST /detect  (multipart/form-data)
                         ▼
┌─────────────────────────────────────────────────────────┐
│               FLASK BACKEND  (app.py)                   │
│   Receives image → saves → triggers YOLOv5 detect.py   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│            SDS-YOLO MODEL  (sds_yolo_best.pt)           │
│   Runs inference → generates annotated output image    │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│               DETECTION OUTPUT                          │
│  Annotated image · count · confidence · detection log  │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technologies Used

### 🖥️ Frontend
| Technology | Purpose |
|------------|---------|
| HTML5 | Page structure and layout |
| CSS3 | Styling and responsive design |
| JavaScript | API calls and dynamic rendering |

### ⚙️ Backend
| Technology | Purpose |
|------------|---------|
| Python 3.10+ | Core backend language |
| Flask | Web server and REST API |
| Flask-CORS | Cross-origin request handling |

### 🤖 Machine Learning
| Technology | Purpose |
|------------|---------|
| YOLOv5 | Object detection base framework |
| PyTorch | Deep learning inference engine |
| OpenCV | Image processing and annotation |
| SDS-YOLO `.pt` | Custom-trained soiling detection model |

### 🔧 Dev Tools
| Tool | Purpose |
|------|---------|
| Google Colab | Model training and testing |
| Visual Studio Code | Local development |
| GitHub | Version control |
| Google Drive | Model storage and dataset management |

---

## 📂 Project Structure

```
solar-soiling-web-app/
│
├── 📁 backend/
│   ├── 🐍 app.py                  # Flask app entry point
│   ├── 📄 requirements.txt        # Python dependencies
│   │
│   ├── 📁 model/
│   │   └── 🤖 sds_yolo_best.pt    # Trained SDS-YOLO model
│   │
│   ├── 📁 uploads/                # Incoming user images
│   ├── 📁 results/                # Detection output images
│   │
│   └── 📁 yolov5/                 # YOLOv5 submodule
│       ├── 🐍 detect.py
│       ├── 📁 models/
│       └── 📁 utils/
│
├── 📁 frontend/
│   ├── 🌐 index.html              # Main UI page
│   ├── 🎨 style.css               # Styling
│   └── ⚡ script.js               # Frontend logic
│
├── 📁 .vscode/
│   └── ⚙️ settings.json
│
└── 📄 README.md
```

---

## ⚙️ Installation & Setup

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/solar-soiling-web-app.git
cd solar-soiling-web-app
```

---

### Step 2 — Navigate to Backend

```bash
cd backend
```

---

### Step 3 — Create & Activate Virtual Environment

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

---

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 5 — Verify Model File

Ensure the trained model exists at:

```
backend/model/sds_yolo_best.pt
```

> ⚠️ If missing, manually place `sds_yolo_best.pt` inside the `model/` folder before running.

---

### Step 6 — Start the Flask Server

```bash
python app.py
```

Then open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## 🚀 How to Use

```
1. 🌐  Open the system in your browser
2. 📷  Upload a solar panel image (JPG / PNG)
3. ▶️   Click "Run Detection"
4. ⏳  Wait for SDS-YOLO to process the image
5. 🖼️  View the annotated detection output
6. 📊  Review soiling status, count, and confidence log
```

---

## 📸 Sample Output

```
┌──────────────────────────────────────┐
│       DETECTION RESULT               │
├──────────────────────────────────────┤
│  Panel Status  :  Soiling Detected   │
│  Detections    :  4                  │
│  Model         :  SDS-YOLO           │
│  Confidence    :  85%                │
├──────────────────────────────────────┤
│  Classes Found :  Dust, Bird-Drop    │
└──────────────────────────────────────┘
```

The output image includes:
- 🟩 Bounding boxes around soiling regions
- 🏷️ Class labels (`Dust` / `Bird-Droppings`)
- 📈 Per-detection confidence percentages

---

## 🧪 Google Colab Testing

The SDS-YOLO model was also validated inside Google Colab:

```
1. 📂  Mount Google Drive
2. 📦  Load dataset and model weights
3. 🚀  Run YOLOv5 detect.py on test images
4. 🖼️  Display annotated detection results
5. 📊  Evaluate mAP and class-wise performance
```

> Model weights can be stored in Google Drive and loaded directly for Colab inference.

---

## ⚠️ Known Limitation

> The current system detects only **Dust** and **Bird-Droppings**. It does **not** validate whether the uploaded image is an actual solar panel.

Non-panel images may occasionally produce false positive detections.

---

## ✅ Recommended Improvement (Two-Stage Pipeline)

For a production-grade system, a **validation stage** should be added before detection:

```
Stage 1 → 🔍 Solar Panel Validator
          Check if uploaded image contains a solar panel

Stage 2 → 🤖 SDS-YOLO Detector
          If panel confirmed → run dust / bird-dropping detection

Stage 3 → 📊 Output Results
          Display annotated image + confidence log
```

This significantly reduces false positives from unrelated images.

---

## 🌱 Future Enhancements

- [ ] 🔍 Add solar panel image validation (Stage 1 classifier)
- [ ] 🕐 Detection history and session logging
- [ ] ☁️ Cloud storage for images and results (Google Drive / AWS S3)
- [ ] 👤 User authentication and role management
- [ ] 📊 Admin dashboard for maintenance teams
- [ ] 📄 Downloadable PDF detection reports
- [ ] 🌍 Online deployment (Docker + cloud hosting)
- [ ] 📱 Mobile-responsive PWA interface

---

## 📊 Use Cases

| Industry | Application |
|----------|-------------|
| ⚡ Energy | Solar farm contamination monitoring |
| 🏭 Industrial | Automated panel inspection pipelines |
| 🔬 Research | Soiling dataset collection and benchmarking |
| 🎓 Academic | Computer vision and YOLO-based project work |
| 🤖 Smart Systems | Integration with IoT panel monitoring systems |

---

## 🧩 File Reference

| File | Role |
|------|------|
| `sds_yolo_best.pt` | Trained SDS-YOLO detection model |
| `app.py` | Flask backend — API routes and server |
| `detect.py` | YOLOv5 detection runner |
| `index.html` | Frontend page structure |
| `style.css` | Frontend styling and layout |
| `script.js` | Frontend API calls and dynamic rendering |
| `requirements.txt` | Python package dependencies |

---

## 👨‍💻 Developer

<div align="center">

**Kosala Daneshwara Athapaththu**
<br/>
*Intern — Sri Lanka Telecom (SLT)*
<br/>
🏢 SLT — Sri Lanka Telecom PLC

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-kosaladathapththu-181717?style=for-the-badge&logo=github)](https://github.com/kosaladathapththu)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Kosala%20D.%20Athapaththu-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/kosala-d-athapaththu-a453b9248/)
[![Email](https://img.shields.io/badge/Email-kosalaathapaththu1234%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:kosalaathapaththu1234@gmail.com)

</div>

---

## 📄 License

This project is developed for **academic and research purposes**.

---

<div align="center">

```
╔══════════════════════════════════════════════════════╗
║       🌞  SDS-YOLO Solar Panel Soiling Detection    ║
║              Detect · Analyze · Maintain             ║
╚══════════════════════════════════════════════════════╝
```

*Built with ☀️ and Python · SLT Internship Project by Kosala Daneshwara Athapaththu*

</div>
