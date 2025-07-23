from crewai import Agent, LLM
from dotenv import load_dotenv
from src.crypto_project.tools.custom_tool import DocumentSearchTool

load_dotenv()


llm= LLM(model="openai/gpt-4")
def get_recommender_agent(llm: LLM) -> Agent:
    return Agent(
        name="recommender-agent",
        role="recommender-agent",
         goal=(
            "You have a mapping of coin symbols to quantities. "
            "First, call the `price-checker` tool to fetch the current USD price for each symbol. "
            "Next, call the `quantity-calculator` tool to multiply each price by its quantity and compute the total value per asset and the overall portfolio value. "
            "Finally, consult the `document-searcha` tool on our crypto whitepapers for any relevant background on risk factors, and include a brief summary.Specifically mention" \
            "the fact you use the white papers when you read through it "
        ),
        backstory=(
            "You are a portfolio manager with 20 years of experience "
            "advising clients on diversification, asset allocation, and risk management."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[DocumentSearchTool(docs_folder="knowledgebase/")],
        ai_kwargs={"temperature": 0.2}
    )