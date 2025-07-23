<<<<<<< HEAD
# CryptoAI

A modular cryptocurrency portfolio management system with AI-powered analysis, a web portal, CLI tool, and backend services.

---

## 📁 Project Structure

```
CryptoAI/
├── src/
│   ├── cli_server/                # Command-line interface tool
│   ├── mcp_server/                # AI/Backend service (e.g., portfolio analysis)
│   ├── shared/                    # Shared agents, tools, and tasks
│   │   ├── agents/
│   │   ├── tools/
│   │   └── tasks/
│   └── web_application_server/    # Streamlit web portal
│       └── app.py
├── venv/                          # Python virtual environment (ignored)
├── knowledgebase/                 # Reference documents (e.g., whitepapers)
├── requirements.txt               # Python dependencies
├── .gitignore
├── streamlit_app.py               # Entry point for Streamlit deployment
├── test_db.py                     # Local test script (ignored)
├── portfolios.db                  # Local database (ignored)
├── LICENSE
├── README.md
└── dockerfile
=======
# Crypto Portfolio Advisor

A modern, AI-powered crypto portfolio analysis and recommendation platform. This project includes:
- A Streamlit web app for interactive portfolio analysis
- An MCP (Multi-Agent Communication Protocol) server for agent-based queries (e.g., via Claude Desktop)
- Modular agents and tools for price fetching, news, risk assessment, and more

---

## Features
- 📊 **Portfolio Analysis**: Analyze your crypto holdings and get AI-powered insights
- 💡 **Investment Recommendations**: Receive tailored suggestions for portfolio improvement
- ⚠️ **Risk Assessment**: Understand the risk profile of your portfolio
- 📰 **News Integration**: See relevant news for your assets
- 🗃️ **Portfolio History**: Track and review past analyses
- 🤖 **MCP Server**: Query your portfolio from agent clients (e.g., Claude Desktop)

---

## Folder Structure
```
crewaipratice/
├── app.py                # Streamlit web app
├── main.py               # CLI/analysis entrypoint
├── portfolio_mcp_server.py # MCP server for agent-based queries
├── requirements.txt      # Python dependencies
├── dockerfile            # Docker build file
├── .gitignore            # Files/folders to exclude from Git
├── .dockerignore         # Files/folders to exclude from Docker builds
├── portfolios.db         # (Ignored) SQLite database
├── agents/               # Agent modules (price, news, etc.)
├── tools/                # Custom tools
├── tasks/                # Task definitions
├── knowledgebase/        # (Optional) Whitepapers, PDFs, etc.
└── ...
>>>>>>> 6e6f85e2359d1730dc6cc7ad2a350f5627b8514e
```

---

<<<<<<< HEAD
## 🚀 Components

- **Web Application Server** (`src/web_application_server/`):  
  Streamlit-based web portal for portfolio management and analysis.

- **CLI Server** (`src/cli_server/`):  
  Command-line tool for managing and analyzing portfolios.

- **MCP Server** (`src/mcp_server/`):  
  Backend/AI service for advanced portfolio analysis and recommendations.

- **Shared** (`src/shared/`):  
  Common agents, tools, and tasks used by all services.

- **Knowledgebase**:  
  Reference documents (e.g., crypto whitepapers) for AI-powered document search.

---

## 🛠️ Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/cryptoai.git
   cd cryptoai
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

=======
## Setup Instructions

### 1. Local Development
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/crypto-portfolio-advisor.git
   cd crypto-portfolio-advisor
   ```
2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
>>>>>>> 6e6f85e2359d1730dc6cc7ad2a350f5627b8514e
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
<<<<<<< HEAD

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
# Example (customize as needed)
python src/cli_server/main.py --help
```

### MCP/AI Service

```bash
# Example (customize as needed)
python src/mcp_server/server.py
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

=======
4. **(Optional) Set up environment variables:**
   - Create a `.env` file for API keys (e.g., OpenAI, news APIs). See `.gitignore` to ensure it won't be committed.
5. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
6. **Run the MCP server (for agent/Claude Desktop integration):**
   ```bash
   python portfolio_mcp_server.py
   ```

### 2. Docker
1. **Build the Docker image:**
   ```bash
   docker build -t crypto-portfolio-advisor .
   ```
2. **Run the Streamlit app in Docker:**
   ```bash
   docker run -p 8501:8501 crypto-portfolio-advisor
   ```
   - The app will be available at [http://localhost:8501](http://localhost:8501)
3. **Run the MCP server in Docker (optional):**
   - Edit the `CMD` in `dockerfile` to `CMD ["python", "portfolio_mcp_server.py"]` and rebuild.
   - Run with `docker run -p 8050:8050 crypto-portfolio-advisor`

---

## Security & Best Practices
- **Sensitive Data:** `.gitignore` and `.dockerignore` are set to exclude `portfolios.db`, `.env`, and other sensitive files from Git and Docker images.
- **API Keys:** Store all API keys in a `.env` file. Never commit this file to Git.
- **Database:** The SQLite database is for local use only. For production, use a managed database and update `DATABASE_URL` accordingly.

---

## Usage
- **Web App:**
  - Open [http://localhost:8501](http://localhost:8501) after running `streamlit run app.py` or the Docker container.
  - Enter your portfolio (e.g., `BTC:1.5, ETH:10`) and analyze.
  - View history, recommendations, risk, and news.
- **MCP Server:**
  - Start with `python portfolio_mcp_server.py`.
  - Connect from Claude Desktop or any MCP-compatible client at `http://localhost:8050`.
  - Use tools like `get_portfolio_history`, `get_latest_portfolio`, etc.

---

## Contributing
>>>>>>> 6e6f85e2359d1730dc6cc7ad2a350f5627b8514e
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

<<<<<<< HEAD
## 📄 License

This project is licensed under the MIT License. 
=======
## License
[MIT](LICENSE) (or specify your license)

---

## Contact / Help
- For questions, open an issue on GitHub.
- For security concerns, contact the maintainer directly. 
>>>>>>> 6e6f85e2359d1730dc6cc7ad2a350f5627b8514e
