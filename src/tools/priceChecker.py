import requests

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class PriceList(BaseModel):
    query: str= Field(..., description= " the crypto we are looking up")

class PricecheckTool(BaseTool):
    name:str = "Price Checker for crypto"
    description: str ="this finds the price of crypto"
    args_schema: type[BaseModel] = PriceList

    

    def _run(self, query :str) -> str:
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"

            params = {
            "vs_currencies": "usd",
            "ids": query# CoinGecko IDs, not symbols
            
        }
            response = requests.get(url, params=params)

            if response.status_code==200:
                data=response.json()
                if not data:
                     return f"Issue with returned data-> Possible misspelling of the query ID{ query}"
                return response.text
            else:
                return ("Query Id is incorrect,, gave {response.status_code} for query {query}")
        except Exception as e:
                return f"Error: Query ID '{query}' caused exception: {str(e)}"
