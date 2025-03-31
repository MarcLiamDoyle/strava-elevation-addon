/**
 * Strava Elevation Matcher - Main Application JavaScript
 */

// Global state
const state = {
    authenticated: false,
    user: null,
    activities: [],
    routes: [],
    targetRoute: null,
    matches: [],
    selectedMatch: null,
    charts: {}
};

// API endpoints
const API = {
    base: '/api',
    auth: '/api/auth',
    activities: '/api/activities',
    routes: '/api/routes',
    match: '/api/match',
    compare: '/api/compare'
};

// DOM Elements
const DOM = {
    // Auth elements
    authRequired: document.getElementById('auth-required'),
    appContainer: document.getElementById('app-container'),
    loginBtn: document.getElementById('login-btn'),
    connectStravaBtn: document.getElementById('connect-strava-btn'),
    userProfile: document.getElementById('user-profile'),
    profileImg: document.getElementById('profile-img'),
    userName: document.getElementById('user-name'),
    logoutBtn: document.getElementById('logout-btn'),
    
    // Target selection elements
    activitiesList: document.getElementById('activities-list'),
    routesList: document.getElementById('routes-list'),
    activitySearch: document.getElementById('activity-search'),
    routeSearch: document.getElementById('route-search'),
    activitySort: document.getElementById('activity-sort'),
    routeSort: document.getElementById('route-sort'),
    
    // Target profile elements
    targetProfileSection: document.getElementById('target-profile-section'),
    targetName: document.getElementById('target-name'),
    targetDistance: document.getElementById('target-distance'),
    targetElevationGain: document.getElementById('target-elevation-gain'),
    targetMaxElevation: document.getElementById('target-max-elevation'),
    targetMinElevation: document.getElementById('target-min-elevation'),
    changeTargetBtn: document.getElementById('change-target-btn'),
    findMatchesBtn: document.getElementById('find-matches-btn'),
    
    // Matching results elements
    matchingResultsSection: document.getElementById('matching-results-section'),
    maxDistance: document.getElementById('max-distance'),
    minSimilarity: document.getElementById('min-similarity'),
    matchesContainer: document.getElementById('matches-container'),
    
    // Comparison elements
    comparisonSection: document.getElementById('comparison-section'),
    backToMatchesBtn: document.getElementById('back-to-matches-btn'),
    targetComparisonName: document.getElementById('target-comparison-name'),
    targetComparisonDistance: document.getElementById('target-comparison-distance'),
    targetComparisonElevation: document.getElementById('target-comparison-elevation'),
    targetComparisonMaxElevation: document.getElementById('target-comparison-max-elevation'),
    targetComparisonMinElevation: document.getElementById('target-comparison-min-elevation'),
    matchComparisonName: document.getElementById('match-comparison-name'),
    matchComparisonDistance: document.getElementById('match-comparison-distance'),
    matchComparisonElevation: document.getElementById('match-comparison-elevation'),
    matchComparisonMaxElevation: document.getElementById('match-comparison-max-elevation'),
    matchComparisonMinElevation: document.getElementById('match-comparison-min-elevation'),
    similarityScore: document.getElementById('similarity-score'),
    similarityScoreBar: document.getElementById('similarity-score-bar'),
    elevationMatch: document.getElementById('elevation-match'),
    elevationMatchBar: document.getElementById('elevation-match-bar')
};

// Chart configurations
const chartConfig = {
    elevation: {
        type: 'line',
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Distance (%)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Elevation (m)'
                    }
                }
            }
        }
    }
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    // Set up event listeners
    setupEventListeners();
    
    // Check authentication status
    checkAuthStatus();
});

// Set up event listeners
function setupEventListeners() {
    // Auth buttons
    DOM.loginBtn.addEventListener('click', handleLogin);
    DOM.connectStravaBtn.addEventListener('click', handleLogin);
    DOM.logoutBtn.addEventListener('click', handleLogout);
    
    // Target selection
    DOM.activitySearch.addEventListener('input', handleActivitySearch);
    DOM.routeSearch.addEventListener('input', handleRouteSearch);
    DOM.activitySort.addEventListener('change', handleActivitySort);
    DOM.routeSort.addEventListener('change', handleRouteSort);
    
    // Target profile
    DOM.changeTargetBtn.addEventListener('click', handleChangeTarget);
    DOM.findMatchesBtn.addEventListener('click', handleFindMatches);
    
    // Matching results
    DOM.maxDistance.addEventListener('change', handleFilterChange);
    DOM.minSimilarity.addEventListener('change', handleFilterChange);
    
    // Comparison
    DOM.backToMatchesBtn.addEventListener('click', handleBackToMatches);
}

// Authentication functions
function checkAuthStatus() {
    // Simulate API call to check auth status
    // In a real implementation, this would call the backend API
    simulateApiCall(API.auth + '/status')
        .then(response => {
            if (response.authenticated) {
                handleAuthSuccess(response.user);
            } else {
                showAuthRequired();
            }
        })
        .catch(error => {
            console.error('Auth check failed:', error);
            showAuthRequired();
        });
}

function handleLogin() {
    // Redirect to Strava OAuth
    // In a real implementation, this would redirect to the Strava OAuth flow
    // For demo purposes, we'll simulate a successful login
    simulateApiCall(API.auth + '/strava')
        .then(response => {
            handleAuthSuccess(response.user);
        })
        .catch(error => {
            console.error('Login failed:', error);
            showError('Failed to authenticate with Strava. Please try again.');
        });
}

function handleLogout() {
    // Clear auth state
    // In a real implementation, this would call the backend API to clear the session
    state.authenticated = false;
    state.user = null;
    showAuthRequired();
}

function handleAuthSuccess(user) {
    state.authenticated = true;
    state.user = user;
    
    // Update UI
    DOM.userName.textContent = user.firstname;
    DOM.profileImg.src = user.profile;
    DOM.userProfile.classList.remove('d-none');
    DOM.loginBtn.classList.add('d-none');
    DOM.authRequired.classList.add('d-none');
    DOM.appContainer.classList.remove('d-none');
    
    // Load initial data
    loadActivities();
    loadRoutes();
}

function showAuthRequired() {
    DOM.authRequired.classList.remove('d-none');
    DOM.appContainer.classList.add('d-none');
    DOM.userProfile.classList.add('d-none');
    DOM.loginBtn.classList.remove('d-none');
}

// Data loading functions
function loadActivities() {
    DOM.activitiesList.innerHTML = '<tr><td colspan="5" class="text-center">Loading activities...</td></tr>';
    
    // Simulate API call to get activities
    simulateApiCall(API.activities)
        .then(activities => {
            state.activities = activities;
            renderActivitiesList();
        })
        .catch(error => {
            console.error('Failed to load activities:', error);
            DOM.activitiesList.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Failed to load activities. Please try again.</td></tr>';
        });
}

function loadRoutes() {
    DOM.routesList.innerHTML = '<tr><td colspan="4" class="text-center">Loading routes...</td></tr>';
    
    // Simulate API call to get routes
    simulateApiCall(API.routes)
        .then(routes => {
            state.routes = routes;
            renderRoutesList();
        })
        .catch(error => {
            console.error('Failed to load routes:', error);
            DOM.routesList.innerHTML = '<tr><td colspan="4" class="text-center text-danger">Failed to load routes. Please try again.</td></tr>';
        });
}

// Rendering functions
function renderActivitiesList() {
    if (state.activities.length === 0) {
        DOM.activitiesList.innerHTML = '<tr><td colspan="5" class="text-center">No activities found</td></tr>';
        return;
    }
    
    let html = '';
    state.activities.forEach(activity => {
        html += `
            <tr>
                <td>${activity.name}</td>
                <td>${formatDate(activity.start_date)}</td>
                <td>${formatDistance(activity.distance)}</td>
                <td>${formatElevation(activity.total_elevation_gain)}</td>
                <td>
                    <button class="btn btn-sm btn-primary select-activity" data-id="${activity.id}">
                        Select
                    </button>
                </td>
            </tr>
        `;
    });
    
    DOM.activitiesList.innerHTML = html;
    
    // Add event listeners to select buttons
    document.querySelectorAll('.select-activity').forEach(button => {
        button.addEventListener('click', () => {
            const activityId = button.getAttribute('data-id');
            selectActivity(activityId);
        });
    });
}

function renderRoutesList() {
    if (state.routes.length === 0) {
        DOM.routesList.innerHTML = '<tr><td colspan="4" class="text-center">No routes found</td></tr>';
        return;
    }
    
    let html = '';
    state.routes.forEach(route => {
        html += `
            <tr>
                <td>${route.name}</td>
                <td>${formatDistance(route.distance)}</td>
                <td>${formatElevation(route.elevation_gain)}</td>
                <td>
                    <button class="btn btn-sm btn-primary select-route" data-id="${route.id}">
                        Select
                    </button>
                </td>
            </tr>
        `;
    });
    
    DOM.routesList.innerHTML = html;
    
    // Add event listeners to select buttons
    document.querySelectorAll('.select-route').forEach(button => {
        button.addEventListener('click', () => {
            const routeId = button.getAttribute('data-id');
            selectRoute(routeId);
        });
    });
}

function renderTargetProfile() {
    const target = state.targetRoute;
    
    // Update UI elements
    DOM.targetName.textContent = target.name;
    DOM.targetDistance.textContent = formatDistance(target.distance);
    DOM.targetElevationGain.textContent = formatElevation(target.elevation_gain);
    DOM.targetMaxElevation.textContent = formatElevation(target.elevation_stats.max);
    DOM.targetMinElevation.textContent = formatElevation(target.elevation_stats.min);
    
    // Show target profile section
    DOM.targetProfileSection.classList.remove('d-none');
    
    // Render elevation chart
    renderElevationChart('target-elevation-chart', target);
}

function renderElevationChart(canvasId, route) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart if it exists
    if (state.charts[canvasId]) {
        state.charts[canvasId].destroy();
    }
    
    // Prepare data
    const elevationProfile = route.normalized_elevation_profile || [];
    const labels = elevationProfile.map(point => `${Math.round(point[0] * 100)}%`);
    const data = elevationProfile.map(point => point[1]);
    
    // Create chart
    const chartData = {
        labels: labels,
        datasets: [{
            label: route.name,
            data: data,
            borderColor: '#0d6efd',
            backgroundColor: 'rgba(13, 110, 253, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4
        }]
    };
    
    state.charts[canvasId] = new Chart(ctx, {
        type: chartConfig.elevation.type,
        data: chartData,
        options: chartConfig.elevation.options
    });
}

function renderComparisonChart() {
    const target = state.targetRoute;
    const match = state.selectedMatch;
    
    if (!target || !match) return;
    
    const canvas = document.getElementById('comparison-chart');
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart if it exists
    if (state.charts['comparison-chart']) {
        state.charts['comparison-chart'].destroy();
    }
    
    // Prepare data
    const targetProfile = target.normalized_elevation_profile || [];
    const matchProfile = match.normalized_elevation_profile || [];
    
    const labels = targetProfile.map(point => `${Math.round(point[0] * 100)}%`);
    const targetData = targetProfile.map(point => point[1]);
    const matchData = matchProfile.map(point => point[1]);
    
    // Create chart
    const chartData = {
        labels: labels,
        datasets: [
            {
                label: target.name,
                data: targetData,
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            },
            {
                label: match.name,
                data: matchData,
                borderColor: '#198754',
                backgroundColor: 'rgba(25, 135, 84, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }
        ]
    };
    
    state.charts['comparison-chart'] = new Chart(ctx, {
        type: chartConfig.elevation.type,
        data: chartData,
        options: chartConfig.elevation.options
    });
}

function renderMatches() {
    if (state.matches.length === 0) {
        DOM.matchesContainer.innerHTML = '<div class="alert alert-info">No matching routes found. Try adjusting the filters.</div>';
        return;
    }
    
    let html = '';
    state.matches.forEach((match, index) => {
        const route = match.route;
        const similarity = match.similarity;
        
        html += `
            <div class="match-card">
                <div class="match-card-header">
                    <h5 class="match-card-title">${route.name}</h5>
                    <span class="badge bg-${getSimilarityBadgeColor(similarity)}">${Math.round(similarity * 100)}% Match</span>
                </div>
                <div class="match-card-body">
                    <div class="match-card-stats">
                        <div class="match-card-stat">
                            <div class="match-card-stat-label">Distance</div>
                            <div class="match-card-stat-value">${formatDistance(route.distance)}</div>
                        </div>
                        <div class="match-card-stat">
                            <div class="match-card-stat-label">Elevation Gain</div>
                            <div class="match-card-stat-value">${formatElevation(route.elevation_gain)}</div>
                        </div>
                        <div class="match-card-stat">
                            <div class="match-card-stat-label">Max Elevation</div>
                            <div class="match-card-stat-value">${formatElevation(route.elevation_stats.max)}</div>
                        </div>
                        <div class="match-card-stat">
                            <div class="match-card-stat-label">Min Elevation</div>
                            <div class="match-card-stat-value">${formatElevation(route.elevation_stats.min)}</div>
                        </div>
                    </div>
                    <canvas id="match-chart-${index}" class="match-card-chart"></canvas>
                </div>
                <div class="match-card-footer">
                    <div class="match-similarity">
                        <div class="match-similarity-label">Similarity:</div>
                        <div class="match-similarity-value">${Math.round(similarity * 100)}%</div>
                    </div>
                    <button class="btn btn-primary btn-sm view-comparison" data-index="${index}">
                        Compare
                    </button>
                </div>
            </div>
        `;
    });
    
    DOM.matchesContainer.innerHTML = html;
    
    // Render mini charts for each match
    state.matches.forEach((match, index) => {
        renderMatchMiniChart(`match-chart-${index}`, match.route);
    });
    
    // Add event listeners to comparison buttons
    document.querySelectorAll('.view-comparison').forEach(button => {
        button.addEventListener('click', () => {
            const index = parseInt(button.getAttribute('data-index'));
            selectMatch(index);
        });
    });
}

function renderMatchMiniChart(canvasId, route) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext('2d');
    
    // Prepare data
    const elevationProfile = route.normalized_elevation_profile || [];
    const labels = elevationProfile.map(point => `${Math.round(point[0] * 100)}%`);
    const data = elevationProfile.map(point => point[1]);
    
    // Create chart with simplified options for mini display
    const chartData = {
        labels: labels,
        datasets: [{
            data: data,
            borderColor: '#198754',
            backgroundColor: 'rgba(25, 135, 84, 0.1)',
            borderWidth: 1.5,
            fill: true,
            tension: 0.4
        }]
    };
    
    const miniChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                enabled: false
            }
        },
        scales: {
            x: {
                display: false
            },
            y: {
                display: false
            }
        },
        elements: {
            point: {
                radius: 0
            }
        }
    };
    
    state.charts[canvasId] = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: miniChartOptions
    });
}

// Event handlers
function handleActivitySearch() {
    const searchTerm = DOM.activitySearch.value.toLowerCase();
    
    if (searchTerm === '') {
        renderActivitiesList();
        return;
    }
    
    const filteredActivities = state.activities.filter(activity => 
        activity.name.toLowerCase().includes(searchTerm)
    );
    
    if (filteredActivities.length === 0) {
        DOM.activitiesList.innerHTML = '<tr><td colspan="5" class="text-center">No matching activities found</td></tr>';
        return;
    }
    
    let html = '';
    filteredActivities.forEach(activity => {
        html += `
            <tr>
                <td>${activity.name}</td>
                <td>${formatDate(activity.start_date)}</td>
                <td>${formatDistance(activity.distance)}</td>
                <td>${formatElevation(activity.total_elevation_gain)}</td>
                <td>
                    <button class="btn btn-sm btn-primary select-activity" data-id="${activity.id}">
                        Select
                    </button>
                </td>
            </tr>
        `;
    });
    
    DOM.activitiesList.innerHTML = html;
    
    // Add event listeners to select buttons
    document.querySelectorAll('.select-activity').forEach(button => {
        button.addEventListener('click', () => {
            const activityId = button.getAttribute('data-id');
            selectActivity(activityId);
        });
    });
}

function handleRouteSearch() {
    const searchTerm = DOM.routeSearch.value.toLowerCase();
    
    if (searchTerm === '') {
        renderRoutesList();
        return;
    }
    
    const filteredRoutes = state.routes.filter(route => 
        route.name.toLowerCase().includes(searchTerm)
    );
    
    if (filteredRoutes.length === 0) {
        DOM.routesList.innerHTML = '<tr><td colspan="4" class="text-center">No matching routes found</td></tr>';
        return;
    }
    
    let html = '';
    filteredRoutes.forEach(route => {
        html += `
            <tr>
                <td>${route.name}</td>
                <td>${formatDistance(route.distance)}</td>
                <td>${formatElevation(route.elevation_gain)}</td>
                <td>
                    <button class="btn btn-sm btn-primary select-route" data-id="${route.id}">
                        Select
                    </button>
                </td>
            </tr>
        `;
    });
    
    DOM.routesList.innerHTML = html;
    
    // Add event listeners to select buttons
    document.querySelectorAll('.select-route').forEach(button => {
        button.addEventListener('click', () => {
            const routeId = button.getAttribute('data-id');
            selectRoute(routeId);
        });
    });
}

function handleActivitySort() {
    const sortValue = DOM.activitySort.value;
    
    switch (sortValue) {
        case 'date-desc':
            state.activities.sort((a, b) => new Date(b.start_date) - new Date(a.start_date));
            break;
        case 'date-asc':
            state.activities.sort((a, b) => new Date(a.start_date) - new Date(b.start_date));
            break;
        case 'distance-desc':
            state.activities.sort((a, b) => b.distance - a.distance);
            break;
        case 'elevation-desc':
            state.activities.sort((a, b) => b.total_elevation_gain - a.total_elevation_gain);
            break;
    }
    
    renderActivitiesList();
}

function handleRouteSort() {
    const sortValue = DOM.routeSort.value;
    
    switch (sortValue) {
        case 'date-desc':
            state.routes.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            break;
        case 'date-asc':
            state.routes.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
            break;
        case 'distance-desc':
            state.routes.sort((a, b) => b.distance - a.distance);
            break;
        case 'elevation-desc':
            state.routes.sort((a, b) => b.elevation_gain - a.elevation_gain);
            break;
    }
    
    renderRoutesList();
}

function handleChangeTarget() {
    DOM.targetProfileSection.classList.add('d-none');
    DOM.matchingResultsSection.classList.add('d-none');
    DOM.comparisonSection.classList.add('d-none');
    state.targetRoute = null;
    state.matches = [];
    state.selectedMatch = null;
}

function handleFindMatches() {
    DOM.matchingResultsSection.classList.remove('d-none');
    DOM.matchesContainer.innerHTML = `
        <div class="loading-container">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Finding matches...</p>
        </div>
    `;
    
    // Get filter values
    const maxDistance = parseFloat(DOM.maxDistance.value);
    const minSimilarity = parseFloat(DOM.minSimilarity.value) / 100;
    
    // Simulate API call to find matches
    const params = {
        target_id: state.targetRoute.id,
        is_activity: state.targetRoute.type === 'activity',
        max_distance: maxDistance,
        min_similarity: minSimilarity
    };
    
    simulateApiCall(API.match, 'POST', params)
        .then(matches => {
            state.matches = matches;
            renderMatches();
        })
        .catch(error => {
            console.error('Failed to find matches:', error);
            DOM.matchesContainer.innerHTML = '<div class="alert alert-danger">Failed to find matches. Please try again.</div>';
        });
}

function handleFilterChange() {
    if (state.targetRoute) {
        handleFindMatches();
    }
}

function handleBackToMatches() {
    DOM.comparisonSection.classList.add('d-none');
    DOM.matchingResultsSection.classList.remove('d-none');
    state.selectedMatch = null;
}

// Selection functions
function selectActivity(activityId) {
    // Find the activity
    const activity = state.activities.find(a => a.id === activityId);
    
    if (!activity) {
        showError('Activity not found');
        return;
    }
    
    // Simulate API call to get activity details with elevation data
    simulateApiCall(`${API.activities}/${activityId}`)
        .then(activityDetails => {
            state.targetRoute = {
                ...activityDetails,
                type: 'activity'
            };
            renderTargetProfile();
            
            // Hide matching results if previously shown
            DOM.matchingResultsSection.classList.add('d-none');
            DOM.comparisonSection.classList.add('d-none');
        })
        .catch(error => {
            console.error('Failed to get activity details:', error);
            showError('Failed to load activity details. Please try again.');
        });
}

function selectRoute(routeId) {
    // Find the route
    const route = state.routes.find(r => r.id === routeId);
    
    if (!route) {
        showError('Route not found');
        return;
    }
    
    // Simulate API call to get route details with elevation data
    simulateApiCall(`${API.routes}/${routeId}`)
        .then(routeDetails => {
            state.targetRoute = {
                ...routeDetails,
                type: 'route'
            };
            renderTargetProfile();
            
            // Hide matching results if previously shown
            DOM.matchingResultsSection.classList.add('d-none');
            DOM.comparisonSection.classList.add('d-none');
        })
        .catch(error => {
            console.error('Failed to get route details:', error);
            showError('Failed to load route details. Please try again.');
        });
}

function selectMatch(index) {
    const match = state.matches[index];
    
    if (!match) {
        showError('Match not found');
        return;
    }
    
    state.selectedMatch = match.route;
    
    // Update comparison UI
    DOM.targetComparisonName.textContent = state.targetRoute.name;
    DOM.targetComparisonDistance.textContent = formatDistance(state.targetRoute.distance);
    DOM.targetComparisonElevation.textContent = formatElevation(state.targetRoute.elevation_gain);
    DOM.targetComparisonMaxElevation.textContent = formatElevation(state.targetRoute.elevation_stats.max);
    DOM.targetComparisonMinElevation.textContent = formatElevation(state.targetRoute.elevation_stats.min);
    
    DOM.matchComparisonName.textContent = match.route.name;
    DOM.matchComparisonDistance.textContent = formatDistance(match.route.distance);
    DOM.matchComparisonElevation.textContent = formatElevation(match.route.elevation_gain);
    DOM.matchComparisonMaxElevation.textContent = formatElevation(match.route.elevation_stats.max);
    DOM.matchComparisonMinElevation.textContent = formatElevation(match.route.elevation_stats.min);
    
    // Update similarity scores
    const similarityPercent = Math.round(match.similarity * 100);
    DOM.similarityScore.textContent = `${similarityPercent}%`;
    DOM.similarityScoreBar.style.width = `${similarityPercent}%`;
    DOM.similarityScoreBar.className = `progress-bar bg-${getSimilarityBadgeColor(match.similarity)}`;
    
    const elevationMatchPercent = Math.round(match.elevation_similarity * 100);
    DOM.elevationMatch.textContent = `${elevationMatchPercent}%`;
    DOM.elevationMatchBar.style.width = `${elevationMatchPercent}%`;
    DOM.elevationMatchBar.className = `progress-bar bg-${getSimilarityBadgeColor(match.elevation_similarity)}`;
    
    // Show comparison section
    DOM.matchingResultsSection.classList.add('d-none');
    DOM.comparisonSection.classList.remove('d-none');
    
    // Render comparison chart
    renderComparisonChart();
}

// Utility functions
function formatDistance(meters) {
    if (meters === undefined || meters === null) return '--';
    
    const km = meters / 1000;
    return km < 10 ? `${km.toFixed(1)} km` : `${Math.round(km)} km`;
}

function formatElevation(meters) {
    if (meters === undefined || meters === null) return '--';
    
    return `${Math.round(meters)} m`;
}

function formatDate(dateString) {
    if (!dateString) return '--';
    
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function getSimilarityBadgeColor(similarity) {
    const percent = similarity * 100;
    
    if (percent >= 90) return 'success';
    if (percent >= 75) return 'primary';
    if (percent >= 60) return 'info';
    if (percent >= 40) return 'warning';
    return 'danger';
}

function showError(message) {
    // In a real implementation, this would show a toast or alert
    alert(message);
}

// Mock API functions for demo purposes
// In a real implementation, these would be replaced with actual API calls
function simulateApiCall(endpoint, method = 'GET', data = null) {
    console.log(`Simulating ${method} request to ${endpoint}`, data);
    
    return new Promise((resolve, reject) => {
        // Add a small delay to simulate network latency
        setTimeout(() => {
            try {
                const response = getMockResponse(endpoint, method, data);
                resolve(response);
            } catch (error) {
                reject(error);
            }
        }, 500);
    });
}

function getMockResponse(endpoint, method, data) {
    // Auth endpoints
    if (endpoint.includes('/auth/status')) {
        return {
            authenticated: state.authenticated,
            user: state.user || null
        };
    }
    
    if (endpoint.includes('/auth/strava')) {
        // Simulate successful Strava auth
        return {
            user: {
                id: '12345',
                firstname: 'John',
                lastname: 'Doe',
                profile: 'https://via.placeholder.com/30'
            }
        };
    }
    
    // Activities endpoints
    if (endpoint === API.activities) {
        // Return mock activities list
        return getMockActivities();
    }
    
    if (endpoint.match(/\/activities\/\d+/)) {
        // Return mock activity details
        const activityId = endpoint.split('/').pop();
        return getMockActivityDetails(activityId);
    }
    
    // Routes endpoints
    if (endpoint === API.routes) {
        // Return mock routes list
        return getMockRoutes();
    }
    
    if (endpoint.match(/\/routes\/\d+/)) {
        // Return mock route details
        const routeId = endpoint.split('/').pop();
        return getMockRouteDetails(routeId);
    }
    
    // Match endpoint
    if (endpoint === API.match && method === 'POST') {
        // Return mock matches
        return getMockMatches(data);
    }
    
    // Compare endpoint
    if (endpoint.includes('/compare') && method === 'GET') {
        // Return mock comparison
        return getMockComparison();
    }
    
    // Default fallback
    throw new Error(`No mock response defined for ${method} ${endpoint}`);
}

// Mock data generators
function getMockActivities() {
    return [
        {
            id: '1001',
            name: 'Morning Run',
            type: 'Run',
            distance: 8500,
            total_elevation_gain: 120,
            start_date: '2025-03-20T08:30:00Z'
        },
        {
            id: '1002',
            name: 'Hill Repeats',
            type: 'Run',
            distance: 12300,
            total_elevation_gain: 350,
            start_date: '2025-03-18T17:15:00Z'
        },
        {
            id: '1003',
            name: 'Long Weekend Run',
            type: 'Run',
            distance: 21500,
            total_elevation_gain: 280,
            start_date: '2025-03-16T09:00:00Z'
        },
        {
            id: '1004',
            name: 'Trail Run',
            type: 'Run',
            distance: 15200,
            total_elevation_gain: 420,
            start_date: '2025-03-14T16:30:00Z'
        },
        {
            id: '1005',
            name: 'Recovery Run',
            type: 'Run',
            distance: 5000,
            total_elevation_gain: 35,
            start_date: '2025-03-12T07:45:00Z'
        }
    ];
}

function getMockRoutes() {
    return [
        {
            id: '2001',
            name: 'City Loop',
            distance: 10000,
            elevation_gain: 150,
            created_at: '2025-02-15T10:30:00Z'
        },
        {
            id: '2002',
            name: 'Mountain Trail',
            distance: 18500,
            elevation_gain: 650,
            created_at: '2025-02-10T14:20:00Z'
        },
        {
            id: '2003',
            name: 'Riverside Path',
            distance: 7500,
            elevation_gain: 50,
            created_at: '2025-01-28T09:15:00Z'
        },
        {
            id: '2004',
            name: 'Half Marathon Route',
            distance: 21097,
            elevation_gain: 210,
            created_at: '2025-01-15T16:45:00Z'
        },
        {
            id: '2005',
            name: 'Hill Challenge',
            distance: 12800,
            elevation_gain: 520,
            created_at: '2024-12-20T11:30:00Z'
        }
    ];
}

function getMockActivityDetails(activityId) {
    // Generate mock elevation profile
    const elevationPoints = generateMockElevationProfile();
    const normalizedProfile = normalizeElevationProfile(elevationPoints);
    
    // Find basic activity info
    const activity = getMockActivities().find(a => a.id === activityId) || {
        id: activityId,
        name: 'Unknown Activity',
        type: 'Run',
        distance: 10000,
        total_elevation_gain: 200,
        start_date: '2025-03-01T10:00:00Z'
    };
    
    // Add detailed information
    return {
        ...activity,
        elevation_points: elevationPoints,
        normalized_elevation_profile: normalizedProfile,
        elevation_stats: {
            gain: activity.total_elevation_gain,
            max: Math.max(...elevationPoints),
            min: Math.min(...elevationPoints),
            avg: elevationPoints.reduce((sum, val) => sum + val, 0) / elevationPoints.length
        },
        start_latlng: [37.7749, -122.4194],
        end_latlng: [37.7749, -122.4194]
    };
}

function getMockRouteDetails(routeId) {
    // Generate mock elevation profile
    const elevationPoints = generateMockElevationProfile();
    const normalizedProfile = normalizeElevationProfile(elevationPoints);
    
    // Find basic route info
    const route = getMockRoutes().find(r => r.id === routeId) || {
        id: routeId,
        name: 'Unknown Route',
        distance: 10000,
        elevation_gain: 200,
        created_at: '2025-01-01T10:00:00Z'
    };
    
    // Add detailed information
    return {
        ...route,
        elevation_points: elevationPoints,
        normalized_elevation_profile: normalizedProfile,
        elevation_stats: {
            gain: route.elevation_gain,
            max: Math.max(...elevationPoints),
            min: Math.min(...elevationPoints),
            avg: elevationPoints.reduce((sum, val) => sum + val, 0) / elevationPoints.length
        },
        start_latlng: [37.7749, -122.4194],
        end_latlng: [37.7749, -122.4194]
    };
}

function getMockMatches(data) {
    // Generate 3 mock matches with varying similarity
    return [
        {
            route: getMockRouteDetails('2002'),
            similarity: 0.92,
            elevation_similarity: 0.94,
            distance_similarity: 0.85
        },
        {
            route: getMockRouteDetails('2005'),
            similarity: 0.78,
            elevation_similarity: 0.82,
            distance_similarity: 0.70
        },
        {
            route: getMockActivityDetails('1004'),
            similarity: 0.65,
            elevation_similarity: 0.68,
            distance_similarity: 0.60
        }
    ];
}

function getMockComparison() {
    return {
        similarity_score: 0.85,
        elevation_gain_diff: 50,
        elevation_gain_diff_percent: 10,
        distance_diff: 1500,
        distance_diff_percent: 8,
        route1_stats: {
            gain: 350,
            max: 450,
            min: 100,
            avg: 250
        },
        route2_stats: {
            gain: 400,
            max: 500,
            min: 120,
            avg: 280
        }
    };
}

function generateMockElevationProfile() {
    // Generate a random elevation profile with 100 points
    const numPoints = 100;
    const baseElevation = 100 + Math.random() * 200;
    const maxVariation = 100 + Math.random() * 300;
    
    const elevationPoints = [];
    
    for (let i = 0; i < numPoints; i++) {
        // Create a somewhat realistic profile with hills
        const progress = i / numPoints;
        const hillFactor = Math.sin(progress * Math.PI * (2 + Math.random() * 3));
        const randomFactor = Math.random() * 0.3;
        
        const elevation = baseElevation + hillFactor * maxVariation * (0.7 + randomFactor);
        elevationPoints.push(Math.round(elevation));
    }
    
    return elevationPoints;
}

function normalizeElevationProfile(elevationPoints) {
    // Convert elevation points to normalized format (distance percentage, elevation)
    const numPoints = elevationPoints.length;
    
    return elevationPoints.map((elevation, index) => {
        const distancePercent = index / (numPoints - 1);
        return [distancePercent, elevation];
    });
}
