# agents/news_agent.py

from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()

def get_news_grabber_agent(llm: LLM) -> Agent:
    from src.shared.tools.newsChecker import NewsCheckTool
    from src.shared.tasks.portfolio_project_tasks import PortfolioTasks

    news_checker = NewsCheckTool()

    return Agent(
        name="news-grabber",
        role="Crypto News Fetcher",
        goal=(
            "Given a cryptocurrency symbol or name, fetch the top 3 latest news "
            "headlines, links, and publication dates to inform portfolio decisions."
        ),
        backstory=(
            "You’re a crypto journalist turned AI agent—skilled at querying newsdata.io "
            "for breaking developments that could impact a user’s holdings."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[news_checker],
        ai_kwargs={"temperature": 0.0}
    )
