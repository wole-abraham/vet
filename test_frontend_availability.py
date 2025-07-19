#!/usr/bin/env python3
"""
Test script to demonstrate that booked times are not shown in the frontend.
This script will:
1. Check what times are available
2. Book a specific time
3. Check available times again to show the booked time is removed
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

def test_frontend_availability():
    """Test that booked times are not shown in frontend"""
    print("🔍 Testing Frontend Availability - Booked Times Hidden")
    print("=" * 60)
    
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Step 1: Check initial available times
    print("📅 Step 1: Initial Available Times")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/available-slots/?selected_date={today}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Available times for {today}:")
            for i, slot in enumerate(data['available_slots'], 1):
                time_only = slot.split(' ')[1]
                print(f"   {i}. {time_only}")
            print(f"   Total: {len(data['available_slots'])} available slots")
            
            if data['available_slots']:
                # Step 2: Book the first available time
                first_slot = data['available_slots'][0]
                print(f"\n📝 Step 2: Booking {first_slot}")
                print("-" * 40)
                
                booking_data = {
                    'first_name': 'Test',
                    'last_name': 'User',
                    'email': 'test@example.com',
                    'phone_number': '555-0123',
                    'reason': 'Test booking',
                    'service_type': 'General Checkup',
                    'pet_type': 'dog',
                    'appointment_date': first_slot
                }
                
                # Create a simple image file for testing
                with open('test_image.jpg', 'wb') as f:
                    f.write(b'fake image data')
                
                with open('test_image.jpg', 'rb') as image_file:
                    files = {'image': ('test_image.jpg', image_file, 'image/jpeg')}
                    booking_response = requests.post(f"{BASE_URL}/book/", data=booking_data, files=files)
                
                if booking_response.status_code == 200:
                    result = booking_response.json()
                    print(f"✅ Successfully booked: {first_slot}")
                    print(f"   Booking ID: {result['booking_id']}")
                    
                    # Step 3: Check available times again
                    print(f"\n🔍 Step 3: Available Times After Booking")
                    print("-" * 40)
                    
                    response2 = requests.get(f"{BASE_URL}/available-slots/?selected_date={today}")
                    if response2.status_code == 200:
                        data2 = response2.json()
                        print(f"✅ Available times for {today} (after booking):")
                        
                        if data2['available_slots']:
                            for i, slot in enumerate(data2['available_slots'], 1):
                                time_only = slot.split(' ')[1]
                                print(f"   {i}. {time_only}")
                        else:
                            print("   No available times")
                        
                        print(f"   Total: {len(data2['available_slots'])} available slots")
                        
                        # Check if the booked time is no longer available
                        if first_slot not in data2['available_slots']:
                            print(f"\n✅ SUCCESS: Booked time {first_slot} is NOT shown in available slots!")
                            print("   This means the frontend will not display this time as an option.")
                        else:
                            print(f"\n❌ ERROR: Booked time {first_slot} is still shown in available slots!")
                            
                    else:
                        print(f"❌ Error checking slots after booking: {response2.status_code}")
                        
                else:
                    print(f"❌ Booking failed: {booking_response.status_code}")
                    
            else:
                print("❌ No available slots to test with")
                
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Clean up test file
        import os
        if os.path.exists('test_image.jpg'):
            os.remove('test_image.jpg')

if __name__ == "__main__":
    test_frontend_availability() 