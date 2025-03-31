"""
Main application module that integrates all components.
"""

import logging
import os
from api.strava_client import StravaClient
from elevation.elevation_client import ElevationClient
from matching.elevation_matcher import ElevationMatcher
from models.route import Route

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StravaElevationMatcher:
    """
    Main application class that integrates Strava API, elevation data,
    and matching algorithm to find routes with similar elevation profiles.
    """
    
    def __init__(self, strava_client_id=None, strava_client_secret=None, 
                 strava_refresh_token=None, elevation_provider="open-meteo"):
        """
        Initialize the Strava Elevation Matcher.
        
        Args:
            strava_client_id (str): Strava API client ID
            strava_client_secret (str): Strava API client secret
            strava_refresh_token (str): Strava OAuth refresh token
            elevation_provider (str): Elevation data provider
        """
        # Initialize Strava client
        self.strava_client = StravaClient(
            client_id=strava_client_id,
            client_secret=strava_client_secret,
            refresh_token=strava_refresh_token
        )
        
        # Initialize elevation client
        self.elevation_client = ElevationClient(
            primary_provider=elevation_provider
        )
        
        # Initialize elevation matcher
        self.elevation_matcher = ElevationMatcher()
        
        # Cache for routes
        self.route_cache = {}
    
    def authenticate(self, auth_code=None):
        """
        Authenticate with Strava using an authorization code or refresh token.
        
        Args:
            auth_code (str): Authorization code from OAuth flow
            
        Returns:
            bool: True if authenticated, False otherwise
        """
        if auth_code:
            # Get token using authorization code
            token = self.strava_client.get_token(auth_code)
            return token is not None
        else:
            # Use existing refresh token
            return self.strava_client.ensure_token_valid()
    
    def get_athlete_profile(self):
        """
        Get the authenticated athlete's profile.
        
        Returns:
            dict: Athlete profile data
        """
        return self.strava_client.get_athlete()
    
    def get_activities(self, limit=30):
        """
        Get the athlete's recent activities.
        
        Args:
            limit (int): Maximum number of activities to retrieve
            
        Returns:
            list: List of Route objects
        """
        return self.strava_client.get_activities(limit=limit)
    
    def get_routes(self, limit=30):
        """
        Get the athlete's routes.
        
        Args:
            limit (int): Maximum number of routes to retrieve
            
        Returns:
            list: List of Route objects
        """
        return self.strava_client.get_routes(limit=limit)
    
    def get_route_with_elevation(self, route_id, use_cache=True):
        """
        Get a route with elevation data.
        
        Args:
            route_id (int): Strava route ID
            use_cache (bool): Whether to use cached data if available
            
        Returns:
            Route: Route object with elevation data
        """
        # Check cache first
        if use_cache and route_id in self.route_cache:
            return self.route_cache[route_id]
        
        # Get route data from Strava
        route = self.strava_client.get_route(route_id)
        if not route:
            logger.error(f"Failed to get route {route_id}")
            return None
        
        # Get route streams for elevation data
        streams = self.strava_client.get_route_streams(route_id)
        if streams and 'altitude' in streams:
            route.add_elevation_stream(streams['altitude'])
        
        if streams and 'latlng' in streams:
            route.add_latlng_stream(streams['latlng'])
        
        # If no elevation data from streams, try to get from external API
        if not route.elevation_points and route.latlng_points:
            logger.info(f"Getting elevation data for route {route_id} from external API")
            elevations = self.elevation_client.get_elevations_for_route(route.latlng_points)
            if elevations:
                route.add_elevation_stream(elevations)
        
        # Cache the route
        self.route_cache[route_id] = route
        
        return route
    
    def get_activity_with_elevation(self, activity_id, use_cache=True):
        """
        Get an activity with elevation data.
        
        Args:
            activity_id (int): Strava activity ID
            use_cache (bool): Whether to use cached data if available
            
        Returns:
            Route: Route object with elevation data
        """
        # Check cache first
        cache_key = f"activity_{activity_id}"
        if use_cache and cache_key in self.route_cache:
            return self.route_cache[cache_key]
        
        # Get activity data from Strava
        route = self.strava_client.get_activity(activity_id)
        if not route:
            logger.error(f"Failed to get activity {activity_id}")
            return None
        
        # Get activity streams for elevation data
        streams = self.strava_client.get_activity_streams(
            activity_id, 
            stream_types=['altitude', 'distance', 'latlng']
        )
        
        if streams and 'altitude' in streams:
            route.add_elevation_stream(streams['altitude'])
        
        if streams and 'latlng' in streams:
            route.add_latlng_stream(streams['latlng'])
        
        # If no elevation data from streams, try to get from external API
        if not route.elevation_points and route.latlng_points:
            logger.info(f"Getting elevation data for activity {activity_id} from external API")
            elevations = self.elevation_client.get_elevations_for_route(route.latlng_points)
            if elevations:
                route.add_elevation_stream(elevations)
        
        # Cache the route
        self.route_cache[cache_key] = route
        
        return route
    
    def find_similar_routes(self, target_route, candidate_routes=None, min_similarity=0.0):
        """
        Find routes with similar elevation profiles to the target route.
        
        Args:
            target_route (Route): Target route object
            candidate_routes (list): List of Route objects to compare against
            min_similarity (float): Minimum similarity score (0.0 to 1.0)
            
        Returns:
            list: List of matches with similarity scores
        """
        if not target_route or not target_route.elevation_points:
            logger.error("Target route has no elevation data")
            return []
        
        # If no candidate routes provided, use all available routes
        if candidate_routes is None:
            candidate_routes = []
            
            # Add routes
            routes = self.get_routes(limit=50)
            if routes:
                for route in routes:
                    if route.id != target_route.id:  # Skip target
                        route_with_elevation = self.get_route_with_elevation(route.id)
                        if route_with_elevation and route_with_elevation.elevation_points:
                            candidate_routes.append(route_with_elevation)
            
            # Add activities
            activities = self.get_activities(limit=50)
            if activities:
                for activity in activities:
                    if activity.id != target_route.id:  # Skip target
                        activity_with_elevation = self.get_activity_with_elevation(activity.id)
                        if activity_with_elevation and activity_with_elevation.elevation_points:
                            candidate_routes.append(activity_with_elevation)
        
        # Find matches using the elevation matcher
        return self.elevation_matcher.find_similar_routes(
            target_route, 
            candidate_routes, 
            min_similarity=min_similarity
        )
    
    def compare_routes(self, route1, route2):
        """
        Compare two routes and return detailed comparison metrics.
        
        Args:
            route1 (Route): First route object
            route2 (Route): Second route object
            
        Returns:
            dict: Comparison metrics
        """
        if not route1 or not route2:
            logger.error("Invalid routes for comparison")
            return None
        
        if not route1.elevation_points or not route2.elevation_points:
            logger.error("Routes have no elevation data")
            return None
        
        # Compare routes
        comparison = self.elevation_matcher.compare_routes(route1, route2)
        
        # Add route names
        comparison['route1_name'] = route1.name
        comparison['route2_name'] = route2.name
        
        return comparison
