import asyncio
import json
import os
from dataclasses import dataclass
from contextlib import asynccontextmanager
from typing import AsyncIterator
from mcp.server.fastmcp import FastMCP, Context
from sqlalchemy import Column, Float, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker  # Fixed deprecation
from datetime import datetime
import logging
import re

logging.basicConfig(filename="mcp_server_logs.log",level=logging.DEBUG,format='%(asctime)s:%(levelname)s:%(message)s')


# Debug information
logging.debug(f"Current working directory: {os.getcwd()}")

# Use the full path to ensure we're using the same database
DATABASE_URL = "sqlite:///C:/Users/anupa_gtxnlgd/Downloads/crewai/crewaipratice/portfolios.db"
logging.debug(f"Using DATABASE_URL: {DATABASE_URL}")

# Check if the database file actually exists
db_path = "C:/Users/anupa_gtxnlgd/Downloads/crewai/crewaipratice/portfolios.db"
logging.debug(f"Database file exists: {os.path.exists(db_path)}")

engine = create_engine(DATABASE_URL)
logging.debug(f"Engine URL: {engine.url}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



def validate_crypto_symbol(crypto_symbol: str) -> str:
    if not crypto_symbol or not crypto_symbol.strip():
        raise ValueError("Crypto symbol cannot be empty")
    cleaned=crypto_symbol.strip().upper()
    if not re.fullmatch(r"^[A-Z0-9]+$",cleaned):
        raise ValueError(f"Invalid crypto symbol: {crypto_symbol}")
    return cleaned

def validate_user_id(uid: str) -> str:
    if not uid or not uid.isdigit():
        raise ValueError("user_id must be a string of digits")
    return uid

def validate_portfolio_id(pid: int) -> int:
    if not pid or not isinstance(pid, int):
        raise ValueError("portfolio_id must be an integer")
    return pid

# Define Portfolio class early to avoid NameError
class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    holdings = Column(String)        # JSON-encoded list
    total_val = Column(Float)
    analysis = Column(String)        # raw Crew analysis
    recommendation = Column(String)  # raw Crew recommendations
    risk = Column(String)
    further_reading = Column(String) # raw Crew risk output
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables after model definition
Base.metadata.create_all(bind=engine)

@dataclass
class PortfolioContext:
    db: sessionmaker

@asynccontextmanager
async def portfolio_lifespan(server: FastMCP) -> AsyncIterator[PortfolioContext]:
    logging.debug("Entering portfolio_lifespan context manager")
    yield PortfolioContext(db=SessionLocal)

mcp = FastMCP(
    "portfolio-analyzer",
    description="MCP server for portfolio storage and analysis",
    lifespan=portfolio_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=int(os.getenv("PORT", "8050"))
)

def get_latest_portfolio(user_id: str = "1"):
    uid=validate_user_id(user_id)
    logging.debug(f"Querying for user_id: {user_id} (type: {type(user_id)})")
    with SessionLocal() as session:
        # Now try the actual query
        portfolio = session.query(Portfolio).filter(Portfolio.user_id == uid).order_by(Portfolio.created_at.desc()).first()
        logging.debug(f"Found portfolio: {portfolio}")
        return portfolio

@mcp.tool()
async def get_portfolio_history(ctx: Context, user_id: str = "1") -> str:
    uid=validate_user_id(user_id)
    db = ctx.request_context.lifespan_context.db()
    try:
        portfolios = db.query(Portfolio).filter(Portfolio.user_id == uid).all()
        logging.debug(f"Found {len(portfolios)} portfolios for user_id: {user_id}")
        history = [
            {
                "id": p.id,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "total_value": p.total_val,
                "holdings": json.loads(p.holdings)
            }
            for p in portfolios
        ]
        return json.dumps(history, indent=2) if history else "No portfolios found for this user."
    finally:
        db.close()

@mcp.tool()
async def get_portfolio_details(ctx: Context, portfolio_id: int) -> str:
    pid=validate_portfolio_id(portfolio_id)
    logging.debug(f"get_portfolio_details called with portfolio_id: {portfolio_id}")
    db = ctx.request_context.lifespan_context.db()
    try:
        p = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        logging.debug(f"Portfolio found: {bool(p)}")
        if not p:
            return "Portfolio not found"
        details = {
            "id": p.id,
            "user_id": p.user_id,
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "total_value": p.total_val,
            "holdings": json.loads(p.holdings),
            "analysis": p.analysis,
            "recommendations": p.recommendation,
            "risk_assessment": p.risk,
            "news": json.loads(p.further_reading) if p.further_reading else []
        }
        return json.dumps(details, indent=2)
    finally:
        db.close()

@mcp.tool()
async def get_latest_portfolio(ctx: Context, user_id: str = "1") -> str:
    uid=validate_user_id(user_id)
    logging.debug(f"get_latest_portfolio called with user_id: {user_id}")
    db = ctx.request_context.lifespan_context.db()
    try:
        p = db.query(Portfolio).filter(Portfolio.user_id == uid).order_by(Portfolio.created_at.desc()).first()
        logging.debug(f"Latest portfolio found: {bool(p)}")
        if not p:
            return "No portfolios found for this user."
        latest = {
            "id": p.id,
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "total_value": p.total_val,
            "holdings": json.loads(p.holdings),
            "analysis_preview": p.analysis[:200] + "..." if p.analysis and len(p.analysis) > 200 else p.analysis
        }
        return json.dumps(latest, indent=2)
    finally:
        db.close()

@mcp.tool()
async def search_portfolios_by_crypto(ctx: Context, crypto_symbol: str, user_id: str = "1") -> str:
    crypto_symbol=validate_crypto_symbol(crypto_symbol)
    uid=validate_user_id(user_id)
    logging.debug(f"search_portfolios_by_crypto called with crypto_symbol: {crypto_symbol}, user_id: {user_id}")
    db = ctx.request_context.lifespan_context.db()
    try:
        portfolios = db.query(Portfolio).filter(Portfolio.user_id == uid).all()
        logging.debug(f"Found {len(portfolios)} portfolios for user_id: {uid}")
        matches = []
        for p in portfolios:
            holdings = json.loads(p.holdings)
            for h in holdings:
                if h.get("crypto", "").upper() == crypto_symbol.upper():
                    matches.append({
                        "portfolio_id": p.id,
                        "created_at": p.created_at.isoformat() if p.created_at else None,
                        "total_portfolio_value": p.total_val,
                        "crypto_holding": h
                    })
                    break
        logging.debug(f"Found {len(matches)} matching portfolios for crypto_symbol: {crypto_symbol}")
        return json.dumps(matches, indent=2) if matches else f"No portfolios found containing {crypto_symbol}"
    finally:
        db.close()

@mcp.tool()
async def get_portfolio_summary(ctx: Context, user_id: str = "1") -> str:
    uid=validate_user_id(user_id)
    logging.debug(f"get_portfolio_summary called with user_id: {user_id}")
    db = ctx.request_context.lifespan_context.db()
    try:
        portfolios = db.query(Portfolio).filter(Portfolio.user_id == uid).all()
        logging.debug(f"Found {len(portfolios)} portfolios for user_id: {user_id}")
        if not portfolios:
            return "No portfolios found for this user."
        total_values = [p.total_val for p in portfolios if p.total_val]
        all_cryptos = set()
        for p in portfolios:
            for h in json.loads(p.holdings):
                all_cryptos.add(h.get("crypto", ""))
        summary = {
            "user_id": user_id,
            "total_portfolios": len(portfolios),
            "value_stats": {
                "min": min(total_values),
                "max": max(total_values),
                "avg": sum(total_values) / len(total_values),
                "latest": total_values[-1] if total_values else None
            },
            "unique_cryptocurrencies": sorted(list(all_cryptos)),
            "date_range": {
                "earliest": min([p.created_at for p in portfolios]).isoformat() if portfolios else None,
                "latest": max([p.created_at for p in portfolios]).isoformat() if portfolios else None
            }
        }
        return json.dumps(summary, indent=2)
    finally:
        db.close()

async def main():
    transport = os.getenv("TRANSPORT", "sse")
    if transport == 'sse':
        await mcp.run_sse_async()
    else:
        await mcp.run_stdio_async()

if __name__ == "__main__":
    # Test the database connection before starting MCP server
    logging.debug("Testing database connection...")
    
    try:
        result = get_latest_portfolio("1")
        logging.debug(f"Test result: {result}")
        if result:
            logging.debug(f"Portfolio found: ID={result.id}, user_id={result.user_id}, total_val={result.total_value}")
        else:
            logging.debug(" No portfolio found")
    except Exception as e:
        logging.debug(f" Error testing database: {e}")
    
    # Then start your MCP server
    asyncio.run(main())