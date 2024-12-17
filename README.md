# FlightsTracker

## Features

- Real-time flight tracking by airport code
- Flight statistics grouped by country


## Installation

1. Clone the repository:
```bash
git clone this-repo.git FlightsTracker
cd FlightsTracker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add your FlightAPI.io API key:
```
FLIGHT_API_KEY=your_api_key_here
```


## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Open your browser and navigate to `http://localhost:8000`

## Usage

1. Enter a valid 3-letter IATA airport code (e.g., LAX, JFK, SFO)
2. Click "Search Flights" or press Enter
3. View real-time flight statistics grouped by country of origin

## Testing

The project includes comprehensive unit tests for both the service layer and views. To run the tests:

```bash
python manage.py test flight_tracker.tests
```

## Project Structure

```
FlightsTracker/
├── core/                   # Django project settings
├── flight_tracker/         # Main application
│   ├── services/          # API service layer
│   ├── templates/         # HTML templates
│   │   └── partials/     # HTMX partial templates
│   ├── tests/            # Unit tests
│   ├── views.py          # View controllers
│   └── urls.py           # URL routing
├── static/                # Static files
└── requirements.txt       # Python dependencies
```

## Technologies Used

- **Backend**: Django
- **Frontend**: 
  - HTMX for dynamic content loading
  - Tailwind CSS for styling
- **API**: FlightAPI.io
