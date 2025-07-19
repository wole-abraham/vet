#!/usr/bin/env python3
"""
Test script to verify that time is being sent correctly in bookings.
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/api"

def test_time_fix():
    """Test that time is being sent correctly"""
    print("🔍 Testing Time Fix - Verify Correct Time in Bookings")
    print("=" * 60)
    
    # Get tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    try:
        # Step 1: Check available times for tomorrow
        print("📅 Step 1: Available Times for Tomorrow")
        print("-" * 40)
        
        response = requests.get(f"{BASE_URL}/available-slots/?selected_date={tomorrow}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Available times for {tomorrow}:")
            for i, slot in enumerate(data['available_slots'], 1):
                time_only = slot.split(' ')[1]
                print(f"   {i}. {time_only}")
            print(f"   Total: {len(data['available_slots'])} available slots")
            
            if data['available_slots']:
                # Step 2: Book a specific time
                selected_slot = data['available_slots'][0]  # First available slot
                print(f"\n📝 Step 2: Booking {selected_slot}")
                print("-" * 40)
                
                booking_data = {
                    'first_name': 'Time',
                    'last_name': 'Test',
                    'email': 'timetest@example.com',
                    'phone_number': '555-0123',
                    'reason': 'Time verification test',
                    'service_type': 'General Checkup',
                    'pet_type': 'dog',
                    'appointment_date': selected_slot  # This should be the full datetime
                }
                
                # Create a simple image file for testing
                with open('test_image.jpg', 'wb') as f:
                    f.write(b'fake image data')
                
                with open('test_image.jpg', 'rb') as image_file:
                    files = {'image': ('test_image.jpg', image_file, 'image/jpeg')}
                    booking_response = requests.post(f"{BASE_URL}/book/", data=booking_data, files=files)
                
                if booking_response.status_code == 200:
                    result = booking_response.json()
                    print(f"✅ Successfully booked!")
                    print(f"   Booking ID: {result['booking_id']}")
                    print(f"   Full datetime sent: {selected_slot}")
                    print(f"   Time component: {selected_slot.split(' ')[1]}")
                    
                    # Step 3: Check if the time is correct in the database
                    print(f"\n🔍 Step 3: Verifying Time in Database")
                    print("-" * 40)
                    
                    # Get all bookings to see the latest one
                    bookings_response = requests.get(f"{BASE_URL}/bookings/")
                    if bookings_response.status_code == 200:
                        bookings = bookings_response.json()
                        if bookings:
                            latest_booking = bookings[-1]  # Get the most recent booking
                            print(f"✅ Latest booking in database:")
                            print(f"   Booking ID: {latest_booking.get('id')}")
                            print(f"   Appointment Date: {latest_booking.get('appointment_date')}")
                            
                            # Check if the time is not 00:00:00
                            appointment_time = latest_booking.get('appointment_date', '')
                            if '00:00:00' not in appointment_time:
                                print(f"✅ SUCCESS: Time is correctly saved as {appointment_time}")
                            else:
                                print(f"❌ ERROR: Time is still showing as 00:00:00")
                        else:
                            print("❌ No bookings found in database")
                    else:
                        print(f"❌ Error getting bookings: {bookings_response.status_code}")
                        
                else:
                    print(f"❌ Booking failed: {booking_response.status_code}")
                    print(f"   Response: {booking_response.text}")
                    
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
    test_time_fix() 