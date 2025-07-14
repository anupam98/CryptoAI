from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()


llm= LLM(model="openai/gpt-4")
def get_risk_assesor_agent(llm: LLM) -> Agent:
    return Agent(
        name="riskassesor-agent",
        role="riskassesor-agent",
        goal=("""adapted_agent=
              Using allications and price history, calculate the " \
            "" \
            ""Portfolio volatility (std dev of daily returns).
        Max drawdown,
        Concentration risk (e.g. Herfindahl index)


            """
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