from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Profile(BaseModel):
    firstName: str
    lastName: str
    age: int
    sex: str
    email: str
    location: str
    interests: str
    needsSitter: bool
    spouseFirstName: str
    spouseLastName: str
    spouseAge: int
    spouseSex: str
    spouseEmail: str

def generate_ideas(interests: List[str], location: str) -> List[str]:
    ideas_bank = {
        "art": "🎨 Art exhibit and wine night",
        "food": "🍽️ Chef's table dinner downtown",
        "hike": "🥾 Guided scenic hike with picnic",
        "movie": "🎬 Drive-in movie + diner",
        "music": "🎶 Jazz & cocktails at a rooftop bar",
        "cooking": "👩‍🍳 Couples cooking class",
        "spa": "💆‍♂️ Couples spa & brunch"
    }

    results = [desc for key, desc in ideas_bank.items() if key in interests]
    if not results:
        results = random.sample(list(ideas_bank.values()), 3)
    return results[:3]

@app.post("/get-date-ideas")
async def get_date_ideas(profile: Profile):
    interest_keywords = [i.strip().lower() for i in profile.interests.split(",")]
    suggestions = generate_ideas(interest_keywords, profile.location)
    return {"suggestions": suggestions}