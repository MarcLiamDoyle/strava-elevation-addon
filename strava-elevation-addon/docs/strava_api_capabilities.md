# Strava API Capabilities for Elevation Data

## Overview
The Strava API provides several endpoints and data structures that can be used to access elevation data for activities and routes. This document outlines the key capabilities relevant to our elevation matching add-on.

## Authentication
- Authentication is required via OAuth 2.0
- Access tokens expire every six hours
- Refresh tokens can be used to get new access tokens
- Default rate limit: 200 requests every 15 minutes, up to 2,000 requests per day

## Activity Endpoints
### Get Activity
- Endpoint: `/activities/{id}`
- Returns detailed activity information including:
  - `total_elevation_gain`: Total elevation gain in meters
  - `elev_high`: Highest elevation point in meters
  - `elev_low`: Lowest elevation point in meters

### Get Activity Streams
- Endpoint: `/activities/{id}/streams`
- Returns detailed stream data for an activity
- Requires `activity:read` scope
- Can request specific stream types including `altitude`
- Sample response includes altitude data points along the activity

## Route Endpoints
### Get Route
- Endpoint: `/routes/{id}`
- Returns route information

### Export Route GPX
- Endpoint: `/routes/{id}/export_gpx`
- Returns a GPX file of the route
- GPX files contain detailed elevation data

### Export Route TCX
- Endpoint: `/routes/{id}/export_tcx`
- Returns a TCX file of the route
- TCX files contain detailed elevation data

### Get Route Streams
- Endpoint: `/routes/{id}/streams`
- Returns detailed stream data for a route
- Includes `altitude` stream type
- Sample response includes altitude data points along the route

## Data Structures
### DetailedActivity
- Contains elevation-related fields:
  - `total_elevation_gain`
  - `elev_high`
  - `elev_low`

### StreamSet
- Contains various stream types including altitude
- Altitude stream provides elevation data points along an activity or route

## Conclusion
The Strava API provides comprehensive access to elevation data through multiple endpoints. For our elevation matching add-on, we can use:
1. Activity streams to get detailed altitude data for specific activities
2. Route streams to get detailed altitude data for routes
3. GPX/TCX exports for more detailed elevation profiles
4. Basic elevation statistics from activity details

These capabilities will allow us to extract elevation profiles from Strava activities and routes, which can then be matched against local elevation data to find similar training routes.
