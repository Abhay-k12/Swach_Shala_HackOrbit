# Swach_Shala_HackOrbit
# 🧼 AI-Powered Hygiene Monitoring System for Schools

**HackOrbit 2025 – Team Tech Titans**

## 💡 Problem Statement

In rural and government schools of India, hygiene areas (toilets, kitchens, drinking water zones) often lack proper maintenance. Manual checks are irregular and unreliable, risking children's health. Our goal is to automate hygiene monitoring using AI-driven image analysis.

---

## 🚀 Solution Overview

We built a lightweight AI system to:

* 📸 Collect hygiene images via mobile/form
* 🤖 Analyze images using a TensorFlow Lite model
* 📊 Assign a hygiene score (0–100) based on detected issues
* 📃 Auto-generate improvement suggestions
* 🌐 Display data on a real-time dashboard
* 🔔 Trigger alerts when hygiene scores fall below threshold

---

## 🔧 Work Completed (Technical Progress)

### ✅ Data Collection

* Collected 2000+ sample images representing hygiene conditions (clean/dirty toilets, kitchens, taps, dustbins).
* Images sourced from open datasets and real environments (with permissions).

### ✅ Data Preprocessing

* Resized images to 240x240 resolution.
* Performed normalization and augmentation (rotation, brightness adjustments).
* Categorized images into labels: `trash`, `leak`, `dirty_floor`, `overflowing_bin`, `clean`.

### ✅ Model Development

* Built a Convolutional Neural Network (CNN) using TensorFlow/Keras.
* Converted and optimized model to TensorFlow Lite for mobile deployment.
* Trained model on augmented dataset for binary and multi-class classification of hygiene issues.
* Achieved \~92% accuracy on validation set.

---

## 🧠 Tech Stack

* **AI/ML:** Python, TensorFlow, TensorFlow Lite, OpenCV
* **Data:** Firebase (Realtime DB + Storage), Google Forms (initial data intake)
* **Frontend:** HTML, CSS, JavaScript
* **Deployment:** Firebase Hosting / Flask for backend (WIP)

---

## 📈 Key Features

* AI-based hygiene detection from images
* Score-based cleanliness evaluation
* Auto-generated suggestions for improvement
* Scalable dashboard to monitor multiple schools
* Low-cost, sensor-free solution using just photos

---

## ⚠️ Challenges & Solutions

| Challenge                  | Solution                                                     |
| -------------------------- | ------------------------------------------------------------ |
| Low-light images           | Applied brightness correction, filtered poor-quality uploads |
| No Internet at rural sites | Offline image capture with sync support                      |
| Inconsistent uploads       | App-level reminders & notifications                          |

---
