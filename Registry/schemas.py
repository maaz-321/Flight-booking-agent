FLIGHT_TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search_flights",
            "description": "Search available flights, timings, prices, and seat availability between an origin city and a destination city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Departure city name (e.g., Karachi, Lahore, Islamabad)"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Arrival city name (e.g., Lahore, Dubai, Karachi)"
                    }
                },
                "required": ["origin", "destination"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_flight",
            "description": "Book a flight ticket for a passenger once they confirm the flight number and provide their full name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "flight_no": {
                        "type": "string",
                        "description": "The exact flight number (e.g., PK-301, EK-601)"
                    },
                    "passenger_name": {
                        "type": "string",
                        "description": "Full name of the passenger"
                    }
                },
                "required": ["flight_no", "passenger_name"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_booking_details",
            "description": "Check existing flight booking details using the PNR confirmation code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pnr": {
                        "type": "string",
                        "description": "The PNR code (e.g., PNR-4521)"
                    }
                },
                "required": ["pnr"],
                "additionalProperties": False
            }
        }
    }
]