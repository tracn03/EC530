from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

class RoomType(Enum):
    LIVING_ROOM = "LIVING_ROOM"
    BEDROOM = "BEDROOM"
    KITCHEN = "KITCHEN"
    BATHROOM = "BATHROOM"
    HALLWAY = "HALLWAY"
    LAUNDRY = "LAUNDRY"

class DeviceType(Enum):
    LIGHT = "LIGHT"
    THERMOSTAT = "THERMOSTAT"
    CAMERA = "CAMERA"

class DeviceStatus(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


@dataclass
class User:
    id: str
    name: str
    email: str
    houses: List['House'] = None

@dataclass
class House:
    id: str
    name: str
    address: str
    owner: User
    rooms: List['Room'] = None

@dataclass
class Room:
    id: str
    name: str
    type: RoomType
    house: House
    devices: List['Device'] = None

@dataclass
class Device:
    id: str
    name: str
    type: DeviceType
    status: DeviceStatus
    room: Room    