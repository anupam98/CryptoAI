# CryptoAI

A modular cryptocurrency portfolio management system with AI-powered analysis, a web portal, CLI tool, and backend services.

---

## 📁 Project Structure

```
CryptoAI/
├── src/
│   ├── cli_server/                  # Command-line interface tool
│   │   └── main.py                  # CLI entry point
│   ├── mcp_server/                  # AI/Backend service
│   │   └── portfolio_mcp_server.py  # MCP server entry point
│   ├── shared/                      # Shared agents, tools, and tasks
│   │   ├── agents/
│   │   ├── tools/
│   │   └── tasks/
│   └── web_application_server/      # Streamlit web portal
│       └── app.py
├── venv/                            # Python virtual environment (ignored)
├── knowledgebase/                   # Reference documents (e.g., whitepapers)
├── requirements.txt                 # Python dependencies
├── .gitignore
├── streamlit_app.py                 # Entry point for Streamlit deployment
├── test_db.py                       # Local test script (ignored)
├── portfolios.db                    # Local database (ignored)
├── LICENSE
├── README.md
└── dockerfile
```

---

## 🚀 Components

- **Web Application Server** (`src/web_application_server/app.py`):  
  Streamlit-based web portal for portfolio management and analysis.

- **CLI Server** (`src/cli_server/main.py`):  
  Command-line tool for managing and analyzing portfolios.

- **MCP Server** (`src/mcp_server/portfolio_mcp_server.py`):  
  Backend/AI service for advanced portfolio analysis and recommendations.

- **Shared** (`src/shared/`):  
  Common agents, tools, and tasks used by all services.

- **Knowledgebase**:  
  Reference documents (e.g., crypto whitepapers) for AI-powered document search.

---

## 🛠️ Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anupam98/CryptoAI.git
   cd CryptoAI
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

### Web Portal

```bash
# From project root
streamlit run streamlit_app.py
```
or
```bash
streamlit run src/web_application_server/app.py
```

### CLI Tool

```bash
python src/cli_server/main.py --help
```

### MCP/AI Service

```bash
python src/mcp_server/portfolio_mcp_server.py
```

---

## 📝 Notes

- The `venv/`, `portfolios.db`, and `test_db.py` files are ignored by Git and should not be committed.
- Place any sensitive information (API keys, etc.) in a `.env` file (also ignored by Git).
- The `knowledgebase/` folder can be used for storing reference documents for AI-powered search.

---

## 📦 Docker

To build and run the project with Docker:

```bash
docker build -t cryptoai .
docker run -p 8501:8501 cryptoai
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License.
