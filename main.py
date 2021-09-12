import requests
import datetime
import os

API_KEY = os.environ["NUTRITIONIX_KEY"]
APP_ID = os.environ["NUTRITIONIX_APP_ID"]
# uses bearer authentication to interact with a spreadsheet
API_TOKEN = os.environ["SHEET_TOKEN"]

GENDER = "female"
WEIGHT = 52
HEIGHT = 158
AGE = 19

NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]

request_body = {
    "query": input("Tell me which exercises you did: "),
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

user_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0"
}

# makes and API request and decodes output to JSON format
nutritionix_response = requests.post(url=NUTRITIONIX_ENDPOINT, json=request_body, headers=user_headers)
result = nutritionix_response.json()

# gets today's date and time in specific format
today = datetime.datetime.today()
date = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")

header = {
    "Authorization": f"Bearer {API_TOKEN}"
}
# goes through the output exercises and adds information to "contents" dictionary
for exercise in result["exercises"]:
    contents = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise["name"],
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    # uses Sheety API to turn JSON API into spreadsheet and post it to Google Sheets
    sheety_response = requests.post(url=SHEETY_ENDPOINT, json=contents, headers=header)

    print(sheety_response.text)

