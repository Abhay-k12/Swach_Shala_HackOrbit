# 🧼 SmartClean: AI-Powered Hygiene Monitoring System
**HackOrbit 2025 – Team Tech Titans**

---

## 💡 Problem Statement
In rural and government schools of India, hygiene conditions in essential areas like toilets, kitchens, and handwash stations are often poorly maintained due to irregular manual inspections and unreliable paper-based reports. This can lead to an unhealthy environment for children, increasing the risk of diseases.

Our goal is to develop a low-cost, AI-based hygiene monitoring system that automates cleanliness checks using image analysis and provides real-time reports to school authorities and district officers.

---

## 🚀 Solution Overview
SmartClean is an AI-powered hygiene audit platform that allows school staff to upload images of hygiene-critical areas. Our trained AI model analyzes these images to detect cleanliness-related issues such as:

- Presence of trash
- Dirty or wet floors
- Water leaks
- Absence of soap
- Overflowing bins

Based on the detection, a hygiene score is generated, and the system offers suggestions to improve cleanliness. The scores and reports are displayed on a real-time dashboard, with alert mechanisms for critical cases.

---

## 🧠 Key Features
- 🧠 **AI-Driven Analysis:** Detects hygiene issues from uploaded images
- 📊 **Auto Hygiene Scoring:** Generates a 0–100 score based on detected issues
- 📝 **Improvement Suggestions:** Recommends corrective actions
- 📈 **Dashboard View:** Displays reports, trends, and risk levels
- 🚨 **Alert System:** Sends notifications when hygiene score drops below threshold
- 📁 **Offline-Ready:** Designed for low-internet areas (sync on reconnect)
- 🧾 **PDF Export:** Allows downloading of detailed AI-generated reports

---

## 🖥️ UI Pages Summary
| Page           | Status        | Description |
|----------------|---------------|-------------|
| `index.html`   | ✅ Uploaded   | Landing page with project overview and CTA |
| `upload.html`  | ✅ Ready (local) | Upload image, preview, analyze via AI |
| `dashboard.html` | ✅ Ready (local) | Admin view with hygiene scores and trends |
| `alerts.html`  | ✅ Ready (local) | Critical hygiene alerts and resolution flow |
| `report.html`  | ✅ Ready (local) | Detailed report with image + PDF export |

> ⚠️ Only `index.html` has been pushed to GitHub so far. Remaining UIs are tested locally and ready to upload.

---

## 📂 Project Structure
```
📁 SmartClean
├── index.html          # Landing Page
├── upload.html         # Image Upload & AI Result Page
├── dashboard.html      # Reports Dashboard
├── alerts.html         # Hygiene Alerts & Tracking
├── report.html         # Detailed AI Report + PDF Download
├── dataset/            # Collected and Preprocessed Image Dataset
├── README.md           # Project Overview
```

---

## 🔧 Technical Progress
### ✅ Data Collection
- Over 300 labeled images across different hygiene categories
- Classes: `trash`, `no_soap`, `dirty_floor`, `clean`, etc.

### ✅ Preprocessing
- Image resizing to 224x224
- Brightness correction
- Rotation and flip augmentation for model generalization

### ✅ AI Model
- Convolutional Neural Network (CNN) using TensorFlow
- Trained on augmented, labeled hygiene dataset
- Achieved ~92% validation accuracy and 90% F1-score
- Fully tested on unseen images for all major hygiene classes
- Converted to TensorFlow Lite for mobile deployment
- Tested end-to-end inference using Flask and Firebase

### ✅ Frontend
- Developed 5 responsive and colorful HTML pages using Bootstrap
- jsPDF integration for downloading reports
- Chart.js used for score visualization in the dashboard

### ✅ Backend (in progress)
- Firebase Realtime Database and Storage integration for image uploads and score history

---

## 🧠 Tech Stack
| Purpose        | Tools Used |
|----------------|-------------|
| AI Model       | Python, TensorFlow, TensorFlow Lite |
| Data Handling  | OpenCV, NumPy |
| Frontend       | HTML5, CSS3, Bootstrap, JavaScript |
| Reporting      | jsPDF, Chart.js |
| Database/Auth  | Firebase |

---

## ⚠️ Challenges & Solutions
| Challenge | Solution |
|----------|----------|
| Poor image quality | Applied brightness checks & filtered blurred images |
| Internet unavailability | Added offline support for image sync |
| Upload inconsistency | Planned push notification reminders via mobile UI |

---

## 📆 Progress Timeline (HackOrbit 2025)
### 🗓️ Day 1 – July 8
- ✅ Finalized Idea
- ✅ Collected and Preprocessed Dataset
- ✅ AI Model Trained and Converted to TFLite
- ✅ `index.html` pushed to GitHub
- ✅ Local development of UI pages

### 🗓️ Day 2 – July 9 (Planned)
- 🛠️ Integrate Firebase
- 🛠️ Final Testing of UI Interactions
- 🛠️ Push Remaining UI Files to GitHub
- 🚨 Demo with PDF Export & Live Score Dashboard

---

## 📌 Current Status
✅ Dataset, Model, UI (local) completed
✅ Firebase integration to be done (Realtime DB + Storage)


---

## 🔗 Future Plans
- Mobile-friendly PWA version
- Hindi language support for rural users
- Role-based login for staff/admin/district
- Model auto-update via cloud retraining pipeline
  
---
