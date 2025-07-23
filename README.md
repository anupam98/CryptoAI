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
```

---

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
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
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
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License
[MIT](LICENSE) (or specify your license)

---

## Contact / Help
- For questions, open an issue on GitHub.
- For security concerns, contact the maintainer directly. 
