import requests

from crewai.tools import BaseTool
from pydantic import BaseModel, Field,ConfigDict
import os




class NewsQuery(BaseModel):
    query: str= Field(..., description= " the crypto we are looking up")

class NewsCheckTool(BaseTool):
    name:str = "news Checker for crypto"
    description: str ="this finds the news of crypto"
    args_schema: type[BaseModel] = NewsQuery
    model_config = ConfigDict(extra="allow")

    

    def _run(self, query :str) -> str:

        url = " https://newsdata.io/api/1/latest"

        params = {
        "apikey": os.getenv("NEWSDATA_API_KEY"),
        "q": query,
        "language": "en",
       
    }
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            raise RuntimeError(f"newsdata.io returned {resp.status_code}: {resp.text}")

        data = resp.json()
        articles = data.get("results", [])
        if not articles:
            return []

        # Return top 3 headlines with link and pubDate
        top3 = []
        for art in articles[:3]:
            top3.append({
                "title": art.get("title"),
                "link": art.get("link"),
                "pubDate": art.get("pubDate"),
                "description":art.get("description")
            })
        return top3
    
def test_news_tool():
    tool = NewsCheckTool()
    print("we are ere now")
    try:
        # 2. Call it with a known crypto name
        results = tool._run("bitcoin")
        print("✅ Success! Here are the top 3 results:")
        for idx, art in enumerate(results, 1):
            print(f"\nResult #{idx}")
            print(" Title:      ", art["title"])
            print(" Link:       ", art["link"])
            print(" Published:  ", art["pubDate"])
            print(" Description:", art["description"])
    except Exception as e:
        print("❌ Something went wrong:", e)

if __name__ == "__main__":
    print("we are here")
    test_news_tool()