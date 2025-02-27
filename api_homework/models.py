from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr

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

# Pydantic models for API requests/responses
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