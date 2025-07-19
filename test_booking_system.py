#!/usr/bin/env python3
"""
Test script to demonstrate the booking system with time slot restrictions.
This script will:
1. Check available slots for today
2. Book an appointment
3. Check available slots again to see the restriction in action
"""

import requests
import json
from datetime import datetime, timedelta
import time

BASE_URL = "http://127.0.0.1:8000/api"

def test_available_slots():
    """Test the available slots endpoint"""
    print("🔍 Testing Available Slots Endpoint...")
    
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    
    try:
        response = requests.get(f"{BASE_URL}/available-slots/?selected_date={today}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Available slots for {today}:")
            print(f"   - Total available: {len(data['available_slots'])}")
            print(f"   - Total booked: {len(data['booked_times'])}")
            print(f"   - Business hours: {data['business_hours']['start']} - {data['business_hours']['end']}")
            
            if data['available_slots']:
                print(f"   - First available slot: {data['available_slots'][0]}")
                print(f"   - Last available slot: {data['available_slots'][-1]}")
            
            return data
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the server is running on http://127.0.0.1:8000")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def test_booking_appointment():
    """Test booking an appointment"""
    print("\n📅 Testing Appointment Booking...")
    
    # Get available slots first
    slots_data = test_available_slots()
    if not slots_data or not slots_data['available_slots']:
        print("❌ No available slots to book")
        return None
    
    # Use the first available slot
    appointment_time = slots_data['available_slots'][0]
    
    # Prepare booking data
    booking_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'phone_number': '555-0123',
        'reason': 'Test appointment',
        'service_type': 'General Checkup',
        'pet_type': 'dog',
        'appointment_date': appointment_time
    }
    
    # Create a simple image file for testing
    with open('test_image.jpg', 'wb') as f:
        f.write(b'fake image data')
    
    try:
        with open('test_image.jpg', 'rb') as image_file:
            files = {'image': ('test_image.jpg', image_file, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/book/", data=booking_data, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Booking successful!")
            print(f"   - Booking ID: {result['booking_id']}")
            print(f"   - Veterinarian: {result['vet']}")
            print(f"   - Service: {result['service']}")
            print(f"   - Pet Type: {result['pet_type']}")
            return appointment_time
        else:
            print(f"❌ Booking failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Booking error: {e}")
        return None
    finally:
        # Clean up test file
        import os
        if os.path.exists('test_image.jpg'):
            os.remove('test_image.jpg')

def test_slot_restriction():
    """Test that booked slots are no longer available"""
    print("\n🔒 Testing Slot Restriction...")
    
    # Book an appointment first
    booked_time = test_booking_appointment()
    if not booked_time:
        print("❌ Could not book appointment for testing")
        return
    
    # Wait a moment for the database to update
    time.sleep(1)
    
    # Check available slots again
    today = datetime.now().strftime("%Y-%m-%d")
    
    try:
        response = requests.get(f"{BASE_URL}/available-slots/?selected_date={today}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if the booked time is no longer available
            if booked_time not in data['available_slots']:
                print("✅ Slot restriction working correctly!")
                print(f"   - Booked time {booked_time} is no longer available")
                print(f"   - Remaining available slots: {len(data['available_slots'])}")
            else:
                print("❌ Slot restriction not working - booked time still available")
                
        else:
            print(f"❌ Error checking slots: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all tests"""
    print("🚀 Testing Booking System with Time Slot Restrictions")
    print("=" * 60)
    
    # Test 1: Check available slots
    test_available_slots()
    
    # Test 2: Book an appointment
    test_booking_appointment()
    
    # Test 3: Verify slot restriction
    test_slot_restriction()
    
    print("\n" + "=" * 60)
    print("✅ Testing complete!")
    print("\nTo test the frontend:")
    print("1. Open booking.html in your browser")
    print("2. Select a date to see available time slots")
    print("3. Book an appointment and see the slot become unavailable")

if __name__ == "__main__":
    main() 