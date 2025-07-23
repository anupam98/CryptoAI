from crewai import Agent, LLM
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import requests
from crewai import Agent, Task, Crew
from src.crypto_project.tools.priceChecker import PricecheckTool
from src.crypto_project.tools.totalpriceCalculator import PortfolioQuantityCalculator

# test 
def get_price_fetcher_agent(llm) -> Agent:

    return Agent(
        name="price-fetcher",
        role="price fetcher",
        goal=(
                "Given a list of crypto holdings {currency} and there {quantity} calculate its current price point and total price."
            ),
        backstory=(
                "You are a portfolio manager with 20 years of experience "
                "advising clients on diversification, asset allocation, and risk management."
            ),
            verbose=True,
            allow_delegation=False,
            llm=llm,
            tools=[PricecheckTool(),PortfolioQuantityCalculator()],
            ai_kwargs={"temperature": 0.2}
        )


    
