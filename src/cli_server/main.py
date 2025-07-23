from crewai import LLM, Crew
from tasks.portfolio_project_tasks import PortfolioTasks
from agents.price_fetcher_agent import get_price_fetcher_agent
from agents.portfolio_analysis_agent import get_portfolio_analyser_agent
from agents.recommendation_agent import get_recommender_agent
from agents.risk_assesor_agent import get_risk_assesor_agent
from agents.news_grabber_agent import get_news_grabber_agent
import re
import json
from datetime import datetime
from sqlalchemy import Column, Float, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker  # Changed this line
import ast


DATABASE_URL = "sqlite:///./portfolios.db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Portfolio(Base):
    __tablename__ = "portfolios"
    id             = Column(Integer, primary_key=True)
    user_id        = Column(String, index=True)
    holdings       = Column(String)        # JSON-encoded list
    total_val      = Column(Float)
    analysis       = Column(String)        # raw Crew analysis
    recommendation = Column(String)        # raw Crew recommendations
    risk           = Column(String)   
    further_reading=Column(String)     # raw Crew risk output
    created_at     = Column(DateTime, default=datetime.utcnow)  # Added timestamp

# Create tables
Base.metadata.create_all(bind=engine)

def get_user_portfolios(user_id: str):
    db = SessionLocal()
    try:
        return db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
    finally:
        db.close()

def main(holdings=None):
    user_id = "1"
    
    if holdings is None:
        holdings = input("Enter your portfolio (e.g. BTC:1,ETH:2) or type 'history': ")

    # Handle history request
    if holdings.strip().lower() == "history":
        rows = get_user_portfolios(user_id)

        if not rows:
            print("No saved portfolios found.")
            return

        print("\nYour past portfolios:")
        for row in rows:
            holdings_list = json.loads(row.holdings)
            created_date = row.created_at.strftime("%Y-%m-%d %H:%M") if row.created_at else "Unknown"
            print(f"  ID={row.id}  Value=${row.total_val:.2f}  Date={created_date}  Holdings={holdings_list}")

        choice = input("\nEnter the ID whose recommendations you want to view: ").strip()
        try:
            sel = next(r for r in rows if str(r.id) == choice)
        except StopIteration:
            print("Invalid ID.")
            return

        print(f"\n▶ Analysis for portfolio #{sel.id}:\n{sel.analysis}")
        print(f"\n▶ Recommendations for portfolio #{sel.id}:\n{sel.recommendation}")
        print(f"\n▶ Risk Assessment for portfolio #{sel.id}:\n{sel.risk}")
        return

    # Fresh portfolio analysis
    db = SessionLocal()
    try:
        llm = LLM(model="openai/o3-mini")
        portfolio_analyser_agent = get_portfolio_analyser_agent(llm)
        portfolio_tasks = PortfolioTasks()
        recommender_agent = get_recommender_agent(llm)

        fullport = []
        total_cost = 0
        newsinfo=[]
        
        # Process each holding
        for s in holdings.split(","):
            if ":" in s:
                try:
                    crypto, quantity = s.split(":")
                    crypto = crypto.strip()
                    quantity = quantity.strip()
                    
                    # Get price
                    price_agent = get_price_fetcher_agent(llm)
                    price_task = portfolio_tasks.create_price_fetch_task(crypto, quantity, price_agent)
                    # get news
                    news_agent=get_news_grabber_agent(llm)
                    news_task=portfolio_tasks.create_related_news_task(crypto,news_agent)
                    crew = Crew(agents=[price_agent,news_agent], tasks=[price_task,news_task], verbose=True)
                    result = crew.kickoff()
                    print(" I am here before output of news and price result")
                    price_result = price_task.output  
                    news_result = news_task.output   
                    print (" this is news_result.raw" , news_result.raw)
                    print("Type of news_result.raw:", type(news_result.raw))

                    raw = news_result.raw

                    if isinstance(raw, str):
                        # Try to parse the string as JSON
                        try:
                            articles = json.loads(raw)
                        except json.JSONDecodeError:
                            # If JSON parsing fails, try to evaluate it as a Python literal
                            try:
                                articles = ast.literal_eval(raw)
                            except (ValueError, SyntaxError):
                                print("Error: Could not parse news_result.raw as JSON or Python literal")
                                print("Raw content:", raw[:500])  # Print first 500 chars for debugging
                                articles = []
                    else:
                        articles = raw

                    # Process the articles
                    for art in articles:
                        if isinstance(art, dict) and 'title' in art and 'link' in art:
                            newsinfo.append({
                                "title": art["title"],
                                "link": art["link"],
                            })

                    print("this is newsinfo:", newsinfo)  # Fixed: use comma instead of +

                    # Extract value from result
                    matches = re.findall(r"\b\d+(?:\.\d+)?\b", price_result.raw)
                    if matches:
                        value = float(matches[-1].replace(",", "").rstrip("."))
                        total_cost += value
                        fullport.append({
                            "crypto": crypto, 
                            "quantity": float(quantity), 
                            "value": value
                        })
                        print(f"Added {crypto}: {quantity} units = ${value:.2f}")
                    else:
                        print(f"Could not extract price for {crypto}")
                        
                except Exception as e:
                    print(f"Error processing {s}: {e}")
                    continue

        if not fullport:
            print("No valid holdings found.")
            return

        print(f"\nTotal Portfolio Value: ${total_cost:.2f}")

        # Analysis
        analysis_task = portfolio_tasks.create_portfolio_analysis_task(fullport, total_cost, portfolio_analyser_agent)
        crew2 = Crew(agents=[portfolio_analyser_agent], tasks=[analysis_task], verbose=True)
        result2 = crew2.kickoff()

        # Recommendations
        recomm_task = portfolio_tasks.create_recommendation_agent_task(fullport, total_cost, result2, recommender_agent)
        crew3 = Crew(agents=[recommender_agent], tasks=[recomm_task], verbose=True)
        result3 = crew3.kickoff()

        # Risk Assessment
        risk_agent = get_risk_assesor_agent(llm)
        risk_task = portfolio_tasks.create_risk_assessment_task(fullport, total_cost, result2, risk_agent)
        crew4 = Crew(agents=[risk_agent], tasks=[risk_task], verbose=True)
        risk_result = crew4.kickoff()

        # Persist to database
        new_port = Portfolio(
            user_id=user_id,
            holdings=json.dumps(fullport),
            total_val=total_cost,
            analysis=result2.raw,
            recommendation=result3.raw,
            risk=risk_result.raw,
            further_reading=json.dumps(newsinfo)  # ADD THIS LINE
        )
        db.add(new_port)
        db.commit()
        db.refresh(new_port)
        
        print(f"\nSaved portfolio with ID: {new_port.id}")
        
        # Display results
        print(f"\n{'='*50}")
        print("PORTFOLIO ANALYSIS COMPLETE")
        print(f"{'='*50}")
        print(f"Total Value: ${total_cost:.2f}")
        print(f"\nAnalysis:\n{result2.raw}")
        print(f"\nRecommendations:\n{result3.raw}")
        print(f"\nRisk Assessment:\n{risk_result.raw}")
        print(f"\n THIS IS NEWINFO: {newsinfo}")
        return {
            "portfolio_id": new_port.id,
            "total_value": total_cost,
            "holdings": fullport,
            "analysis": result2.raw,
            "recommendation": result3.raw,
            "risk": risk_result.raw,
            "further_reading":newsinfo
        }
    
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    main()