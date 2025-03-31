# Elevation Data Sources Research

## Open Topo Data
- **Website**: https://www.opentopodata.org/
- **Type**: REST API for elevation data
- **Hosting Options**: 
  - Self-hosted (Docker container)
  - Free public API
- **Public API Limitations**:
  - Max 100 locations per request
  - Max 1 call per second
  - Max 1000 calls per day
- **Available Datasets**:
  - ASTER (30m resolution)
  - ETOPO1 (1.8km resolution)
  - EU-DEM (25m resolution for Europe)
  - Mapzen (various resolutions)
  - NED (10m resolution for US)
  - NZ DEM (8m resolution for New Zealand)
  - SRTM (30m resolution globally)
  - EMOD bathymetry (ocean depths)
  - GEBCO bathymetry (ocean depths)
  - BKG (Germany)
  - Swisstopo (Switzerland)
- **API Format**: Compatible with Google Maps Elevation API
- **Advantages**:
  - Multiple datasets with different resolutions
  - Self-hosting option for higher usage limits
  - Well-documented API
- **Disadvantages**:
  - Limited daily requests on public API

## Open-Meteo Elevation API
- **Website**: https://open-meteo.com/en/docs/elevation-api
- **Type**: REST API for elevation data
- **Hosting Options**:
  - Free public API
  - Self-hosted option
  - Commercial option
- **Data Source**: Copernicus DEM 2021 release GLO-90 with 90 meters resolution
- **API Limitations**:
  - Non-commercial use: Less than 10,000 daily API calls
  - Up to 100 coordinates can be requested at once
- **API Format**: Simple JSON response with elevation array
- **Advantages**:
  - Consistent global coverage
  - Simple API format
  - Higher daily request limit than Open Topo Data
- **Disadvantages**:
  - Single dataset only
  - Less flexibility in data sources

## Open-Elevation
- **Website**: https://github.com/Jorl17/open-elevation
- **Type**: Open-source elevation API
- **Hosting Options**:
  - Self-hosted
  - Free public API at open-elevation.com
- **Features**:
  - Free and open-source alternative to Google Elevation API
  - Docker image available
  - Scripts to acquire custom datasets
- **Advantages**:
  - Fully open-source
  - Easy to set up
  - Customizable datasets
- **Disadvantages**:
  - Less detailed documentation on limitations
  - Unclear current maintenance status

## Comparison for Strava Add-on Use Case
For our Strava elevation matching add-on, we need to consider:

1. **Coverage**: All three options provide global coverage, which is essential for matching elevation profiles from anywhere.

2. **Resolution**: 
   - Open Topo Data offers the most flexibility with multiple datasets of varying resolutions
   - Open-Meteo provides consistent 90m resolution globally
   - Open-Elevation depends on the datasets you configure

3. **Usage Limits**:
   - Open-Meteo has the highest free tier with up to 10,000 daily API calls
   - Open Topo Data is limited to 1,000 daily calls on the public API
   - Self-hosting any of these options removes these limitations

4. **Implementation Complexity**:
   - Open-Meteo has the simplest API
   - Open Topo Data has good documentation and Google-compatible API
   - Open-Elevation requires more setup but offers more customization

5. **Reliability**:
   - All three are community-maintained projects
   - Open-Meteo and Open Topo Data appear to have active maintenance

## Recommendation
For the Strava add-on, we should consider:

1. **Initial Development**: Use Open-Meteo's public API due to higher daily limits and simple integration
2. **Production Deployment**: 
   - For lower usage: Continue with Open-Meteo
   - For higher usage: Self-host Open Topo Data with SRTM dataset for global coverage
3. **Advanced Features**: Consider combining multiple data sources for varying resolution based on location
