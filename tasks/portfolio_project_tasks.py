from crewai import Task
from textwrap import dedent

class PortfolioTasks:

    def create_price_fetch_task(self, currency: str, quantity: str, agent) -> Task:
        return Task(
            description=(
                f"Fetch the current price for {currency} using the price checker tool. "
                f"Then multiply it by the quantity ({quantity}) to compute total value."
            ),
            agent=agent,
            expected_output="A float representing current price × quantity."
        )

    def create_portfolio_analysis_task(self, portfolio: list, total_value: float, agent) -> Task:
        return Task(
            description=(
                f"You are given a crypto portfolio with total value ${total_value:.2f}. "
                f"Each asset includes its name, quantity, and total value. "
                f"Compute allocation percentages, simulate unrealized P/L, "
                f"and provide dummy risk metrics (volatility, max drawdown). "
                f"Here is the portfolio: {portfolio}"
            ),
            agent=agent,
            expected_output="Bullet-point breakdown per asset with allocation %, P/L, and risk metrics."
        )

    def create_recommendation_agent_task(
        self,
        portfolio: list,
        total_value: float,
        prior_analysis: str,
        agent
    ) -> Task:
        return Task(
            description=dedent(f"""
                Here’s the analysis you produced:

                {prior_analysis}

                Given the portfolio {portfolio} (total value = ${total_value:.2f}), recommend **1** action to improve diversification or reduce risk:

                1. **Primary recommendation**: Call the `document-search` tool **once** with your query to fetch relevant background from our whitepapers (especially on risk factors), then ground your rationale in those retrieved passages.

                2. & 3. **Secondary recommendations**: For the remaining two actions, just provide `action` and `rationale` without using RAG.
            """),
            agent=agent,
            expected_output=dedent("""
                A string with the action and rationale provided by the whitepapers. specifically say what the whitepapers said
            """)
        )

    def create_risk_assessment_task(self, portfolio: list, total_value: float, prior_analysis: str, agent) -> Task:
        return Task(
            description=dedent(f"""
                Use the analysis you produced:
                
                {prior_analysis}
                
                to assess the portfolio with total value ${total_value:.2f}.
                Calculate and explain:
                - Portfolio volatility (std dev of daily returns)
                - Max drawdown
                - Concentration risk (Herfindahl Index)
            """),
            agent=agent,
            expected_output="Bullet-point summary of all risk metrics with explanations."
        )
    
    def create_related_news_task(self, currency: str, agent) -> Task:
        return Task(
            description=dedent(f"""
                Fetch the latest news articles related to the cryptocurrency "{currency}" 
                using the CryptoNewsTool. Provide the top 3 headlines, their URLs, and publication dates.
            """),
            agent=agent,
            expected_output="A list of 4 dicts, each with keys: 'title', 'link', 'description' and 'pubDate'."
        )

