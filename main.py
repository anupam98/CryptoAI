from crewai import LLM, Crew
from tasks.portfolio_project_tasks import PortfolioTasks
from agents.price_fetcher_agent import get_price_fetcher_agent
from agents.portfolio_analysis_agent import get_portfolio_analyser_agent
from agents.recommendation_agent import get_recommender_agent
from agents.risk_assesor_agent import get_risk_assesor_agent
import re

def main(holdings=None):
    if holdings is None:
        holdings = input("Enter your portfolio: ")
    # Configuration
    # currency = "bitcoin"
    llm = LLM(model="openai/o3-mini")

    portfolio_analyser_agent=get_portfolio_analyser_agent(llm)
    portfolio_tasks =PortfolioTasks()
    recommender_agent=get_recommender_agent(llm)





    # portfolio=[]
    fullport_portfolio=[]
    total_cost=0
    #Crew 1 that is calculating total cost of everything
    for s in holdings.split(","):
            if ":" in s:
                try:
                    crypto, quantity = s.split(":")
                except Exception as e:
                    print(f"failed to pase input properly {s} : {e}")
                    continue
                # portfolio.append({"crypto":crypto.strip(),"quantity":quantity.strip()})
                price_agent=get_price_fetcher_agent(llm)
                price_task=portfolio_tasks.create_price_fetch_task(crypto,quantity,price_agent)
                crew=Crew(agents=[price_agent],
                tasks=[price_task],
                verbose=True
        
                )
                result=crew.kickoff()
                try:
                    matches = re.findall(r"\b\d+(?:\.\d+)?\b", result.raw)

                    print("RAW TOOL OUTPUT:", result.raw)
                    print("REGEX MATCHES:", matches)
                    if matches:
                        value_str = matches[-1].replace(",", "").rstrip(".")
  # Get the last number in the string
                        value = float(value_str)
                        total_cost += value
                        print("total cost is " + str(total_cost))

                        fullport_portfolio.append({"crypto":crypto.strip(),
                                      "quantity":float(quantity.strip()),
                                      "value":value})
                    else:
                        print(f"Could not extract value for {crypto}")
                except Exception as e:
                    print(f"Failed to properly parse value for {crypto}: {e}")
                

    print(f"\nTotal Portfolio Value: ${total_cost:.2f}")
    

    #Analyzing the full portfolio
    portfolio_analysis_task =portfolio_tasks.create_portfolio_analysis_task(fullport_portfolio,total_cost,portfolio_analyser_agent)
    crew2=Crew(agents=[portfolio_analyser_agent],
                  tasks=[portfolio_analysis_task ],
                  verbose=True
)
    result2=crew2.kickoff()
    print(f"this is result 2{result2.raw}")
    
    
    # def recommendation_agent_task(self,portfolio:list,total_value:float,prior_analysis:str,agent) ->Task:

    #Now that we have calculated the whole portfolio and analyzed everything, we will recommend 3 things to balance out the portfolio
    recommender_task=portfolio_tasks.create_recommendation_agent_task(fullport_portfolio,total_cost,result2,recommender_agent)
    recommendation_crew=Crew(agents=[recommender_agent],
               tasks=[recommender_task],
                      verbose=True
    )
    result3=recommendation_crew.kickoff()
    print(f"this is result 3 {result3.raw}")

    risk_assesor_agent=get_risk_assesor_agent(llm)

    risk_assesor_task=portfolio_tasks.create_risk_assessment_task(fullport_portfolio,total_cost,result2,risk_assesor_agent)

    risk_crew =Crew(agents=[risk_assesor_agent],
               tasks=[risk_assesor_task],
                      verbose=True
    )

    risk_result  = risk_crew.kickoff()
    print(f"this is the risk result {risk_result.raw}")

    return {
    "total_value": total_cost,
    "analysis": result2.raw,
    "recommendation":result3.raw,
    "risk": risk_result.raw
}


if __name__ == "__main__":

    
    main()
