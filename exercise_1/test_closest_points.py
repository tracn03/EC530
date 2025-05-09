import unittest
import numpy as np
import pandas as pd
import os
from closest_points import (
    find_closest_points, 
    haversine_distance, 
    read_points_from_csv,
    convert_degrees_to_decimal,
    convert_decimal_to_degrees
)

class TestClosestPoints(unittest.TestCase):
    def test_euclidean_distance(self):
        points1 = [(0, 0), (1, 1), (2, 2)]
        points2 = [(1, 0), (2, 1), (3, 2)]
        
        result = find_closest_points(points1, points2)
        
        expected = [
            (0, 0, 1.0),  # (0,0) is closest to (1,0)
            (1, 1, 1.0),  # (1,1) is closest to (2,1)
            (2, 2, 1.0)   # (2,2) is closest to (3,2)
        ]
        
        for (i, j, dist), (exp_i, exp_j, exp_dist) in zip(result, expected):
            self.assertEqual(i, exp_i)
            self.assertEqual(j, exp_j)
            self.assertAlmostEqual(dist, exp_dist, places=5)

    def test_haversine_distance(self):
        points1 = [(42.3601, -71.0589)]  # Boston
        points2 = [(40.7128, -74.0060)]  # New York
        
        result = find_closest_points(points1, points2, use_haversine=True)
        
        self.assertAlmostEqual(result[0][2], 306, delta=10)

    def test_degrees_conversion(self):
        # Test converting from degrees to decimal
        decimal = convert_degrees_to_decimal(42, 21, 36, 'N')
        self.assertAlmostEqual(decimal, 42.36, places=2)
        
        decimal = convert_degrees_to_decimal(71, 3, 32, 'W')
        self.assertAlmostEqual(decimal, -71.059, places=3)
        
        # Test converting from decimal to degrees
        deg, min, sec, dir = convert_decimal_to_degrees(42.36)
        self.assertEqual(deg, 42)
        self.assertEqual(min, 21)
        self.assertAlmostEqual(sec, 36, places=0)
        self.assertEqual(dir, 'N')
        
        deg, min, sec, dir = convert_decimal_to_degrees(-71.059)
        self.assertEqual(deg, 71)
        self.assertEqual(min, 3)
        self.assertAlmostEqual(sec, 32, places=0)
        self.assertEqual(dir, 'S')

    def test_degrees_format(self):
        # Test with degrees, minutes, seconds format
        points1 = [(42, 21, 36, 'N', 71, 3, 32, 'W')]  # Boston in DMS
        points2 = [(40, 42, 46, 'N', 74, 0, 22, 'W')]  # New York in DMS
        
        result = find_closest_points(points1, points2, use_haversine=True, input_format='degrees')
        self.assertAlmostEqual(result[0][2], 306, delta=10)

    def test_empty_inputs(self):
        self.assertEqual(find_closest_points([], []), [])
        self.assertEqual(find_closest_points([(1, 1)], []), [])
        self.assertEqual(find_closest_points([], [(1, 1)]), [])

    def test_single_point(self):
        points1 = [(0, 0)]
        points2 = [(1, 1)]
        
        result = find_closest_points(points1, points2)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)
        self.assertAlmostEqual(result[0][2], np.sqrt(2), places=5)

    def test_csv_reading_decimal(self):
        data = {
            'latitude': [42.3601, 40.7128],
            'longitude': [-71.0589, -74.0060]
        }
        df = pd.DataFrame(data)
        test_file = 'test_coordinates.csv'
        df.to_csv(test_file, index=False)
        
        try:
            points = read_points_from_csv(test_file, 'latitude', 'longitude')
            self.assertEqual(len(points), 2)
            self.assertEqual(points.shape[1], 2)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_csv_reading_degrees(self):
        data = {
            'latitude_deg': [42, 40],
            'latitude_min': [21, 42],
            'latitude_sec': [36, 46],
            'latitude_dir': ['N', 'N'],
            'longitude_deg': [71, 74],
            'longitude_min': [3, 0],
            'longitude_sec': [32, 22],
            'longitude_dir': ['W', 'W']
        }
        df = pd.DataFrame(data)
        test_file = 'test_coordinates_degrees.csv'
        df.to_csv(test_file, index=False)
        
        try:
            points = read_points_from_csv(test_file, 'latitude', 'longitude', format='degrees')
            self.assertEqual(len(points), 2)
            self.assertEqual(points.shape[1], 2)
            # Verify the conversion is correct
            self.assertAlmostEqual(points[0][0], 42.36, places=2)  # Boston latitude
            self.assertAlmostEqual(points[0][1], -71.059, places=3)  # Boston longitude
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

if __name__ == '__main__':
    unittest.main() 