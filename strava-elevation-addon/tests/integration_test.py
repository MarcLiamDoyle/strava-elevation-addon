#!/usr/bin/env python3
"""
Strava Elevation Matcher - Integration Test
This script performs integration testing of the Strava Elevation Matcher addon.
"""

import os
import sys
import json
import time
import matplotlib.pyplot as plt
import numpy as np
from unittest.mock import patch

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the modules to test
from models.route import Route
from api.strava_client import StravaClient
from elevation.elevation_client import ElevationClient
from matching.elevation_matcher import ElevationMatcher
from strava_elevation_matcher import StravaElevationMatcher


def create_test_routes():
    """Create test routes with realistic elevation profiles"""
    
    # Create a hilly route (multiple hills)
    hilly_route = Route.from_dict({
        'id': 'test_hilly',
        'name': 'Hilly Test Route',
        'distance': 15000,  # 15km
        'elevation_gain': 450,
        'start_latlng': [37.7749, -122.4194],
        'end_latlng': [37.7749, -122.4194],
        'elevation_points': generate_hilly_profile(100, 450, 100)
    })
    
    # Create a mountain route (one big climb)
    mountain_route = Route.from_dict({
        'id': 'test_mountain',
        'name': 'Mountain Test Route',
        'distance': 20000,  # 20km
        'elevation_gain': 800,
        'start_latlng': [37.7749, -122.4194],
        'end_latlng': [37.7749, -122.4194],
        'elevation_points': generate_mountain_profile(100, 900, 100)
    })
    
    # Create a flat route
    flat_route = Route.from_dict({
        'id': 'test_flat',
        'name': 'Flat Test Route',
        'distance': 10000,  # 10km
        'elevation_gain': 50,
        'start_latlng': [37.7749, -122.4194],
        'end_latlng': [37.7749, -122.4194],
        'elevation_points': generate_flat_profile(100, 150, 100)
    })
    
    # Create a rolling route (gentle ups and downs)
    rolling_route = Route.from_dict({
        'id': 'test_rolling',
        'name': 'Rolling Test Route',
        'distance': 12000,  # 12km
        'elevation_gain': 200,
        'start_latlng': [37.7749, -122.4194],
        'end_latlng': [37.7749, -122.4194],
        'elevation_points': generate_rolling_profile(100, 200, 100)
    })
    
    # Create a similar hilly route with slight variations
    similar_hilly_route = Route.from_dict({
        'id': 'test_similar_hilly',
        'name': 'Similar Hilly Test Route',
        'distance': 16000,  # 16km
        'elevation_gain': 480,
        'start_latlng': [37.8, -122.5],
        'end_latlng': [37.8, -122.5],
        'elevation_points': generate_hilly_profile(120, 480, 100, noise=0.2)
    })
    
    # Create a similar mountain route with slight variations
    similar_mountain_route = Route.from_dict({
        'id': 'test_similar_mountain',
        'name': 'Similar Mountain Test Route',
        'distance': 18000,  # 18km
        'elevation_gain': 750,
        'start_latlng': [37.8, -122.5],
        'end_latlng': [37.8, -122.5],
        'elevation_points': generate_mountain_profile(120, 850, 100, noise=0.2)
    })
    
    return {
        'hilly': hilly_route,
        'mountain': mountain_route,
        'flat': flat_route,
        'rolling': rolling_route,
        'similar_hilly': similar_hilly_route,
        'similar_mountain': similar_mountain_route
    }


def generate_hilly_profile(base_elevation, max_elevation, num_points, noise=0.0):
    """Generate a hilly elevation profile with multiple hills"""
    profile = []
    
    # Create multiple hills
    num_hills = 4
    for i in range(num_points):
        # Position in the route (0 to 1)
        pos = i / (num_points - 1)
        
        # Base elevation with multiple sine waves for hills
        elevation = base_elevation
        for hill in range(num_hills):
            hill_pos = (hill + 1) / num_hills
            hill_width = 0.15
            hill_height = (max_elevation - base_elevation) / num_hills
            
            # Calculate distance from hill center
            dist = abs(pos - hill_pos)
            
            # Add elevation based on distance from hill center
            if dist < hill_width:
                # Use cosine function for a smooth hill shape
                hill_factor = np.cos(dist / hill_width * np.pi) + 1  # Range 0 to 2
                elevation += hill_factor * hill_height / 2
        
        # Add random noise if specified
        if noise > 0:
            elevation += np.random.normal(0, noise * (max_elevation - base_elevation))
        
        profile.append(int(elevation))
    
    return profile


def generate_mountain_profile(base_elevation, max_elevation, num_points, noise=0.0):
    """Generate a mountain elevation profile with one big climb"""
    profile = []
    
    for i in range(num_points):
        # Position in the route (0 to 1)
        pos = i / (num_points - 1)
        
        # Base shape: gradual climb to middle, then descent
        if pos < 0.4:
            # First 40%: gradual climb
            factor = pos / 0.4
            elevation = base_elevation + factor * (max_elevation - base_elevation) * 0.8
        elif pos < 0.6:
            # Middle 20%: high plateau
            elevation = max_elevation
        else:
            # Last 40%: descent
            factor = (pos - 0.6) / 0.4
            elevation = max_elevation - factor * (max_elevation - base_elevation) * 0.8
        
        # Add random noise if specified
        if noise > 0:
            elevation += np.random.normal(0, noise * (max_elevation - base_elevation))
        
        profile.append(int(elevation))
    
    return profile


def generate_flat_profile(base_elevation, max_elevation, num_points, noise=0.0):
    """Generate a flat elevation profile with minimal changes"""
    profile = []
    
    for i in range(num_points):
        # Position in the route (0 to 1)
        pos = i / (num_points - 1)
        
        # Base elevation with very small variations
        elevation = base_elevation + (max_elevation - base_elevation) * 0.1 * np.sin(pos * np.pi * 4)
        
        # Add random noise if specified
        if noise > 0:
            elevation += np.random.normal(0, noise * (max_elevation - base_elevation) * 0.1)
        
        profile.append(int(elevation))
    
    return profile


def generate_rolling_profile(base_elevation, max_elevation, num_points, noise=0.0):
    """Generate a rolling elevation profile with gentle ups and downs"""
    profile = []
    
    for i in range(num_points):
        # Position in the route (0 to 1)
        pos = i / (num_points - 1)
        
        # Base elevation with sine waves for rolling hills
        elevation = base_elevation + (max_elevation - base_elevation) * 0.5 * (
            np.sin(pos * np.pi * 6) + 1  # Range 0 to 2, scaled to 0 to 1
        )
        
        # Add random noise if specified
        if noise > 0:
            elevation += np.random.normal(0, noise * (max_elevation - base_elevation))
        
        profile.append(int(elevation))
    
    return profile


def visualize_elevation_profiles(routes):
    """Visualize the elevation profiles of test routes"""
    plt.figure(figsize=(12, 8))
    
    for name, route in routes.items():
        # Get normalized elevation profile
        profile = route.get_normalized_elevation_profile()
        x = [p[0] for p in profile]
        y = [p[1] for p in profile]
        
        plt.plot(x, y, label=route.name)
    
    plt.title('Elevation Profiles of Test Routes')
    plt.xlabel('Distance (%)')
    plt.ylabel('Elevation (m)')
    plt.legend()
    plt.grid(True)
    
    # Save the figure
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'tests', 'output')
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'elevation_profiles.png'))
    plt.close()


def test_elevation_matching():
    """Test the elevation matching algorithm with various profiles"""
    print("Testing elevation matching algorithm...")
    
    # Create test routes
    routes = create_test_routes()
    
    # Visualize the elevation profiles
    visualize_elevation_profiles(routes)
    
    # Create the matcher
    matcher = ElevationMatcher()
    
    # Test cases to evaluate
    test_cases = [
        {
            'name': 'Hilly vs All',
            'target': routes['hilly'],
            'candidates': [routes[k] for k in ['mountain', 'flat', 'rolling', 'similar_hilly']]
        },
        {
            'name': 'Mountain vs All',
            'target': routes['mountain'],
            'candidates': [routes[k] for k in ['hilly', 'flat', 'rolling', 'similar_mountain']]
        },
        {
            'name': 'Flat vs All',
            'target': routes['flat'],
            'candidates': [routes[k] for k in ['hilly', 'mountain', 'rolling']]
        }
    ]
    
    # Run test cases
    results = {}
    for test_case in test_cases:
        print(f"\nRunning test case: {test_case['name']}")
        
        # Find similar routes
        matches = matcher.find_similar_routes(test_case['target'], test_case['candidates'])
        
        # Store results
        results[test_case['name']] = matches
        
        # Print results
        print(f"Target: {test_case['target'].name}")
        print("Matches (sorted by similarity):")
        for i, match in enumerate(matches):
            print(f"  {i+1}. {match['route'].name}: {match['similarity']:.4f}")
    
    # Visualize the best matches
    visualize_best_matches(results, routes)
    
    return results


def visualize_best_matches(results, routes):
    """Visualize the best matches for each test case"""
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'tests', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    for test_name, matches in results.items():
        if not matches:
            continue
        
        # Get target route name from test name
        target_type = test_name.split(' ')[0].lower()
        target_route = routes[target_type]
        
        # Get best match
        best_match = matches[0]['route']
        similarity = matches[0]['similarity']
        
        # Create visualization
        plt.figure(figsize=(12, 6))
        
        # Get normalized elevation profiles
        target_profile = target_route.get_normalized_elevation_profile()
        match_profile = best_match.get_normalized_elevation_profile()
        
        # Extract x and y values
        target_x = [p[0] for p in target_profile]
        target_y = [p[1] for p in target_profile]
        match_x = [p[0] for p in match_profile]
        match_y = [p[1] for p in match_profile]
        
        # Plot profiles
        plt.plot(target_x, target_y, 'b-', label=f'Target: {target_route.name}')
        plt.plot(match_x, match_y, 'r-', label=f'Best Match: {best_match.name}')
        
        plt.title(f'Elevation Profile Comparison - Similarity: {similarity:.4f}')
        plt.xlabel('Distance (%)')
        plt.ylabel('Elevation (m)')
        plt.legend()
        plt.grid(True)
        
        # Save the figure
        filename = f"{test_name.replace(' ', '_').lower()}_best_match.png"
        plt.savefig(os.path.join(output_dir, filename))
        plt.close()


def test_full_system():
    """Test the full system with mock Strava API"""
    print("\nTesting full system integration...")
    
    # Create test routes
    routes = create_test_routes()
    
    # Create a mock Strava client
    class MockStravaClient:
        def __init__(self, client_id, client_secret):
            self.client_id = client_id
            self.client_secret = client_secret
            self.access_token = None
            self.refresh_token = None
        
        def get_token(self, auth_code):
            self.access_token = "mock_token"
            self.refresh_token = "mock_refresh"
            return self.access_token
        
        def get_activities(self, limit=30):
            return [routes['hilly'], routes['flat']]
        
        def get_routes(self, limit=30):
            return [routes['mountain'], routes['rolling']]
        
        def get_activity_streams(self, activity_id):
            # Return mock streams based on activity_id
            if activity_id == routes['hilly'].id:
                return [{'type': 'altitude', 'data': routes['hilly'].elevation_points}]
            return [{'type': 'altitude', 'data': [100] * 10}]
    
    # Patch the StravaClient with our mock
    with patch('strava_elevation_matcher.StravaClient', MockStravaClient):
        # Create the matcher
        matcher = StravaElevationMatcher('mock_id', 'mock_secret')
        
        # Test authentication
        auth_result = matcher.authenticate('mock_code')
        print(f"Authentication result: {auth_result}")
        
        # Test getting activities
        activities = matcher.get_activities()
        print(f"Retrieved {len(activities)} activities")
        for activity in activities:
            print(f"  - {activity.name}")
        
        # Test getting routes
        strava_routes = matcher.get_routes()
        print(f"Retrieved {len(strava_routes)} routes")
        for route in strava_routes:
            print(f"  - {route.name}")
        
        # Test finding similar routes
        target = routes['similar_mountain']
        local_routes = activities + strava_routes
        
        print(f"\nFinding routes similar to: {target.name}")
        matches = matcher.find_similar_routes(target, local_routes)
        
        print("Matches (sorted by similarity):")
        for i, match in enumerate(matches):
            print(f"  {i+1}. {match['route'].name}: {match['similarity']:.4f}")
        
        # Visualize the best match
        if matches:
            plt.figure(figsize=(12, 6))
            
            # Get normalized elevation profiles
            target_profile = target.get_normalized_elevation_profile()
            match_profile = matches[0]['route'].get_normalized_elevation_profile()
            
            # Extract x and y values
            target_x = [p[0] for p in target_profile]
            target_y = [p[1] for p in target_profile]
            match_x = [p[0] for p in match_profile]
            match_y = [p[1] for p in match_profile]
            
            # Plot profiles
            plt.plot(target_x, target_y, 'b-', label=f'Target: {target.name}')
            plt.plot(match_x, match_y, 'r-', label=f'Best Match: {matches[0]["route"].name}')
            
            plt.title(f'Full System Test - Similarity: {matches[0]["similarity"]:.4f}')
            plt.xlabel('Distance (%)')
            plt.ylabel('Elevation (m)')
            plt.legend()
            plt.grid(True)
            
            # Save the figure
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'tests', 'output')
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(os.path.join(output_dir, 'full_system_test.png'))
            plt.close()


if __name__ == '__main__':
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'tests', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Run the tests
    print("Starting integration tests for Strava Elevation Matcher")
    print("=" * 60)
    
    # Test elevation matching
    matching_results = test_elevation_matching()
    
    # Test full system
    test_full_system()
    
    print("\nTests completed. Results saved to:", output_dir)
