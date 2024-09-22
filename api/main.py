from src.course.crew import CourseCrew
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def read_item():
    inputs = {
        'topic': 'AI LLMs',
        "links": [
            "https://en.wikipedia.org/wiki/Artificial_intelligence"
        ]
    }
    return CourseCrew().crew().kickoff(inputs=inputs)