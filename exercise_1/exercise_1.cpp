#include <iostream>
#include <string>
#include <cmath>
#include <vector>
#include <fstream>
#include <sstream>
#include <cassert>

using namespace std;

#define PI 3.14159265
#define EPSILON 0.0001

const double radius = 6371.0;

struct Point {
    float lat;
    float longi;
};

// Haversine formula
float findDistance(float lat1, float long1, float lat2, float long2) {
    float lat1Rad = lat1 * PI / 180;
    float long1Rad = long1 * PI / 180;
    float lat2Rad = lat2 * PI / 180;
    float long2Rad = long2 * PI / 180;

    float dlat = lat2Rad - lat1Rad;
    float dlong = long2Rad - long1Rad;

    float a = pow(sin(dlat / 2), 2) + cos(lat1Rad) * cos(lat2Rad) * pow(sin(dlong / 2), 2);
    float c = 2 * atan2(sqrt(a), sqrt(1 - a));

    return radius * c;
}

float* closestPoints(float lat, float longi, float points[][2], int n) {
    float minDistance = findDistance(lat, longi, points[0][0], points[0][1]);
    float* closestPoint = points[0];

    for (int i = 1; i < n; i++) {
        float distance = findDistance(lat, longi, points[i][0], points[i][1]);
        if (distance < minDistance) {
            minDistance = distance;
            closestPoint = points[i];
        }
    }

    return closestPoint;
}

// Unit tests
void runTests() {
    cout << "\nRunning unit tests\n";

    float dist = findDistance(37.7749, -122.4194, 34.0522, -118.2437);
    if (abs(dist - 559.0) < 1.0) {  // 1.0 for tolerance
        cout << "Test passed: Distance between SF and LA is " << dist << " km\n";
    } else {
        cout << "Test failed: Distance between SF and LA should be ~559 km, got " << dist << " km\n";
    }


    float points[3][2] = {
        {37.7749, -122.4194},  // SF
        {34.0522, -118.2437},  // LA
        {40.7128, -74.0060}    // NYC
    };
    float* closest = closestPoints(37.0, -122.0, points, 3);
    if (abs(closest[0] - 37.7749) < EPSILON && abs(closest[1] - (-122.4194)) < EPSILON) { // For tolerance
        cout << "Test passed: Correctly found closest point (SF)\n";
    } else {
        cout << "Test failed: Did not find correct closest point\n";
    }
}

int main() {
    float points[5][2] = {
        {37.7749, -122.4194},
        {34.0522, -118.2437},
        {40.7128, -74.0060},
        {41.8781, -87.6298},
        {29.7604, -95.3698}
    };

    float lat, longi;
    cout << "Enter the latitude and longitude of the point: ";
    cin >> lat >> longi;

    float* closestPoint = closestPoints(lat, longi, points, 5);
    cout << "Closest point: (" << closestPoint[0] << ", " << closestPoint[1] << ")" << endl;

    return 0;
}
