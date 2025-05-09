import numpy as np
from typing import List, Tuple, Union
import pandas as pd
from math import radians, sin, cos, sqrt, atan2, degrees

def convert_degrees_to_decimal(degrees: float, minutes: float = 0, seconds: float = 0, direction: str = 'N') -> float:
    """
    Convert degrees, minutes, seconds to decimal degrees.
    Direction can be 'N', 'S', 'E', 'W' for latitude/longitude.
    """
    decimal = degrees + minutes/60 + seconds/3600
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def convert_decimal_to_degrees(decimal: float) -> Tuple[float, float, float, str]:
    """
    Convert decimal degrees to degrees, minutes, seconds format.
    Returns (degrees, minutes, seconds, direction)
    """
    direction = 'N' if decimal >= 0 else 'S'
    decimal = abs(decimal)
    
    degrees = int(decimal)
    minutes_decimal = (decimal - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = (minutes_decimal - minutes) * 60
    
    return degrees, minutes, seconds, direction

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    radius = 6371 
    return radius * c

def find_closest_points(
    points1: Union[List[Tuple[float, float]], np.ndarray],
    points2: Union[List[Tuple[float, float]], np.ndarray],
    use_haversine: bool = False,
    input_format: str = 'decimal'  
) -> List[Tuple[int, int, float]]:
   
    if not points1 or not points2:
        return []

    points1 = np.array(points1)
    points2 = np.array(points2)
    
    if input_format == 'degrees':
        points1 = np.array([[convert_degrees_to_decimal(p[0], p[1], p[2], p[3]) 
                            for p in points1]])
        points2 = np.array([[convert_degrees_to_decimal(p[0], p[1], p[2], p[3]) 
                            for p in points2]])
    
    closest_pairs = []
    
    for i, p1 in enumerate(points1):
        min_dist = float('inf')
        closest_j = -1
        
        for j, p2 in enumerate(points2):
            if use_haversine:
                dist = haversine_distance(p1[0], p1[1], p2[0], p2[1])
            else:
                dist = np.sqrt(np.sum((p1 - p2) ** 2))
            
            if dist < min_dist:
                min_dist = dist
                closest_j = j
        
        closest_pairs.append((i, closest_j, min_dist))
    
    return closest_pairs

def read_points_from_csv(file_path: str, lat_col: str, lon_col: str, format: str = 'decimal') -> np.ndarray:

    df = pd.read_csv(file_path)
    if format == 'decimal':
        return df[[lat_col, lon_col]].values
    else:
        points = []
        for _, row in df.iterrows():
            lat = convert_degrees_to_decimal(
                row[f'{lat_col}_deg'],
                row[f'{lat_col}_min'],
                row[f'{lat_col}_sec'],
                row[f'{lat_col}_dir']
            )
            lon = convert_degrees_to_decimal(
                row[f'{lon_col}_deg'],
                row[f'{lon_col}_min'],
                row[f'{lon_col}_sec'],
                row[f'{lon_col}_dir']
            )
            points.append([lat, lon])
        return np.array(points)

def get_points_from_user(format: str = 'decimal') -> List[Tuple[float, float]]:
   
    points = []
    if format == 'decimal':
        print("Enter points (lat lon) in decimal degrees. Enter empty line to finish:")
        while True:
            line = input().strip()
            if not line:
                break
            try:
                x, y = map(float, line.split())
                points.append((x, y))
            except ValueError:
                print("Invalid input. Please enter two numbers separated by space.")
    else:
        print("Enter points in degrees, minutes, seconds format:")
        print("Format: lat_deg lat_min lat_sec lat_dir lon_deg lon_min lon_sec lon_dir")
        print("Example: 42 21 36 N 71 3 32 W")
        while True:
            line = input().strip()
            if not line:
                break
            try:
                values = line.split()
                if len(values) != 8:
                    raise ValueError
                lat = convert_degrees_to_decimal(
                    float(values[0]), float(values[1]), float(values[2]), values[3]
                )
                lon = convert_degrees_to_decimal(
                    float(values[4]), float(values[5]), float(values[6]), values[7]
                )
                points.append((lat, lon))
            except (ValueError, IndexError):
                print("Invalid input. Please use the format: deg min sec dir deg min sec dir")
    
    return points 