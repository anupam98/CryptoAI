from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()


llm= LLM(model="openai/gpt-4")
def get_portfolio_analyser_agent(llm: LLM) -> Agent:
    return Agent(
        name="portfolio-analyser",
        role="Portfolio Analyser",
        goal=(
            "Given a dict of crypto holdings and how much of each they have , "
            "compute the total portfolio value, allocation percentages per asset, "
            "unrealized P/L, and key risk metrics (volatility, max drawdown)."
        ),
        backstory=(
            "You are a portfolio manager with 20 years of experience "
            "advising clients on diversification, asset allocation, and risk management."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        ai_kwargs={"temperature": 0.2}
    )