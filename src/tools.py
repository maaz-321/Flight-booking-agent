import random

# Simulated flight database (In a real app, this would be a SQL database or external airline API)
FLIGHTS_DB = [
    {"flight_no": "PK-301", "from": "karachi", "to": "lahore", "time": "10:00 AM", "price": 22000, "seats": 5},
    {"flight_no": "PA-402", "from": "karachi", "to": "lahore", "time": "04:30 PM", "price": 19500, "seats": 2},
    {"flight_no": "PK-701", "from": "karachi", "to": "dubai", "time": "08:00 PM", "price": 65000, "seats": 8},
    {"flight_no": "EK-601", "from": "karachi", "to": "dubai", "time": "11:45 PM", "price": 82000, "seats": 4},
    {"flight_no": "PK-308", "from": "islamabad", "to": "karachi", "time": "02:00 PM", "price": 24000, "seats": 0},
]

# Dictionary to store confirmed passenger tickets in memory using PNR as the key
BOOKINGS_DB = {}


def search_flights(origin: str, destination: str) -> str:
    """Search available flights between two cities."""
    # Filter flights that match both the origin and destination cities (case-insensitive)
    results = [
        f for f in FLIGHTS_DB
        if f["from"] == origin.lower().strip() and f["to"] == destination.lower().strip()
    ]
    
    # Return a clear message if no matching flights exist
    if not results:
        return f"No flights found from {origin} to {destination}."
    
    # Build a readable summary string of all matching flights for the LLM
    output = f"Available flights from {origin.title()} to {destination.title()}:\n"
    for f in results:
        status = f"{f['seats']} seats left" if f['seats'] > 0 else "SOLD OUT"
        output += f"- Flight {f['flight_no']} | Time: {f['time']} | Price: Rs. {f['price']} | Status: {status}\n"
    return output


def book_flight(flight_no: str, passenger_name: str) -> str:
    """Book a ticket on a specific flight for a passenger."""
    # Loop through the database to find the requested flight number
    for f in FLIGHTS_DB:
        if f["flight_no"].upper() == flight_no.upper().strip():
            # Check if any seats are still available
            if f["seats"] <= 0:
                return f"Booking Failed: Flight {flight_no} is completely sold out."
            
            # Reduce available seat count by 1
            f["seats"] -= 1
            # Generate a random 4-digit PNR confirmation code
            pnr = f"PNR-{random.randint(1000, 9999)}"
            
            # Save the passenger's booking details into BOOKINGS_DB
            BOOKINGS_DB[pnr] = {
                "pnr": pnr,
                "passenger": passenger_name,
                "flight_no": f["flight_no"],
                "route": f"{f['from'].title()} -> {f['to'].title()}",
                "time": f["time"],
                "price": f["price"]
            }
            
            # Return confirmation message so the LLM can share it with the user
            return (
                f"Booking Confirmed! PNR: {pnr} | Passenger: {passenger_name} | "
                f"Flight: {f['flight_no']} ({f['from'].title()} to {f['to'].title()}) at {f['time']}."
            )
            
    # Return an error message if the flight number was not found
    return f"Booking Failed: Flight number '{flight_no}' does not exist."


def get_booking_details(pnr: str) -> str:
    """Retrieve booked ticket details using PNR number."""
    # Look up the booking in BOOKINGS_DB (clean spaces and convert to uppercase)
    booking = BOOKINGS_DB.get(pnr.upper().strip())
    
    # Return an error message if the PNR does not exist
    if not booking:
        return f"No booking found with PNR '{pnr}'."
        
    # Return formatted ticket details
    return (
        f"Ticket Details -> PNR: {booking['pnr']} | Passenger: {booking['passenger']} | "
        f"Flight: {booking['flight_no']} | Route: {booking['route']} | Time: {booking['time']}"
    )


# Safe Tool Registry: Maps tool string names (from the LLM) to actual Python functions
TOOL_REGISTRY = {
    "search_flights": search_flights,
    "book_flight": book_flight,
    "get_booking_details": get_booking_details,
}