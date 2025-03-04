from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr
import uuid

class RoomType(str, Enum):
    LIVING_ROOM = "LIVING_ROOM"
    BEDROOM = "BEDROOM"
    KITCHEN = "KITCHEN"
    BATHROOM = "BATHROOM"

class DeviceType(str, Enum):
    LIGHT = "LIGHT"
    THERMOSTAT = "THERMOSTAT"
    CAMERA = "CAMERA"
    LOCK = "LOCK"

class DeviceStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    MAINTENANCE = "MAINTENANCE"

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

class HouseCreate(BaseModel):
    name: str
    address: str

class HouseResponse(BaseModel):
    id: str
    name: str
    address: str
    owner_id: str

class RoomCreate(BaseModel):
    name: str
    type: RoomType

class RoomResponse(BaseModel):
    id: str
    name: str
    type: RoomType
    house_id: str

class DeviceCreate(BaseModel):
    name: str
    type: DeviceType

class DeviceResponse(BaseModel):
    id: str
    name: str
    type: DeviceType
    status: DeviceStatus
    room_id: str

class DeviceStatusUpdate(BaseModel):
    status: DeviceStatus

@dataclass
class User:
    id: str
    name: str
    email: str
    houses: List['House'] = field(default_factory=list)
    
    @classmethod
    def create(cls, name: str, email: str) -> 'User':
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            email=email
        )
    
    def to_response(self) -> UserResponse:
        return UserResponse(
            id=self.id,
            name=self.name,
            email=self.email
        )

@dataclass
class House:
    id: str
    name: str
    address: str
    owner_id: str
    rooms: List['Room'] = field(default_factory=list)
    
    @classmethod
    def create(cls, name: str, address: str, owner_id: str) -> 'House':
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            address=address,
            owner_id=owner_id
        )
    
    def to_response(self) -> HouseResponse:
        return HouseResponse(
            id=self.id,
            name=self.name,
            address=self.address,
            owner_id=self.owner_id
        )

@dataclass
class Room:
    id: str
    name: str
    type: RoomType
    house_id: str
    devices: List['Device'] = field(default_factory=list)
    
    @classmethod
    def create(cls, name: str, room_type: RoomType, house_id: str) -> 'Room':
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            type=room_type,
            house_id=house_id
        )
    
    def to_response(self) -> RoomResponse:
        return RoomResponse(
            id=self.id,
            name=self.name,
            type=self.type,
            house_id=self.house_id
        )

@dataclass
class Device:
    id: str
    name: str
    type: DeviceType
    status: DeviceStatus
    room_id: str
    
    @classmethod
    def create(cls, name: str, device_type: DeviceType, room_id: str) -> 'Device':
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            type=device_type,
            status=DeviceStatus.OFFLINE,
            room_id=room_id
        )
    
    def to_response(self) -> DeviceResponse:
        return DeviceResponse(
            id=self.id,
            name=self.name,
            type=self.type,
            status=self.status,
            room_id=self.room_id
        )

# In-memory database for stub implementation
class Database:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.houses: Dict[str, House] = {}
        self.rooms: Dict[str, Room] = {}
        self.devices: Dict[str, Device] = {}
    
    # User operations
    def create_user(self, user: User) -> User:
        self.users[user.id] = user
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)
    
    def update_user(self, user_id: str, data: Dict[str, Any]) -> Optional[User]:
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        return user
    
    def delete_user(self, user_id: str) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    # House operations
    def create_house(self, house: House) -> House:
        self.houses[house.id] = house
        return house
    
    def get_house(self, house_id: str) -> Optional[House]:
        return self.houses.get(house_id)
    
    def update_house(self, house_id: str, data: Dict[str, Any]) -> Optional[House]:
        if house_id not in self.houses:
            return None
        
        house = self.houses[house_id]
        for key, value in data.items():
            if hasattr(house, key):
                setattr(house, key, value)
        
        return house
    
    def delete_house(self, house_id: str) -> bool:
        if house_id in self.houses:
            del self.houses[house_id]
            return True
        return False
    
    # Room operations
    def create_room(self, room: Room) -> Room:
        self.rooms[room.id] = room
        return room
    
    def get_room(self, room_id: str) -> Optional[Room]:
        return self.rooms.get(room_id)
    
    def update_room(self, room_id: str, data: Dict[str, Any]) -> Optional[Room]:
        if room_id not in self.rooms:
            return None
        
        room = self.rooms[room_id]
        for key, value in data.items():
            if hasattr(room, key):
                setattr(room, key, value)
        
        return room
    
    def delete_room(self, room_id: str) -> bool:
        if room_id in self.rooms:
            del self.rooms[room_id]
            return True
        return False
    
    # Device operations
    def create_device(self, device: Device) -> Device:
        self.devices[device.id] = device
        return device
    
    def get_device(self, device_id: str) -> Optional[Device]:
        return self.devices.get(device_id)
    
    def update_device(self, device_id: str, data: Dict[str, Any]) -> Optional[Device]:
        if device_id not in self.devices:
            return None
        
        device = self.devices[device_id]
        for key, value in data.items():
            if hasattr(device, key):
                setattr(device, key, value)
        
        return device
    
    def delete_device(self, device_id: str) -> bool:
        if device_id in self.devices:
            del self.devices[device_id]
            return True
        return False

# Create global database instance
db = Database()