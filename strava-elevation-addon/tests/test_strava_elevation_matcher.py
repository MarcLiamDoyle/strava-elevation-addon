#!/usr/bin/env python3
"""
Strava Elevation Matcher - Test Suite
This script tests the functionality of the Strava Elevation Matcher addon.
"""

import os
import sys
import unittest
import json
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the modules to test
from models.route import Route
from api.strava_client import StravaClient
from elevation.elevation_client import ElevationClient
from matching.elevation_matcher import ElevationMatcher
from strava_elevation_matcher import StravaElevationMatcher


class TestRoute(unittest.TestCase):
    """Test the Route model"""

    def setUp(self):
        """Set up test data"""
        self.route_data = {
            'id': '12345',
            'name': 'Test Route',
            'distance': 10000,  # 10km
            'elevation_gain': 250,
            'start_latlng': [37.7749, -122.4194],
            'end_latlng': [37.7749, -122.4194],
            'elevation_points': [100, 120, 150, 180, 200, 220, 200, 180, 150, 120, 100]
        }
        self.route = Route.from_dict(self.route_data)

    def test_route_creation(self):
        """Test route creation from dictionary"""
        self.assertEqual(self.route.id, '12345')
        self.assertEqual(self.route.name, 'Test Route')
        self.assertEqual(self.route.distance, 10000)
        self.assertEqual(self.route.elevation_gain, 250)
        self.assertEqual(len(self.route.elevation_points), 11)

    def test_route_to_dict(self):
        """Test route conversion to dictionary"""
        route_dict = self.route.to_dict()
        self.assertEqual(route_dict['id'], '12345')
        self.assertEqual(route_dict['name'], 'Test Route')
        self.assertEqual(route_dict['distance'], 10000)
        self.assertEqual(route_dict['elevation_gain'], 250)

    def test_route_elevation_stats(self):
        """Test route elevation statistics calculation"""
        stats = self.route.get_elevation_stats()
        self.assertEqual(stats['min'], 100)
        self.assertEqual(stats['max'], 220)
        self.assertEqual(stats['gain'], 250)
        self.assertAlmostEqual(stats['avg'], 156.36, places=2)

    def test_normalize_elevation_profile(self):
        """Test elevation profile normalization"""
        normalized = self.route.get_normalized_elevation_profile()
        self.assertEqual(len(normalized), len(self.route.elevation_points))
        self.assertEqual(normalized[0][0], 0.0)  # First point at 0% distance
        self.assertEqual(normalized[-1][0], 1.0)  # Last point at 100% distance
        self.assertEqual(normalized[0][1], 100)  # First elevation point
        self.assertEqual(normalized[-1][1], 100)  # Last elevation point


class TestStravaClient(unittest.TestCase):
    """Test the Strava API client"""

    @patch('api.strava_client.requests.post')
    def test_get_token(self, mock_post):
        """Test token acquisition"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_token',
            'refresh_token': 'test_refresh',
            'expires_at': 1616969045
        }
        mock_post.return_value = mock_response

        client = StravaClient('client_id', 'client_secret')
        token = client.get_token('auth_code')

        self.assertEqual(token, 'test_token')
        self.assertEqual(client.refresh_token, 'test_refresh')
        mock_post.assert_called_once()

    @patch('api.strava_client.requests.get')
    def test_get_activities(self, mock_get):
        """Test retrieving activities"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'id': 12345,
                'name': 'Morning Run',
                'distance': 8000,
                'total_elevation_gain': 150
            },
            {
                'id': 12346,
                'name': 'Evening Run',
                'distance': 5000,
                'total_elevation_gain': 100
            }
        ]
        mock_get.return_value = mock_response

        client = StravaClient('client_id', 'client_secret')
        client.access_token = 'test_token'
        activities = client.get_activities()

        self.assertEqual(len(activities), 2)
        self.assertEqual(activities[0].name, 'Morning Run')
        self.assertEqual(activities[1].distance, 5000)
        mock_get.assert_called_once()

    @patch('api.strava_client.requests.get')
    def test_get_activity_streams(self, mock_get):
        """Test retrieving activity streams"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'type': 'distance',
                'data': [0, 10, 20, 30, 40, 50]
            },
            {
                'type': 'altitude',
                'data': [100, 110, 120, 130, 120, 110]
            }
        ]
        mock_get.return_value = mock_response

        client = StravaClient('client_id', 'client_secret')
        client.access_token = 'test_token'
        streams = client.get_activity_streams(12345)

        self.assertEqual(len(streams), 2)
        self.assertEqual(streams[0]['type'], 'distance')
        self.assertEqual(streams[1]['type'], 'altitude')
        self.assertEqual(len(streams[1]['data']), 6)
        mock_get.assert_called_once()


class TestElevationClient(unittest.TestCase):
    """Test the Elevation API client"""

    @patch('elevation.elevation_client.requests.get')
    def test_get_elevation_open_meteo(self, mock_get):
        """Test retrieving elevation from Open-Meteo"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'elevation': [100, 120, 140]
        }
        mock_get.return_value = mock_response

        client = ElevationClient()
        elevations = client.get_elevation_open_meteo([
            [37.7749, -122.4194],
            [37.7750, -122.4195],
            [37.7751, -122.4196]
        ])

        self.assertEqual(len(elevations), 3)
        self.assertEqual(elevations[0], 100)
        self.assertEqual(elevations[2], 140)
        mock_get.assert_called_once()

    @patch('elevation.elevation_client.requests.get')
    def test_get_elevation_open_topo(self, mock_get):
        """Test retrieving elevation from Open Topo Data"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [
                {'elevation': 100},
                {'elevation': 120},
                {'elevation': 140}
            ]
        }
        mock_get.return_value = mock_response

        client = ElevationClient()
        elevations = client.get_elevation_open_topo([
            [37.7749, -122.4194],
            [37.7750, -122.4195],
            [37.7751, -122.4196]
        ])

        self.assertEqual(len(elevations), 3)
        self.assertEqual(elevations[0], 100)
        self.assertEqual(elevations[2], 140)
        mock_get.assert_called_once()


class TestElevationMatcher(unittest.TestCase):
    """Test the Elevation Matching algorithm"""

    def setUp(self):
        """Set up test data"""
        self.matcher = ElevationMatcher()
        
        # Create two similar elevation profiles
        self.profile1 = [
            [0.0, 100],
            [0.2, 120],
            [0.4, 150],
            [0.6, 180],
            [0.8, 150],
            [1.0, 100]
        ]
        
        # Similar profile with slight variations
        self.profile2 = [
            [0.0, 110],
            [0.2, 130],
            [0.4, 160],
            [0.6, 190],
            [0.8, 160],
            [1.0, 110]
        ]
        
        # Very different profile
        self.profile3 = [
            [0.0, 200],
            [0.2, 180],
            [0.4, 150],
            [0.6, 120],
            [0.8, 150],
            [1.0, 200]
        ]

    def test_dtw_similarity(self):
        """Test DTW similarity calculation"""
        # Similar profiles should have high similarity
        similarity1 = self.matcher.calculate_dtw_similarity(self.profile1, self.profile2)
        self.assertGreater(similarity1, 0.8)
        
        # Different profiles should have low similarity
        similarity2 = self.matcher.calculate_dtw_similarity(self.profile1, self.profile3)
        self.assertLess(similarity2, 0.5)
        
        # Same profile should have perfect similarity
        similarity3 = self.matcher.calculate_dtw_similarity(self.profile1, self.profile1)
        self.assertAlmostEqual(similarity3, 1.0, places=4)

    def test_find_similar_routes(self):
        """Test finding similar routes"""
        # Create test routes
        target_route = Route.from_dict({
            'id': '1',
            'name': 'Target Route',
            'distance': 10000,
            'elevation_gain': 200,
            'elevation_points': [100, 120, 150, 180, 150, 100]
        })
        
        # Similar route
        route1 = Route.from_dict({
            'id': '2',
            'name': 'Similar Route',
            'distance': 12000,
            'elevation_gain': 220,
            'elevation_points': [110, 130, 160, 190, 160, 110]
        })
        
        # Different route
        route2 = Route.from_dict({
            'id': '3',
            'name': 'Different Route',
            'distance': 8000,
            'elevation_gain': 250,
            'elevation_points': [200, 180, 150, 120, 150, 200]
        })
        
        routes = [route1, route2]
        
        # Find similar routes
        matches = self.matcher.find_similar_routes(target_route, routes)
        
        # Should return both routes, sorted by similarity
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0]['route'].id, '2')  # Similar route should be first
        self.assertEqual(matches[1]['route'].id, '3')
        self.assertGreater(matches[0]['similarity'], matches[1]['similarity'])


class TestStravaElevationMatcher(unittest.TestCase):
    """Test the main StravaElevationMatcher class"""

    @patch('strava_elevation_matcher.StravaClient')
    @patch('strava_elevation_matcher.ElevationClient')
    @patch('strava_elevation_matcher.ElevationMatcher')
    def setUp(self, mock_matcher, mock_elevation, mock_strava):
        """Set up test data with mocks"""
        self.mock_strava = mock_strava.return_value
        self.mock_elevation = mock_elevation.return_value
        self.mock_matcher = mock_matcher.return_value
        
        # Create the matcher with mocked dependencies
        self.matcher = StravaElevationMatcher('client_id', 'client_secret')

    def test_authenticate(self):
        """Test authentication"""
        self.mock_strava.get_token.return_value = 'test_token'
        
        result = self.matcher.authenticate('auth_code')
        
        self.assertTrue(result)
        self.mock_strava.get_token.assert_called_once_with('auth_code')

    def test_get_activities(self):
        """Test getting activities"""
        # Mock activities
        mock_activities = [
            Route.from_dict({'id': '1', 'name': 'Activity 1'}),
            Route.from_dict({'id': '2', 'name': 'Activity 2'})
        ]
        self.mock_strava.get_activities.return_value = mock_activities
        
        activities = self.matcher.get_activities()
        
        self.assertEqual(len(activities), 2)
        self.assertEqual(activities[0].name, 'Activity 1')
        self.mock_strava.get_activities.assert_called_once()

    def test_get_routes(self):
        """Test getting routes"""
        # Mock routes
        mock_routes = [
            Route.from_dict({'id': '1', 'name': 'Route 1'}),
            Route.from_dict({'id': '2', 'name': 'Route 2'})
        ]
        self.mock_strava.get_routes.return_value = mock_routes
        
        routes = self.matcher.get_routes()
        
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[0].name, 'Route 1')
        self.mock_strava.get_routes.assert_called_once()

    def test_find_similar_routes(self):
        """Test finding similar routes"""
        # Mock target route
        target_route = Route.from_dict({
            'id': '1',
            'name': 'Target Route',
            'distance': 10000,
            'elevation_gain': 200
        })
        
        # Mock local routes
        local_routes = [
            Route.from_dict({'id': '2', 'name': 'Local Route 1'}),
            Route.from_dict({'id': '3', 'name': 'Local Route 2'})
        ]
        
        # Mock matcher response
        mock_matches = [
            {'route': local_routes[0], 'similarity': 0.9},
            {'route': local_routes[1], 'similarity': 0.7}
        ]
        self.mock_matcher.find_similar_routes.return_value = mock_matches
        
        # Test with mocked data
        matches = self.matcher.find_similar_routes(target_route, local_routes)
        
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0]['route'].name, 'Local Route 1')
        self.assertEqual(matches[0]['similarity'], 0.9)
        self.mock_matcher.find_similar_routes.assert_called_once_with(
            target_route, local_routes, min_similarity=0.0
        )


if __name__ == '__main__':
    unittest.main()
