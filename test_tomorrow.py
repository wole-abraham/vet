#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/api"

def test_tomorrow():
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    response = requests.get(f'{BASE_URL}/available-slots/?selected_date={tomorrow}')
    data = response.json()
    
    print(f'📅 Available times for {tomorrow}:')
    for slot in data['available_slots']:
        time_only = slot.split(' ')[1]
        print(f'  {time_only}')
    print(f'Total: {len(data["available_slots"])} slots')

if __name__ == "__main__":
    test_tomorrow() 