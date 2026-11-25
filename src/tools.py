import random

# Simulated Flight Database (Real app mein yahan Amadeus/Sabre API ya SQL DB hogi)
FLIGHTS_DB = [
    {"flight_no": "PK-301", "from": "karachi", "to": "lahore", "time": "10:00 AM", "price": 22000, "seats": 5},
    {"flight_no": "PA-402", "from": "karachi", "to": "lahore", "time": "04:30 PM", "price": 19500, "seats": 2},
    {"flight_no": "PK-701", "from": "karachi", "to": "dubai", "time": "08:00 PM", "price": 65000, "seats": 8},
    {"flight_no": "EK-601", "from": "karachi", "to": "dubai", "time": "11:45 PM", "price": 82000, "seats": 4},
    {"flight_no": "PK-308", "from": "islamabad", "to": "karachi", "time": "02:00 PM", "price": 24000, "seats": 0},
]

# Booked tickets yahan save honge
BOOKINGS_DB = {}


def search_flights(origin: str, destination: str) -> str:
    """Search available flights between two cities."""
    results = [
        f for f in FLIGHTS_DB
        if f["from"] == origin.lower().strip() and f["to"] == destination.lower().strip()
    ]
    
    if not results:
        return f"No flights found from {origin} to {destination}."
    
    output = f"Available flights from {origin.title()} to {destination.title()}:\n"
    for f in results:
        status = f"{f['seats']} seats left" if f['seats'] > 0 else "SOLD OUT"
        output += f"- Flight {f['flight_no']} | Time: {f['time']} | Price: Rs. {f['price']} | Status: {status}\n"
    return output


def book_flight(flight_no: str, passenger_name: str) -> str:
    """Book a ticket on a specific flight for a passenger."""
    for f in FLIGHTS_DB:
        if f["flight_no"].upper() == flight_no.upper().strip():
            if f["seats"] <= 0:
                return f"Booking Failed: Flight {flight_no} is completely sold out."
            
            # Seat kam karein aur PNR generate karein
            f["seats"] -= 1
            pnr = f"PNR-{random.randint(1000, 9999)}"
            BOOKINGS_DB[pnr] = {
                "pnr": pnr,
                "passenger": passenger_name,
                "flight_no": f["flight_no"],
                "route": f"{f['from'].title()} -> {f['to'].title()}",
                "time": f["time"],
                "price": f["price"]
            }
            return (
                f"Booking Confirmed! PNR: {pnr} | Passenger: {passenger_name} | "
                f"Flight: {f['flight_no']} ({f['from'].title()} to {f['to'].title()}) at {f['time']}."
            )
            
    return f"Booking Failed: Flight number '{flight_no}' does not exist."


def get_booking_details(pnr: str) -> str:
    """Retrieve booked ticket details using PNR number."""
    booking = BOOKINGS_DB.get(pnr.upper().strip())
    if not booking:
        return f"No booking found with PNR '{pnr}'."
    return (
        f"Ticket Details -> PNR: {booking['pnr']} | Passenger: {booking['passenger']} | "
        f"Flight: {booking['flight_no']} | Route: {booking['route']} | Time: {booking['time']}"
    )


# Safe Tool Registry (Executor isi se functions call karega)
TOOL_REGISTRY = {
    "search_flights": search_flights,
    "book_flight": book_flight,
    "get_booking_details": get_booking_details,
}