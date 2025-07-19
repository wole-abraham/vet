#!/usr/bin/env python3
"""
Script to add test data to the database for testing the booking system.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def add_test_vets():
    """Add test vets to the database"""
    print("👨‍⚕️ Adding test vets to the database...")
    
    test_vets = [
        {"first_name": "Dr. Sarah", "last_name": "Johnson", "specialization": "General Checkup"},
        {"first_name": "Dr. Michael", "last_name": "Chen", "specialization": "Vaccination"},
        {"first_name": "Dr. Emily", "last_name": "Davis", "specialization": "Physiotherapy"},
        {"first_name": "Dr. James", "last_name": "Wilson", "specialization": "Dermatology"},
        {"first_name": "Dr. Lisa", "last_name": "Brown", "specialization": "Operation"},
        {"first_name": "Dr. Robert", "last_name": "Taylor", "specialization": "Dental Care"},
    ]
    
    for vet_data in test_vets:
        try:
            response = requests.post(f"{BASE_URL}/vet/", params=vet_data)
            
            if response.status_code == 200:
                print(f"✅ Added {vet_data['first_name']} {vet_data['last_name']} - {vet_data['specialization']}")
            else:
                print(f"❌ Failed to add {vet_data['first_name']} {vet_data['last_name']}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error adding {vet_data['first_name']} {vet_data['last_name']}: {e}")

def get_vets():
    """Get all vets from the database"""
    print("\n📋 Current vets in database:")
    
    try:
        response = requests.get(f"{BASE_URL}/vets")
        
        if response.status_code == 200:
            data = response.json()
            vets = data.get('vets', [])
            
            if vets:
                for i, specialization in enumerate(vets, 1):
                    print(f"   {i}. {specialization}")
            else:
                print("   No vets found in database")
                
        else:
            print(f"❌ Error getting vets: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🚀 Setting up test data for booking system")
    print("=" * 50)
    
    # Add test vets
    add_test_vets()
    
    # Show current vets
    get_vets()
    
    print("\n" + "=" * 50)
    print("✅ Test data setup complete!")
    print("\nNow you can:")
    print("1. Run test_booking_system.py to test the booking functionality")
    print("2. Open booking.html in your browser to test the frontend")
    print("3. Try booking appointments with different services")

if __name__ == "__main__":
    main() 