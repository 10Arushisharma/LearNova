# 🚀 Learnova — Learn AI by Building AI

### An Interactive, AI-Powered Web Learning Platform for the Next Generation of AI Engineers.

<p align="center">
  <strong>Learn. Experiment. Build. Innovate.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/React-Web_App-61DAFB?logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-Programming-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/TypeScript-Frontend-3178C6?logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/Generative_AI-Powered-purple" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" />
</p>

---

## 📖 Overview

**Learnova** is an interactive, AI-powered web learning platform designed to transform how students and developers learn Artificial Intelligence, Machine Learning, Data Science, and Generative AI.

Traditional learning often revolves around passive video lectures, lengthy documentation, and theoretical explanations. Learnova takes a different approach by making learning **practical, interactive, and experience-driven.**

Instead of simply reading about algorithms, learners can experiment with mathematical concepts, write and execute Python code, debug implementations with an AI mentor, and build industry-relevant projects — all through an intuitive web-based learning environment.

Whether you're starting with Python or exploring advanced concepts like Large Language Models, Retrieval-Augmented Generation (RAG), and Vector Databases, Learnova provides a structured path from fundamentals to real-world implementation.

## ✨ Key Features

### 🧪 1. Interactive Python & ML Sandbox

Learn by experimenting with code and mathematical concepts in an interactive environment.

- Execute Python code and experiment with programming fundamentals.
- Explore mathematical operations used in Machine Learning.
- Perform matrix multiplication and dot product calculations.
- Visualize sigmoid activation functions and mathematical transformations.
- Understand vector operations and cosine similarity.
- Experiment with concepts instead of relying solely on theoretical explanations.

### 🤖 2. Socratic AI Mentor

An intelligent learning companion that encourages problem-solving rather than simply providing answers.

- Explains complex AI/ML concepts through intuitive examples.
- Identifies and helps diagnose errors in student code.
- Provides contextual hints and step-by-step guidance.
- Uses a Socratic teaching approach to encourage independent thinking.
- Breaks down mathematical intuition behind algorithms.
- Helps learners understand *why* something works, not just *how* to implement it.

### 🗺️ 3. Structured Learning Roadmaps

Progressive learning paths designed to take learners from beginner-level programming to advanced AI engineering.

| Learning Path | Topics Covered |
|---|---|
| 🐍 Python Foundations | Python syntax, data structures, functions, OOP, NumPy, Pandas |
| 📊 Data Science | Data preprocessing, EDA, visualization, statistics, feature engineering |
| 🤖 Machine Learning | Supervised learning, unsupervised learning, regression, classification, XGBoost |
| 🧠 Deep Learning | Neural networks, activation functions, backpropagation, CNNs, PyTorch |
| ✨ Generative AI | LLMs, prompt engineering, embeddings, Transformers |
| 🔍 AI Engineering | RAG, Vector Databases, LangChain, semantic search, AI applications |

### 🏗️ 4. Real-World Capstone Projects

Move beyond tutorials and develop practical projects that demonstrate real engineering skills.

**Featured Projects:**

**Customer Churn Prediction Engine**
- Build an end-to-end customer churn prediction pipeline.
- Apply data preprocessing, feature engineering, and exploratory data analysis.
- Train and evaluate predictive models using XGBoost.
- Understand model performance and prediction workflows.

**Enterprise Policy RAG Assistant**
- Build an intelligent document question-answering system.
- Process and transform enterprise documents into searchable representations.
- Generate embeddings and store them using ChromaDB.
- Implement retrieval workflows using LangChain.
- Generate context-aware responses using Large Language Models.

### 🎯 5. Gamified Learning Experience

Make consistent learning rewarding and engaging.

- Daily learning streaks.
- XP-based progression and rewards.
- Structured milestones and learning goals.
- Progress tracking across different learning paths.
- Engaging learning dashboards.

### 🎨 6. Modern Web Experience

- Clean, modern light-theme interface.
- Responsive web design.
- Intuitive navigation and structured learning dashboards.
- Interactive coding and learning components.
- Consistent typography and accessible UI elements.
- Seamless experience across desktop, tablet, and mobile browsers.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Frontend | React, TypeScript, JavaScript |
| Backend | Python, FastAPI |
| Programming | Python, TypeScript |
| AI / Machine Learning | NumPy, Pandas, Scikit-learn, XGBoost, PyTorch |
| Generative AI | LLMs, LangChain, RAG |
| Vector Database | ChromaDB |
| Mathematical Computing | NumPy, SciPy |
| API Communication | REST APIs |
| Development Tools | Git, GitHub, VS Code |

---

## 🏛️ System Architecture

Learnova follows a modular full-stack architecture that separates the frontend, backend services, and AI-powered learning capabilities.

```text
                 ┌──────────────────────────┐
                 │        LEARNOVA          │
                 │       Web Frontend       │
                 │     React + TypeScript   │
                 └────────────┬─────────────┘
                              │
                              │ REST API
                              ▼
                 ┌──────────────────────────┐
                 │      FastAPI Backend     │
                 │                          │
                 │  Authentication          │
                 │  Learning Management     │
                 │  Progress Tracking       │
                 │  AI Service Integration  │
                 └────────────┬─────────────┘
                              │
                 ┌────────────┴─────────────┐
                 ▼                          ▼
       ┌──────────────────┐       ┌──────────────────┐
       │    AI Mentor     │       │  Learning Engine │
       │                  │       │                  │
       │ LLM Integration  │       │ Python Sandbox   │
       │ Code Assistance  │       │ ML Experiments   │
       │ Concept Guidance │       │ Project Modules  │
       └──────────────────┘       └──────────────────┘
```

---

## 📂 Project Structure

```text
Learnova/
│
├── frontend/                   # React + TypeScript web application
│   ├── public/
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/              # Application pages
│   │   ├── layouts/            # Shared layouts
│   │   ├── hooks/              # Custom React hooks
│   │   ├── services/           # API integration
│   │   ├── context/            # Application state
│   │   ├── assets/             # Images and static assets
│   │   └── utils/              # Helper utilities
│   └── package.json
│
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/                # API endpoints
│   │   ├── core/               # Configuration
│   │   ├── models/             # Data models
│   │   ├── services/           # Business logic
│   │   └── main.py             # Application entry point
│   └── requirements.txt
│
├── docs/                       # Project documentation
│
├── .gitignore
├── LICENSE
└── README.md
```

*Note: Update this structure to reflect the actual repository directories.*

---

## ⚙️ Getting Started

Follow these steps to run Learnova locally.

### Prerequisites

- Node.js (LTS)
- npm
- Python 3.10+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Learnova.git

cd Learnova
```

### 2. Set Up the Frontend

```bash
cd frontend

npm install
```

Start the development server:

```bash
npm run dev
```

Open the local development URL displayed in your terminal.

### 3. Set Up the Backend

Open a new terminal:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file inside the backend directory.

```env
APP_ENV=development
SECRET_KEY=your_secret_key
AI_API_KEY=your_ai_api_key
```

Add any additional environment variables required by your configured services.

**Important:** Never commit API keys, credentials, or sensitive environment variables to GitHub.

### 5. Run the Backend Server

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

---

## 🗺️ Learning Philosophy

Learnova is built around one simple principle:

> The best way to understand Artificial Intelligence is to build it, experiment with it, and learn from the results.

The platform emphasizes three core learning stages:

1. **Understand:** Build conceptual clarity through structured lessons and intuitive explanations.
2. **Experiment:** Apply concepts through interactive coding exercises and mathematical simulations.
3. **Build:** Develop real-world AI applications through guided projects and practical implementation.

---

## 🚀 Project Vision

The vision behind Learnova is to make AI education more accessible, practical, and engaging.

As Artificial Intelligence continues to reshape industries, understanding how these systems work is becoming just as important as knowing how to use them.

Learnova aims to bridge the gap between theoretical knowledge and practical engineering by providing an environment where learners can continuously experiment, solve problems, and build intelligent applications.

**From learning Python to building Generative AI systems — Learnova makes the journey hands-on.**

---

## 🤝 Contributing

Contributions, suggestions, and feature improvements are welcome!

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes:

```bash
git commit -m "Add: your feature description"
```

4. Push your branch:

```bash
git push origin feature/your-feature-name
```

5. Open a Pull Request.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Arushi Sharma**

B.Tech Computer Science & Engineering

Interested in Artificial Intelligence, Machine Learning, Generative AI, and building impactful software products.

- GitHub: [@10Arushisharma](https://github.com/10Arushisharma)

---

<p align="center">
  <strong>⭐ If you find Learnova interesting, consider starring the repository!</strong>
</p>

<p align="center">
  Built with ❤️ to make AI learning practical, interactive, and accessible.
</p>
