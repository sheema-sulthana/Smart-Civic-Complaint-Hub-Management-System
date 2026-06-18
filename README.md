# ComplaintHub – Smart Civic Complaint Management System

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📌 Project Overview

ComplaintHub is a modern web-based civic complaint management system designed to bridge the communication gap between citizens and municipal authorities.
Citizens can report civic issues, track complaint progress, provide feedback, and communicate problems efficiently, while administrators can monitor complaints through an interactive dashboard equipped with analytics and geolocation visualization.

---

# 🎯 Problem Statement

Traditional complaint systems often suffer from:

* Lack of transparency
* Slow response times
* Poor complaint tracking
* Language barriers
* Limited accessibility

ComplaintHub addresses these challenges through multilingual support, voice-assisted complaint registration, real-time analytics, and location-based complaint visualization.

---

# ✨ Features

## 👤 Citizen Features

### Complaint Registration

* Three-step complaint submission process
* Category selection
* Priority selection
* Image upload support
* Automatic complaint timestamping

---

### Voice Assistant

Users can describe their complaint using speech.

Supported Languages:

* English
* Hindi
* Telugu

Technology Used:

* Web Speech API

---

### Multi-language Support

Users can translate the website into:

* English
* Hindi
* Telugu

Technology Used:

Google Translate Widget

---

### Complaint Tracking

Citizens can track complaints using their registered phone number.

Displays:

* Complaint Status
* Category
* Priority
* Date and Time
* Uploaded Evidence

---

### Feedback System

Citizens can submit feedback after complaint resolution.

Reviews Supported:

* Excellent
* Good
* Average
* Poor

---

## 🛠️ Admin Features

### Admin Dashboard

Displays:

* Total Complaints
* Pending Complaints
* Resolved Complaints
* In Progress Complaints

---

### Interactive Maps

Complaint locations are displayed using colored markers.

Marker Colors:

🔴 Pending

🟠 In Progress

🟢 Resolved

Technologies Used:

Leaflet.js

OpenStreetMap

---

### Analytics Dashboard

Provides:

Complaint Status Distribution

Weekly Complaint Trends

Category-wise Analysis

High Priority Complaints

Feedback Statistics

Technology Used:

Chart.js

---

### Complaint Management

Admin can:

View complaints

Update complaint status

Delete complaints

Monitor complaint locations

View uploaded images

---

# 🧠 AI Assisted Features

Although ComplaintHub is not a complete machine learning application, it incorporates AI-assisted accessibility features.

### Speech Recognition

Technology:

Web Speech API

Functionality:

Converts voice input into complaint descriptions.

---

### Machine Translation

Technology:

Google Translate

Functionality:

Automatically translates website content into selected languages.

---

# 🛠 Technologies Used

## Frontend

HTML5

CSS3

JavaScript

---

## Backend

Python

Flask

---

## Database

SQLite3

---

## APIs & Libraries

Chart.js

Leaflet.js

OpenStreetMap

Google Translate Widget

Web Speech API

Font Awesome

Werkzeug

---

# 📂 Project Structure

ComplaintHub/

│

├── app.py

├── ComplaintHub.db

├── requirements.txt

├── README.md

│

├── static/

│   ├── css/

│   ├── images/

│   ├── js/

│   └── uploads/

│

├── templates/

│   ├── admin/

│   │   ├── admin_dashboard.html

│   │   ├── analytics.html

│   │   ├── complaints.html

│   │   ├── complaint_view.html

│   │   └── feedbacks.html

│

│   ├── index.html

│   ├── gallery.html

│   ├── contact.html

│   ├── track.html

│   ├── submit_complaint.html

---

# ⚙️ Installation Guide

## Clone Repository

git clone https://github.com/sheema-sulthana/ComplaintHub.git

cd ComplaintHub

---

## Install Dependencies

pip install -r requirements.txt

---

## Run Application

python app.py

---

Open browser

http://127.0.0.1:5000/

---

# 🔑 Admin Credentials

Username : admin

Password : admin123

---

# 🌍 Supported Languages

English

Hindi

Telugu

---

# 📸 Screenshots

check the screenshots in the folder structure



# ⭐ If you found this project useful, consider giving it a star on GitHub!
