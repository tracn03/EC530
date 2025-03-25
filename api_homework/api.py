from fastapi import FastAPI, HTTPException 
from typing import Optional, List
from .models import (
    RoomType, DeviceType, DeviceStatus,
    UserCreate, UserResponse,
    HouseCreate, HouseResponse,
    RoomCreate, RoomResponse,
    DeviceCreate, DeviceResponse,
    DeviceStatusUpdate,
    User, House, Room, Device,
    db
)
app = FastAPI()

'''
User CRUD
'''
@app.post("/users/", response_model = UserResponse)
def create_user(user_data: UserCreate):
    user = User.create(name = user_data.name, email = user_data.email)
    db.create_user(user)
    return user.to_response()

@app.get("/users/{user_id}", response_model = UserResponse)
def get_user(id: str) -> Optional[User]:
    user = db.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_response()

@app.put("/users/{user_id}", response_model = UserResponse)
def update_user(id: str, user_data: UserCreate):
    user = db.update_user(id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_response()


@app.delete("/users/{user_id}", response_model = UserResponse)
def remove_user(id: str):
    if not db.delete_user(id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

'''
House CRUD
'''
@app.post("/users/{user_id}/houses/", response_model = HouseResponse)
def create_house(user_id: str, house_data: HouseCreate):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    house = House.create(
        name = house_data.name,
        address = house_data.address, 
        owner_id = user.id)
    
    db.create_house(house)
    return house.to_response()

@app.get("/houses/{house_id}", response_model = HouseResponse)
def get_house(id: str) -> Optional[House]:
    house = db.get_house(id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    return house.to_response()
    
@app.put("/houses/{house_id}", response_model = HouseResponse)
def update_house(id: str, house_data: HouseCreate):
    house = db.update_house(id, house_data)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    return house.to_response()

@app.delete("/houses/{house_id}", response_model = HouseResponse)
def delete_house(id: str):
    if not db.delete_house(id):
        raise HTTPException(status_code=404, detail="House not found")
    return {"message": "House deleted successfully"}


'''
Room CRUD
'''
@app.post("/houses/{house_id}/rooms", response_model = RoomResponse)
def create_room(house_id: str, room_data: RoomCreate):
    house = db.get_house(house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    
    room = Room.create(
        name = room_data.name,
        type = room_data.type,
        house = house)
    
    db.create_room(room)
    return room.to_response()

@app.get("/rooms/{room_id}", response_model = RoomResponse) 
def get_room(room_id: str) -> Optional[Room]:
    room = db.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room.to_response()

@app.put("/rooms/{room_id}", response_model = RoomResponse)
def update_room(room_id: str, room_data: RoomCreate):
    room = db.update_room(room_id, {"name": room_data.name, "type": room_data.type})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room.to_response()


@app.delete("/rooms/{room_id}", response_model = RoomResponse)
def delete_room(room_id: str):
    if not db.delete_room(room_id):
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted successfully"}


'''
Device CRUD
'''
@app.post("/rooms/{room_id}/devices", response_model = DeviceResponse)  
def create_device(room_id: str, device_data: DeviceCreate):
    room = db.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    device = Device.create(
        name = device_data.name,
        type = device_data.type,
        room = room)
    
    db.create_device(device)
    return device.to_response()

@app.get("/devices/{device_id}", response_model = DeviceResponse)
def get_device(device_id: str) -> Optional[Device]:
    device = db.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device.to_response()

@app.put("/devices/{device_id}", response_model = DeviceResponse)
def update_device(device_id: str, device_data: DeviceCreate):
    device = db.update_device(device_id, {"name": device_data.name, "type": device_data.type})
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device.to_response()

@app.delete("/devices/{device_id}", response_model = DeviceResponse)
def delete_device(device_id: str):
    if not db.delete_device(device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}