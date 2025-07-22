# test_db.py
import json
from portfolio_mcp_server import SessionLocal, Portfolio

def main():
    session = SessionLocal()
    try:
        rows = session.query(Portfolio).all()
        for p in rows:
            print(f"ID={p.id}, user_id={p.user_id}, total_val={p.total_val}")
            print(" holdings:", json.loads(p.holdings))
            print("---")
    finally:
        session.close()

if __name__ == "__main__":
    main()
