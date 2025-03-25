import requests
import json

BASE_URL = "http://localhost:8000"  # Adjust if your API runs on a different port

# Helper function to print responses nicely
def print_response(response):
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

# 1. Create a user
print("Creating a user...")
user_data = {
    "name": "John Doe",
    "email": "john.doe@example.com"
}
response = requests.post(f"{BASE_URL}/users/", json=user_data)
print_response(response)
user_id = response.json()["id"]

# 2. Get the user
print(f"Getting user with ID: {user_id}")
response = requests.get(f"{BASE_URL}/users/{user_id}")
print_response(response)

# 3. Update the user
print(f"Updating user with ID: {user_id}")
updated_user_data = {
    "name": "John Updated",
    "email": "john.updated@example.com"
}
response = requests.put(f"{BASE_URL}/users/{user_id}", json=updated_user_data)
print_response(response)

# 4. Create a house for the user
print(f"Creating a house for user with ID: {user_id}")
house_data = {
    "name": "Beach House",
    "address": "123 Ocean Drive"
}
response = requests.post(f"{BASE_URL}/users/{user_id}/houses/", json=house_data)
print_response(response)
house_id = response.json()["id"]

# 5. Get the house
print(f"Getting house with ID: {house_id}")
response = requests.get(f"{BASE_URL}/houses/{house_id}")
print_response(response)

# 6. Create a room in the house
print(f"Creating a room in house with ID: {house_id}")
room_data = {
    "name": "Master Bedroom",
    "type": "BEDROOM"
}
response = requests.post(f"{BASE_URL}/houses/{house_id}/rooms", json=room_data)
print_response(response)
room_id = response.json()["id"]

# 7. Get the room
print(f"Getting room with ID: {room_id}")
response = requests.get(f"{BASE_URL}/rooms/{room_id}")
print_response(response)

# 8. Create a device in the room
print(f"Creating a device in room with ID: {room_id}")
device_data = {
    "name": "Smart Light",
    "type": "LIGHT"
}
response = requests.post(f"{BASE_URL}/rooms/{room_id}/devices", json=device_data)
print_response(response)
device_id = response.json()["id"]

# 9. Get the device
print(f"Getting device with ID: {device_id}")
response = requests.get(f"{BASE_URL}/devices/{device_id}")
print_response(response)

# 10. Update the device
print(f"Updating device with ID: {device_id}")
updated_device_data = {
    "name": "Updated Smart Light",
    "type": "LIGHT"
}
response = requests.put(f"{BASE_URL}/devices/{device_id}", json=updated_device_data)
print_response(response)

# 11. Delete operations (uncomment to test)
"""
# Delete device
print(f"Deleting device with ID: {device_id}")
response = requests.delete(f"{BASE_URL}/devices/{device_id}")
print_response(response)

# Delete room
print(f"Deleting room with ID: {room_id}")
response = requests.delete(f"{BASE_URL}/rooms/{room_id}")
print_response(response)

# Delete house
print(f"Deleting house with ID: {house_id}")
response = requests.delete(f"{BASE_URL}/houses/{house_id}")
print_response(response)

# Delete user
print(f"Deleting user with ID: {user_id}")
response = requests.delete(f"{BASE_URL}/users/{user_id}")
print_response(response)
"""

print("API testing completed!") 