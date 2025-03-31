# Strava Elevation Matcher

A tool to help athletes train for races by finding routes with similar elevation profiles in their local area.

## Overview

The Strava Elevation Matcher is an add-on for Strava that analyzes the elevation patterns of target race courses and matches them with local training routes. This makes it easier to prepare for specific race conditions by training on routes with similar elevation characteristics.

## Features

- **Strava Integration**: Connect with your Strava account to access your activities and routes
- **Elevation Profile Matching**: Find routes with similar elevation patterns using Dynamic Time Warping algorithm
- **Local Area Search**: Discover matching routes within a specified distance from your location
- **Visual Comparison**: Compare elevation profiles side-by-side
- **Similarity Scoring**: Routes are ranked by their similarity to the target race course

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

## Quick Start

1. Connect your Strava account
2. Select a target race or route
3. Set your search preferences
4. Find matching routes in your local area
5. Compare elevation profiles and choose the best training route

## Documentation

For detailed documentation, see the [documentation.md](docs/documentation.md) file.

## Example Usage

```python
from src.strava_elevation_matcher import StravaElevationMatcher

# Initialize the matcher
matcher = StravaElevationMatcher(client_id, client_secret)

# Authenticate with Strava
matcher.authenticate(auth_code)

# Get a target route
target_route = matcher.get_route(route_id)

# Find similar routes in your local area
similar_routes = matcher.find_similar_routes(target_route)

# Display the results
for match in similar_routes:
    print(f"Route: {match['route'].name}")
    print(f"Similarity: {match['similarity']:.2f}")
    print(f"Elevation Similarity: {match['elevation_similarity']:.2f}")
    print()
```

## Project Structure

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Strava API for providing access to activity data
- Open-Meteo and Open Topo Data for elevation data
- The scientific community for research on Dynamic Time Warping algorithms
