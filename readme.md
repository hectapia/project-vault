# 🔐 Project Vault (Local-First)

**Project Vault** is a secure, offline-capable desktop application for managing project budgets and expenses. It is designed for engineers and project coordinators who need to track financial data without relying on cloud subscriptions or internet access.

## 🚀 Features
* **Local-First:** All data is stored in a local SQLite database (`vault.db`) on your machine.
* **Project Management:** Create, Edit, and Delete projects with status tracking.
* **Financial Tracking:** Log transactions/expenses for each project.
* **Real-time Budgeting:** Automatically calculates remaining budget based on expenses.
* **Dark Mode:** Professional UI built with Bootstrap 5.
* **Cross-Platform:** Built on Electron, compatible with Windows, macOS, and Linux.

## 🛠️ Tech Stack
* **Frontend:** Electron + HTML5 + Bootstrap 5 (Dark Mode)
* **Backend:** Python (FastAPI)
* **Database:** SQLite
* **Architecture:** "Sidecar" pattern (Electron spawns a hidden Python API server)

---

## 💻 Development Setup

If you want to modify the code, follow these steps:

### 1. Prerequisites
* [Node.js](https://nodejs.org/) installed.
* [Python 3.10+](https://www.python.org/) installed.

### 2. Installation
Clone the repository and enter the folder:
```bash
git clone [https://github.com/your-username/project-vault.git](https://github.com/your-username/project-vault.git)
cd project-vault
```


### 1. The Folder Structure

```
project-vault/
├── package.json          # Electron Config
├── electron-main.js      # The "Brain" of Electron (starts Python)
├── /src
│   ├── /ui               # React/HTML/CSS code (Frontend)
│   └── /backend          # Python code (Backend)
│       ├── main.py       # FastAPI/Flask entry point
│       ├── database.py   # SQLite logic
│       └── requirements.txt
└── /dist                 # Where the final .exe will live
```