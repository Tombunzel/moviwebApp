import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('OPENAI_KEY')
URL = "https://chatgpt-42.p.rapidapi.com/chatbotapi"


def generate_recommendation(movies):
    payload = {
        "bot_id": "OEXJ8qFp5E5AwRwymfPts90vrHnmr8yZgNE171101852010w2S0bCtN3THp448W7kDSfyTf3OpW5TUVefz",
        "messages": [
            {
                "role": "user",
                "content": f"Here's a list of my favourite movies, "
                           f"can you recommend another movie based on my taste? {movies}"
                           f"Make your answer very short"
            }
        ],
        "user_id": "",
        "temperature": 0.9,
        "top_k": 5,
        "top_p": 0.9,
        "max_tokens": 256,
        "model": "gpt 3.5"
    }
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    return requests.post(URL, json=payload, headers=headers).json()['result']


def generate_review(movie_name):
    payload = {
        "bot_id": "OEXJ8qFp5E5AwRwymfPts90vrHnmr8yZgNE171101852010w2S0bCtN3THp448W7kDSfyTf3OpW5TUVefz",
        "messages": [
            {
                "role": "user",
                "content": f"Can you generate a very short review for the following movie: {movie_name}"
            }
        ],
        "user_id": "",
        "temperature": 0.9,
        "top_k": 5,
        "top_p": 0.9,
        "max_tokens": 256,
        "model": "gpt 3.5"
    }
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    return requests.post(URL, json=payload, headers=headers).json()['result']


def generate_trivia(movie_name):
    payload = {
        "bot_id": "OEXJ8qFp5E5AwRwymfPts90vrHnmr8yZgNE171101852010w2S0bCtN3THp448W7kDSfyTf3OpW5TUVefz",
        "messages": [
            {
                "role": "user",
                "content": f"Can you tell me a single fun trivia about this movie: {movie_name},"
                           f"make your answer only comprise of the trivia and nothing else."
            }
        ],
        "user_id": "",
        "temperature": 0.9,
        "top_k": 5,
        "top_p": 0.9,
        "max_tokens": 256,
        "model": "gpt 3.5"
    }
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    return requests.post(URL, json=payload, headers=headers).json()['result']
