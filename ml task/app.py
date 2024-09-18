from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from models import PricingLogic
from sentiment import analyze_sentiment
from negotiation_chatbot import chat_with_gemini

app = FastAPI()

class NegotiationRequest(BaseModel):
    product_id: str
    user_id: str

class OfferRequest(BaseModel):
    user_id: str
    offer_price: float

class SentimentRequest(BaseModel):
    message: str

@app.post("/start-negotiation")
async def start_negotiation(request: NegotiationRequest):
    try:
        initial_price = PricingLogic.get_initial_price(request.product_id)
        return {"message": f"The product's price is ${initial_price}. What is your offer?"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/submit-offer")  # Added the route as suggested
async def submit_offer(request: OfferRequest):
    try:
        counteroffer = PricingLogic.handle_user_offer(request.user_id, request.offer_price)
        bot_response = await chat_with_gemini(f"User offered ${request.offer_price}. Counter with a response.")
        return {"bot_response": bot_response, "counteroffer": counteroffer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/accept-offer")
async def accept_offer(request: OfferRequest):
    return {"message": f"Thank you for accepting the offer of ${request.offer_price}."}


@app.post("/sentiment-analysis")
async def sentiment_analysis(request: SentimentRequest):
    sentiment = analyze_sentiment(request.message)
    return {"sentiment": sentiment}
