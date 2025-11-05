# Smart Inventory Management System

### *AI-powered product detection, analytics, and insights dashboard using YOLO, Streamlit, and Gemini AI.*

---

## 📖 Overview

**Smart Inventory Management System** is an intelligent, end-to-end inventory tracking application that uses **computer vision (YOLO)** to detect products in images (e.g., water bottles, soft drinks), store their counts in a **database**, and generate **real-time analytics and AI-driven insights** using **Google Gemini**.

This project demonstrates how AI, data visualization, and natural language understanding can come together to create a smart, interactive inventory dashboard for retail or warehouse environments.

---

## 🧱 Features

✅ **AI Product Detection**

* Detect items (CocaCola, Pepsi, Sprite, etc.) in images using YOLOv8.
* Automatically count items and log them into an SQLite database.
* Includes a dummy mode that simulates detections (10–20 items) for testing without a trained model.

✅ **Interactive Streamlit Dashboard**

* Upload images for detection.
* View real-time stock counts and top products.
* Analyze historical stock trends and low-stock alerts.
* Smooth, clean dark-themed UI.

✅ **Gemini AI Chatbot**

* Ask natural questions like:

  * “What’s low in stock?”
  * “Show me CocaCola trends this week.”
  * “Which products sold the most recently?”
* Gemini auto-generates SQL queries, executes them safely, and summarizes results in plain English.

✅ **Secure SQL Query Execution**

* Only read-only SQL queries (`SELECT`, `WITH`, etc.) are allowed.
* Prevents destructive commands (`UPDATE`, `DELETE`, etc.) for database safety.

✅ **Modular & Scalable Architecture**

* Separate modules for detection, database, and LLM integration.
* Ready for video feed automation every few hours.
* Easily extendable to multi-store or cloud database setups.

---

## 🧩 Tech Stack

| Component            | Technology           |
| -------------------- | -------------------- |
| **Frontend**         | Streamlit            |
| **Object Detection** | YOLOv8 (Ultralytics) |
| **Database**         | SQLite               |
| **Visualization**    | Plotly, Pandas       |
| **AI Assistant**     | Google Gemini API    |
| **Language**         | Python 3.9+          |

---

## 🗂️ Project Structure

```
smart_inventory_app/
│
├── app.py                # Main Streamlit app (UI + tabs)
├── db_utils.py           # Database setup and query helpers
├── detection_utils.py    # YOLO + dummy detection logic
├── llm_utils.py          # Gemini LLM logic + SQL generation
├── requirements.txt      # Python dependencies
└── inventory.db          # SQLite database (auto-created)
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/RajeshAndra/smart-inventory.git
cd smart-inventory
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure your Gemini API Key

Create a `.env` file or export it directly:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 6️⃣ Run the app

```bash
streamlit run app.py
```

---

## 🧠 Usage Guide

### **Tab 1 – Detect & Upload**

* Upload an image (`.jpg`, `.png`) of shelf products.
* The system detects items (dummy or YOLO).
* Displays the annotated image with bounding boxes and item counts.
* Automatically logs counts into the database.

---

### **Tab 2 – Analytics Dashboard**

* Displays total items, unique SKUs, and low-stock alerts.
* Bar chart of top 5 products by stock.
* Line chart showing product stock trends over time.
* Table of low-stock items (threshold < 10).

---

### **Tab 3 – AI Chatbot**

* Ask Gemini anything about inventory or sales:

  ```
  What is my current Pepsi stock?
  Which items are running low?
  Show daily sales for CocaCola this week.
  ```
* Gemini generates a SQL query, executes it, and gives a summarized insight.
* Supports analytical SQL (WITH, window functions, GROUP BY, etc.)
* Only read operations are allowed — no data modification.

---

## 🛡️ SQL Safety Rules

Allowed:

* `SELECT ...`
* `WITH ... SELECT ...`
* `JOIN`, `GROUP BY`, `ORDER BY`, `WINDOW FUNCTIONS`

Blocked:

* `UPDATE`, `INSERT`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `REPLACE`, `ATTACH`, etc.

This ensures the chatbot never modifies your database.

---

## 🔮 Future Enhancements

🚀 **Real-Time Video Feed Integration**

* Capture frames every few hours from CCTV or camera feeds.

📦 **Cloud Database (PostgreSQL / Firestore)**

* Migrate SQLite to a scalable cloud solution.

🤖 **Sales Forecasting**

* Use ML models (LSTM/Prophet) to predict future demand.

🔊 **Voice Query Support**

* Ask questions via speech-to-text interface.

👤 **Authentication System**

* Add login and role-based access for managers and staff.

---
