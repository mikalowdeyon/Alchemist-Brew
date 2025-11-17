import requests
import json

# Test menu API
base_url = 'http://127.0.0.1:8000'

# Start Django server first (assuming it's running)
print("Testing menu API endpoints...")

# Test GET menu API
print("\n=== Testing GET /menu/api/ ===")
response = requests.get(f'{base_url}/menu/api/')
print(f"GET /menu/api/ - Status: {response.status_code}")
if response.status_code == 200:
    try:
        data = response.json()
        print(f"Items found: {len(data.get('items', []))}")
        for item in data.get('items', []):
            print(f"- {item['name']}: {item['category']} - Available: {item['available']}")
    except Exception as e:
        print(f"JSON decode error: {e}")
        print(f"Response text: {response.text[:500]}...")
else:
    print(f"Error: {response.text}")

# Test POST menu API (create new item) - need to login first
print("\n=== Testing POST /menu/api/ (Create) ===")
# First, login to get session
session = requests.Session()
login_data = {
    'username': 'admin',  # Assuming admin user exists
    'password': 'admin123'
}
login_response = session.post(f'{base_url}/login/', data=login_data)
print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    # Now try to create an item
    new_item = {
        'name': 'Test Item',
        'category': 'Coffees and Pastries',
        'price': 100.00,
        'available': True,
        'is_best_seller': False
    }
    create_response = session.post(f'{base_url}/menu/api/', json=new_item)
    print(f"POST /menu/api/ - Status: {create_response.status_code}")
    if create_response.status_code == 200:
        try:
            result = create_response.json()
            print(f"Created item: {result}")
        except Exception as e:
            print(f"JSON decode error: {e}")
            print(f"Response text: {create_response.text}")
    else:
        print(f"Error creating item: {create_response.text}")
else:
    print("Login failed, cannot test POST")

print("\nMenu API test completed.")
