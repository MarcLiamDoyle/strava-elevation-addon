"""
Route model for storing route information and elevation data.
"""

class Route:
    """
    Represents a route with elevation data.
    Can be created from Strava API data or local sources.
    """
    
    def __init__(self, id=None, name=None, distance=None, elevation_gain=None, 
                 start_latlng=None, end_latlng=None, elevation_points=None, 
                 latlng_points=None, source="unknown"):
        """
        Initialize a route object.
        
        Args:
            id (str): Unique identifier for the route
            name (str): Name of the route
            distance (float): Distance in meters
            elevation_gain (float): Total elevation gain in meters
            start_latlng (tuple): Starting coordinates (lat, lng)
            end_latlng (tuple): Ending coordinates (lat, lng)
            elevation_points (list): List of elevation points along the route
            latlng_points (list): List of (lat, lng) points along the route
            source (str): Source of the route data (e.g., "strava", "local")
        """
        self.id = id
        self.name = name
        self.distance = distance
        self.elevation_gain = elevation_gain
        self.start_latlng = start_latlng
        self.end_latlng = end_latlng
        self.elevation_points = elevation_points or []
        self.latlng_points = latlng_points or []
        self.source = source
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Route object from a dictionary.
        
        Args:
            data (dict): Dictionary containing route data
            
        Returns:
            Route: A new Route object
        """
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            distance=data.get('distance'),
            elevation_gain=data.get('elevation_gain'),
            start_latlng=data.get('start_latlng'),
            end_latlng=data.get('end_latlng'),
            elevation_points=data.get('elevation_points'),
            latlng_points=data.get('latlng_points'),
            source=data.get('source', 'unknown')
        )
        
    @classmethod
    def from_strava_activity(cls, activity_data):
        """
        Create a Route object from Strava activity data.
        
        Args:
            activity_data (dict): Activity data from Strava API
            
        Returns:
            Route: A new Route object
        """
        # Extract basic information
        route_id = f"strava_activity_{activity_data.get('id')}"
        name = activity_data.get('name')
        distance = activity_data.get('distance')
        elevation_gain = activity_data.get('total_elevation_gain')
        
        # Extract start and end coordinates
        start_latlng = tuple(activity_data.get('start_latlng', [None, None]))
        end_latlng = tuple(activity_data.get('end_latlng', [None, None]))
        
        # Create the route object
        route = cls(
            id=route_id,
            name=name,
            distance=distance,
            elevation_gain=elevation_gain,
            start_latlng=start_latlng,
            end_latlng=end_latlng,
            source="strava"
        )
        
        return route
    
    @classmethod
    def from_strava_route(cls, route_data):
        """
        Create a Route object from Strava route data.
        
        Args:
            route_data (dict): Route data from Strava API
            
        Returns:
            Route: A new Route object
        """
        # Extract basic information
        route_id = f"strava_route_{route_data.get('id')}"
        name = route_data.get('name')
        distance = route_data.get('distance')
        elevation_gain = route_data.get('elevation_gain')
        
        # Extract start and end coordinates if available
        segments = route_data.get('segments', [])
        start_latlng = None
        end_latlng = None
        
        if segments and len(segments) > 0:
            first_segment = segments[0]
            last_segment = segments[-1]
            start_latlng = (first_segment.get('start_latitude'), first_segment.get('start_longitude'))
            end_latlng = (last_segment.get('end_latitude'), last_segment.get('end_longitude'))
        
        # Create the route object
        route = cls(
            id=route_id,
            name=name,
            distance=distance,
            elevation_gain=elevation_gain,
            start_latlng=start_latlng,
            end_latlng=end_latlng,
            source="strava"
        )
        
        return route
    
    def add_elevation_stream(self, elevation_stream):
        """
        Add elevation data from a Strava stream.
        
        Args:
            elevation_stream (list): List of elevation points
        """
        self.elevation_points = elevation_stream
    
    def add_latlng_stream(self, latlng_stream):
        """
        Add lat/lng data from a Strava stream.
        
        Args:
            latlng_stream (list): List of [lat, lng] points
        """
        self.latlng_points = latlng_stream
    
    def get_elevation_profile(self):
        """
        Get the elevation profile of the route.
        
        Returns:
            list: List of elevation points
        """
        return self.elevation_points
    
    def get_normalized_elevation_profile(self):
        """
        Get a normalized elevation profile (0-100% of distance).
        
        Returns:
            list: List of (distance_percent, elevation) tuples
        """
        if not self.elevation_points or not self.distance:
            return []
        
        # Create distance points based on even distribution
        num_points = len(self.elevation_points)
        distance_step = 1.0 / (num_points - 1) if num_points > 1 else 0
        
        # Create normalized profile
        normalized_profile = []
        for i, elevation in enumerate(self.elevation_points):
            distance_percent = i * distance_step
            normalized_profile.append((distance_percent, elevation))
        
        return normalized_profile
    
    def get_elevation_stats(self):
        """
        Calculate elevation statistics for the route.
        
        Returns:
            dict: Dictionary with elevation statistics
        """
        if not self.elevation_points:
            return {
                "gain": self.elevation_gain,
                "max": None,
                "min": None,
                "avg": None
            }
        
        return {
            "gain": self.elevation_gain,
            "max": max(self.elevation_points),
            "min": min(self.elevation_points),
            "avg": sum(self.elevation_points) / len(self.elevation_points)
        }
    
    def to_dict(self):
        """
        Convert the route to a dictionary.
        
        Returns:
            dict: Dictionary representation of the route
        """
        return {
            "id": self.id,
            "name": self.name,
            "distance": self.distance,
            "elevation_gain": self.elevation_gain,
            "start_latlng": self.start_latlng,
            "end_latlng": self.end_latlng,
            "source": self.source,
            "elevation_stats": self.get_elevation_stats()
        }
