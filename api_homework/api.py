from typing import Optional, List
import uuid
from models import User, House, Room, Device, RoomType, DeviceType, DeviceStatus

"""
Use CRUD
"""
class userAPI:
    def create_user(self, name: str, email: str) -> User:
        return User(
            id: str(uuid.uuid4()),
            name: name
            email: email
            house: house[]
        )
    
    def get_user(self, id: str) -> Optional[User]:
        return None


    def update_user(self, user_id: str, data: dict) -> Optional[User]:
        return User(
            id=user_id,
            name=data.get('name', 'Updated User'),
            email=data.get('email', 'updated@email.com'),
            houses=[]
        )
    
    def remove_user():
        pass

class HouseAPI:
    def create_house(self, name: str, address: str, owner: User) -> House:
        return House(
            id=str(uuid.uuid4()),
            name=name,
            address=address,
            owner=owner,
            rooms=[]
        )

    def get_house(self, house_id: str) -> Optional[House]:
        return None

    def update_house(self, house_id: str, data: dict) -> Optional[House]:
        return House(
            id=house_id,
            name=data.get('name', 'Updated House'),
            address=data.get('address', 'Updated Address'),
            owner=data.get('owner'),
            rooms=[]
        )

    def delete_house(self, house_id: str) -> bool:
        return True

class RoomAPI:
    def create_room(self, name: str, room_type: RoomType, house: House) -> Room:
        return Room(
            id=str(uuid.uuid4()),
            name=name,
            type=room_type,
            house=house,
            devices=[]
        )

    def get_room(self, room_id: str) -> Optional[Room]:
        return None

    def update_room(self, room_id: str, data: dict) -> Optional[Room]:
        return Room(
            id=room_id,
            name=data.get('name', 'Updated Room'),
            type=data.get('type', RoomType.BEDROOM),
            house=data.get('house'),
            devices=[]
        )

    def delete_room(self, room_id: str) -> bool:
        return True

class DeviceAPI:
    def create_device(self, name: str, device_type: DeviceType, room: Room) -> Device:
        return Device(
            id=str(uuid.uuid4()),
            name=name,
            type=device_type,
            status=DeviceStatus.OFFLINE,
            room=room
        )

    def get_device(self, device_id: str) -> Optional[Device]:
        return None

    def update_device(self, device_id: str, data: dict) -> Optional[Device]:
        return Device(
            id=device_id,
            name=data.get('name', 'Updated Device'),
            type=data.get('type', DeviceType.LIGHT),
            status=data.get('status', DeviceStatus.ONLINE),
            room=data.get('room')
        )

    def delete_device(self, device_id: str) -> bool:
        return True

    def update_device_status(self, device_id: str, status: DeviceStatus) -> Optional[Device]:
        device = self.get_device(device_id)
        if device:
            device.status = status
            return device
        return None