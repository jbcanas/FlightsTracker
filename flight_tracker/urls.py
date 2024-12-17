from django.urls import path
from .views import index, flight_search_results

app_name = 'flight_tracker'

urlpatterns = [
    path('', index, name='index'),
    path('flights/search/', flight_search_results, name='flights_search'),
]
