# 🤖 AI Chatbot with Gemini + Smart Tool Routing (Full Stack)

A full-stack chatbot powered by **Google Gemini** and enhanced with real-world tools like weather, calculator, stock price, tech news, and code explainer. Built using **FastAPI** for the backend and **React** for the frontend.

---

## 📁 Project Structure

```
chatbot-gemini-tools/
├── backend/       # FastAPI app (Gemini + tools)
│   ├── main.py
│   ├── tools.py
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/      # React chatbot UI
│   ├── src/
│   ├── public/
│   ├── .env.example
│   └── package.json
```

---

## 🧠 Features

- 🔍 Intelligent tool routing using Gemini LLM
- 🛠️ Built-in tools:
  - Weather info
  - Stock prices
  - Calculator
  - Tech news
  - Code explanation
- 💬 Gemini handles open-ended/general queries
- 🎯 Modular, lightweight and production-ready structure

---

## ⚙️ Setup Instructions

### 🔧 Backend Setup (FastAPI)

#### Prerequisites:
- Python 3.10+
- Gemini API Key
- Weather API Key (OpenWeather)
- News API Key (NewsAPI)

#### Steps:

```bash
cd backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Fill in .env with your actual API keys
```

To run the server:
```bash
uvicorn main:app --reload
```

API will be live at: `http://localhost:8000/chat`

---

### 💻 Frontend Setup (React)

#### Prerequisites:
- Node.js & npm (or yarn)

#### Steps:

```bash
cd frontend
npm install

# Set up environment
cp .env.example .env
# Update REACT_APP_BACKEND_URL in .env to: http://localhost:8000
```

To run the frontend:

```bash
npm start
```

App will open in browser at: `http://localhost:3000`

---

## 📽️ Demo

🎥 **Video Walkthrough**: [Insert YouTube or Google Drive demo link here]

---

## 🌐 Deployment

You can host this full stack on:

- **Backend (FastAPI)**: Render, Railway, Fly.io
- **Frontend (React)**: Vercel, Netlify, Firebase Hosting

Make sure to update `.env` variables to production endpoints before deploying.

---

## 💡 Future Enhancements

- LangGraph orchestration
- WebSocket for streaming responses
- User authentication
- Session memory
- Voice interaction

---

## 👨‍💻 Author

Built by [@Preetham041199](https://github.com/Preetham041199)

---

> If you found this helpful or inspiring, give the repo a ⭐ on GitHub!