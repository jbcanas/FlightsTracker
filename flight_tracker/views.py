from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .services.flightapi_service import get_flights_by_airport

# Create your views here.

def index(request):
    """Render the index page."""
    return render(request, 'flight_tracker/index.html')

@require_http_methods(["POST"])
def flight_search_results(request):
    """Handle the HTMX request for flight search results."""
    airport_code = request.POST.get('airport_code', '').upper()
    
    # Validate airport code
    if not airport_code:
        return render(request, 'flight_tracker/partials/flight_results.html', {
            'error': 'Airport code is required',
            'airport_code': airport_code
        })
    
    if len(airport_code) != 3:
        return render(request, 'flight_tracker/partials/flight_results.html', {
            'error': 'Airport code must be exactly 3 letters',
            'airport_code': airport_code
        })
    
    try:
        flights, airport_name = get_flights_by_airport(airport_code)
        
        if not flights:
            return render(request, 'flight_tracker/partials/flight_results.html', {
                'flights': [],
                'airport_code': airport_code,
                'airport_name': airport_name
            })
        
        # Sort flights by count in descending order
        sorted_flights = sorted(flights.items(), key=lambda x: x[1], reverse=True)
        context = {
            'flights': sorted_flights,
            'airport_code': airport_code,
            'airport_name': airport_name
        }
    except Exception as e:
        context = {
            'error': str(e),
            'airport_code': airport_code
        }
    
    return render(request, 'flight_tracker/partials/flight_results.html', context)
