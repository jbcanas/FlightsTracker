from typing import Dict, Tuple

import requests
from django.conf import settings


def get_flights_by_airport(airport_code: str) -> Tuple[Dict[str, int], str]:
    """
    Get flights at the specified airport grouped by country.
    
    Args:
        airport_code (str): 3-letter IATA airport code
        
    Returns:
        Tuple[Dict[str, int], str]: A tuple containing:
            - Dictionary with country names as keys and number of flights as values
            - Airport name as a string
    """
    api_key = settings.FLIGHT_API_KEY
    if not api_key:
        raise ValueError("Flight API key not found in Django settings")

    flights = {}

    try:
        mode = 'arrivals'
        url = f'https://api.flightapi.io/compschedule/{api_key}'
        params = {
            'mode': mode,
            'iata': airport_code,
            'day': 1,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        arrivals_data = response.json()

        arrivals = arrivals_data[0]['airport']['pluginData']['schedule']['arrivals']['data']
        for flight in arrivals:
            origin = flight.get('flight', {}).get('airport', {}).get('origin', {})
            country = origin.get('position', {}).get('country', {}).get('name')
            if country:
                flights[country] = flights.get(country, 0) + 1

        airport_name = arrivals_data[0]['airport']['pluginData']['details']['name']

        return flights, airport_name

    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
