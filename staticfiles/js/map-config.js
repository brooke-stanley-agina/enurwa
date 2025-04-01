// Google Maps API Key
const GOOGLE_MAPS_API_KEY = 'AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg'; // This is a test API key, replace with your actual key

// Map Configuration
const mapConfig = {
    center: { lat: -2.0, lng: 37.0 },
    zoom: 6,
    mapTypeId: "terrain",
    styles: [
        {
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [{"color": "#e9e9e9"},{"lightness": 17}]
        },
        {
            "featureType": "landscape",
            "elementType": "geometry",
            "stylers": [{"color": "#f5f5f5"},{"lightness": 20}]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry.stroke",
            "stylers": [{"color": "#ffffff"},{"lightness": 17},{"weight": 1.2}]
        },
        {
            "featureType": "road.arterial",
            "elementType": "geometry",
            "stylers": [{"color": "#ffffff"},{"lightness": 18}]
        },
        {
            "featureType": "road.local",
            "elementType": "geometry",
            "stylers": [{"color": "#ffffff"},{"lightness": 16}]
        },
        {
            "featureType": "poi",
            "elementType": "geometry",
            "stylers": [{"color": "#f5f5f5"},{"lightness": 21}]
        },
        {
            "featureType": "poi.park",
            "elementType": "geometry",
            "stylers": [{"color": "#dedede"},{"lightness": 21}]
        }
    ]
};

// Safari Locations
const locations = [
    {
        name: "Masai Mara",
        position: { lat: -1.4927, lng: 35.2094 },
        description: "Kenya's Premier Safari Destination",
        country: "Kenya"
    },
    {
        name: "Serengeti",
        position: { lat: -2.1540, lng: 34.6857 },
        description: "Tanzania's Endless Plains",
        country: "Tanzania"
    },
    {
        name: "Amboseli",
        position: { lat: -2.6531, lng: 37.2531 },
        description: "Land of Giants",
        country: "Kenya"
    }
]; 