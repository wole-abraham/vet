#!/usr/bin/env python3
"""
Simple test to verify time is saved correctly by checking available slots after booking.
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/api"

def test_time_verification():
    """Test that time is saved correctly"""
    print("🔍 Testing Time Verification")
    print("=" * 40)
    
    # Get tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    try:
        # Step 1: Check available times before booking
        print("📅 Step 1: Available Times Before Booking")
        print("-" * 30)
        
        response = requests.get(f"{BASE_URL}/available-slots/?selected_date={tomorrow}")
        if response.status_code == 200:
            data = response.json()
            print(f"Available times for {tomorrow}:")
            for slot in data['available_slots']:
                print(f"  {slot.split(' ')[1]}")
            print(f"Total: {len(data['available_slots'])} slots")
            
            if data['available_slots']:
                # Step 2: Book the first available time
                selected_slot = data['available_slots'][0]
                print(f"\n📝 Step 2: Booking {selected_slot}")
                print("-" * 30)
                
                booking_data = {
                    'first_name': 'Time',
                    'last_name': 'Verify',
                    'email': 'timeverify@example.com',
                    'phone_number': '555-0123',
                    'reason': 'Time verification',
                    'service_type': 'General Checkup',
                    'pet_type': 'dog',
                    'appointment_date': selected_slot
                }
                
                # Create test image
                with open('test_image.jpg', 'wb') as f:
                    f.write(b'fake image data')
                
                with open('test_image.jpg', 'rb') as image_file:
                    files = {'image': ('test_image.jpg', image_file, 'image/jpeg')}
                    booking_response = requests.post(f"{BASE_URL}/book/", data=booking_data, files=files)
                
                if booking_response.status_code == 200:
                    result = booking_response.json()
                    print(f"✅ Booking successful!")
                    print(f"   Booking ID: {result['booking_id']}")
                    print(f"   Time booked: {selected_slot}")
                    
                    # Step 3: Check available times after booking
                    print(f"\n🔍 Step 3: Available Times After Booking")
                    print("-" * 30)
                    
                    response2 = requests.get(f"{BASE_URL}/available-slots/?selected_date={tomorrow}")
                    if response2.status_code == 200:
                        data2 = response2.json()
                        print(f"Available times for {tomorrow} (after booking):")
                        for slot in data2['available_slots']:
                            print(f"  {slot.split(' ')[1]}")
                        print(f"Total: {len(data2['available_slots'])} slots")
                        
                        # Check if the booked time is no longer available
                        if selected_slot not in data2['available_slots']:
                            print(f"\n✅ SUCCESS: Booked time {selected_slot.split(' ')[1]} is correctly removed!")
                            print("   This confirms the time was saved correctly in the database.")
                        else:
                            print(f"\n❌ ERROR: Booked time {selected_slot.split(' ')[1]} is still available!")
                            
                else:
                    print(f"❌ Booking failed: {booking_response.status_code}")
                    
            else:
                print("❌ No available slots to test with")
                
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        import os
        if os.path.exists('test_image.jpg'):
            os.remove('test_image.jpg')

if __name__ == "__main__":
    test_time_verification() 