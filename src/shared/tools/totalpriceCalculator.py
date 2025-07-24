import requests

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from shared.tools.priceChecker import PricecheckTool
import json

class PortfolioQuantity(BaseModel):
    query: str= Field(..., description= " the crypto we are looking up")
    quantity: str= Field(..., description=" how much crypto you own")


class PortfolioQuantityCalculator(BaseTool):
    name:str = "total Price Checker for crypto portfolio"
    description: str ="this finds the price of crypto portfolio in full "
    args_schema: type[BaseModel] = PortfolioQuantity

    
    
    def _run (self, query:str ,quantity: str)-> float:
        priceChecker=PricecheckTool()
        price=priceChecker._run(query)

        try:
            priceData=json.loads(price)
            price=priceData[query.lower()]["usd"]

            totalPriceofEquity=price*float(quantity)
        except Exception as e:
            return "returned json does not have expected price structure"

        return totalPriceofEquity
        


    


