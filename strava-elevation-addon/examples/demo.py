"""
Example script demonstrating how to use the Strava Elevation Matcher.
"""

import os
import sys
import json
import logging
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.strava_elevation_matcher import StravaElevationMatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Main function to demonstrate the Strava Elevation Matcher.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get Strava API credentials from environment variables
    strava_client_id = os.getenv('STRAVA_CLIENT_ID')
    strava_client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    strava_refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')
    
    if not all([strava_client_id, strava_client_secret, strava_refresh_token]):
        logger.error("Missing Strava API credentials. Please set environment variables.")
        return
    
    # Initialize the Strava Elevation Matcher
    matcher = StravaElevationMatcher(
        strava_client_id=strava_client_id,
        strava_client_secret=strava_client_secret,
        strava_refresh_token=strava_refresh_token,
        elevation_provider="open-meteo"
    )
    
    # Authenticate with Strava
    if not matcher.authenticate():
        logger.error("Failed to authenticate with Strava API")
        return
    
    # Get athlete profile
    athlete = matcher.get_athlete_profile()
    if athlete:
        logger.info(f"Authenticated as {athlete.get('firstname')} {athlete.get('lastname')}")
    
    # Get recent activities
    activities = matcher.get_activities(limit=10)
    if activities:
        logger.info(f"Found {len(activities)} recent activities")
        
        # Print activity names
        for i, activity in enumerate(activities):
            logger.info(f"{i+1}. {activity.get('name')} ({activity.get('id')})")
        
        # Select the first activity as target
        target_activity_id = activities[0].get('id')
        logger.info(f"Using activity '{activities[0].get('name')}' as target")
        
        # Find similar routes
        logger.info("Finding routes with similar elevation profiles...")
        matches = matcher.find_similar_routes(target_activity_id, is_activity=True, max_results=3)
        
        # Print matches
        if matches:
            logger.info(f"Found {len(matches)} matching routes:")
            for i, (route, similarity) in enumerate(matches):
                logger.info(f"{i+1}. {route.name} (Similarity: {similarity:.2f})")
                
                # Compare target with the first match
                if i == 0:
                    logger.info("Comparing target with best match...")
                    comparison = matcher.compare_routes(
                        target_activity_id, 
                        route.id.split('_')[-1],  # Extract ID from route.id
                        route1_is_activity=True,
                        route2_is_activity=(route.source == "strava" and "activity" in route.id)
                    )
                    
                    if comparison:
                        # Print comparison details
                        logger.info(f"Similarity score: {comparison.get('similarity_score'):.2f}")
                        logger.info(f"Elevation gain difference: {comparison.get('elevation_gain_diff'):.1f}m ({comparison.get('elevation_gain_diff_percent'):.1f}%)")
                        logger.info(f"Distance difference: {comparison.get('distance_diff')/1000:.1f}km ({comparison.get('distance_diff_percent'):.1f}%)")
        else:
            logger.info("No matching routes found")
    else:
        logger.error("Failed to get activities")

if __name__ == "__main__":
    main()
