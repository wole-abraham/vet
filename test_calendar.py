#!/usr/bin/env python3
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

def test_calendar():
    today = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(f'{BASE_URL}/availability-calendar/?start_date={today}')
    data = response.json()
    
    print('📅 Calendar Availability:')
    print('=' * 50)
    
    for day in data['calendar'][:7]:  # Show first 7 days
        status_icon = {
            'high': '🟢',
            'medium': '🟡', 
            'low': '🔴',
            'closed': '⚫'
        }.get(day['status'], '❓')
        
        print(f"{status_icon} {day['day_name']} ({day['date']}): {day['available_slots']} slots - {day['status']}")

if __name__ == "__main__":
    test_calendar() 