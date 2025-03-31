# Strava Elevation Matcher - Documentation

## Overview

The Strava Elevation Matcher is an add-on for Strava that helps athletes train for races by finding routes with similar elevation profiles in their local area. This tool analyzes the elevation patterns of target race courses and matches them with local training routes, making it easier to prepare for specific race conditions.

## Features

- **Strava Integration**: Seamlessly connects with your Strava account to access your activities and routes
- **Elevation Profile Matching**: Uses Dynamic Time Warping (DTW) algorithm to find routes with similar elevation patterns
- **Local Area Search**: Finds matching routes within a specified distance from your location
- **Visual Comparison**: Side-by-side visualization of elevation profiles for easy comparison
- **Similarity Scoring**: Ranks potential training routes by their similarity to the target race course
- **Customizable Search**: Filter results by distance, elevation gain, and other criteria

## System Architecture

The Strava Elevation Matcher consists of several components:

1. **Web Frontend**: User interface for interacting with the application
2. **Backend Server**: Handles API requests, authentication, and business logic
3. **Elevation Matching Engine**: Core algorithm for comparing elevation profiles
4. **Strava API Client**: Interfaces with Strava to retrieve user data
5. **Elevation Data Client**: Retrieves elevation data for routes

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Strava account with API access

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/strava-elevation-addon.git
   cd strava-elevation-addon
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your Strava API credentials:
   - Create a file named `.env` in the project root
   - Add your Strava API credentials:
     ```
     STRAVA_CLIENT_ID=your_client_id
     STRAVA_CLIENT_SECRET=your_client_secret
     ```

4. Start the application:
   ```
   python src/strava_elevation_matcher.py
   ```

## Usage

### Authentication

1. Open the application in your web browser
2. Click "Connect with Strava" to authorize the application
3. Follow the Strava authorization flow to grant access

### Finding Similar Routes

1. Select a target race or route:
   - Choose from your Strava activities
   - Upload a GPX file
   - Select a public Strava route

2. Set your search preferences:
   - Maximum distance from your location
   - Minimum/maximum route length
   - Elevation gain range

3. Click "Find Matching Routes" to search for similar elevation profiles

4. Review the results:
   - Routes are ranked by similarity score
   - Compare elevation profiles side-by-side
   - View detailed route information

### Interpreting Results

- **Similarity Score**: Higher scores indicate more similar elevation patterns
- **Elevation Similarity**: Specifically compares the elevation profiles
- **Distance Difference**: How closely the route length matches the target
- **Elevation Gain Difference**: Difference in total climbing

## API Reference

### Strava Client

The `StravaClient` class handles authentication and data retrieval from Strava.

```python
from api.strava_client import StravaClient

# Initialize client
client = StravaClient(client_id, client_secret)

# Authenticate
client.get_token(auth_code)

# Get activities
activities = client.get_activities(limit=30)

# Get activity details
activity = client.get_activity(activity_id)

# Get activity streams (includes elevation data)
streams = client.get_activity_streams(activity_id)
```

### Elevation Client

The `ElevationClient` class retrieves elevation data for routes.

```python
from elevation.elevation_client import ElevationClient

# Initialize client
client = ElevationClient()

# Get elevation for a single point
elevation = client.get_elevation(lat, lng)

# Get elevations for multiple points
elevations = client.get_elevations(points)

# Get elevations for a route
elevations = client.get_elevations_for_route(latlng_points)
```

### Elevation Matcher

The `ElevationMatcher` class implements the elevation profile matching algorithm.

```python
from matching.elevation_matcher import ElevationMatcher

# Initialize matcher
matcher = ElevationMatcher(max_distance_km=50)

# Find similar routes
matches = matcher.find_similar_routes(target_route, candidate_routes)

# Calculate similarity between two routes
similarity = matcher.calculate_dtw_similarity(profile1, profile2)

# Compare routes in detail
comparison = matcher.compare_routes(route1, route2)
```

## Algorithm Details

### Dynamic Time Warping (DTW)

The core of the elevation matching algorithm is Dynamic Time Warping (DTW), which allows comparing elevation profiles of different lengths and paces. DTW finds the optimal alignment between two sequences by warping the time axis.

Key aspects of our DTW implementation:

1. **Normalization**: Elevation profiles are normalized to account for different route lengths
2. **Distance Calculation**: The algorithm calculates the minimum distance between aligned points
3. **Similarity Score**: The DTW distance is converted to a similarity score (0-1, higher is better)
4. **Weighting**: The final score combines elevation similarity and distance similarity

### Matching Process

1. Filter candidate routes by proximity to the target route's start location
2. For each candidate route:
   - Extract and normalize elevation profiles
   - Calculate DTW similarity between profiles
   - Calculate distance similarity
   - Compute overall similarity score
3. Sort routes by similarity score
4. Return top matches

## Troubleshooting

### Common Issues

- **Authentication Errors**: Ensure your Strava API credentials are correct and you have authorized the application
- **No Routes Found**: Check your search radius and ensure you have activities in your Strava account
- **Elevation Data Missing**: The application may fall back to alternative elevation data sources if the primary source fails
- **Performance Issues**: Processing large numbers of routes may take time, especially for longer routes

### Logging

The application uses Python's logging module. To enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Development

### Project Structure

```
strava-elevation-addon/
├── docs/                 # Documentation
├── src/                  # Source code
│   ├── api/              # API clients
│   ├── elevation/        # Elevation data handling
│   ├── matching/         # Elevation matching algorithm
│   ├── models/           # Data models
│   ├── ui/               # User interface
│   └── strava_elevation_matcher.py  # Main application
├── tests/                # Test suite
├── examples/             # Example scripts
└── README.md             # Project overview
```

### Running Tests

```
python -m unittest discover tests
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Strava API for providing access to activity data
- Open-Meteo and Open Topo Data for elevation data
- The scientific community for research on Dynamic Time Warping algorithms
