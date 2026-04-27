from datetime import date
from typing import List, Dict, Any
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import json

# Import DB connection if we want to run queries (commented to keep as skeleton)
# from db.database import get_db_connection 

class SearchInput(BaseModel):
    location: str = Field(description="The city or specific area to search in (e.g., 'Coxs Bazar').")
    check_in: date = Field(description="The desired check-in date.")
    check_out: date = Field(description="The desired check-out date.")
    guests: int = Field(description="The total number of guests.")

@tool("search_available_properties", args_schema=SearchInput)
def search_available_properties(location: str, check_in: date, check_out: date, guests: int) -> str:
    """
    Searches the database for available properties based on user criteria.
    Returns a JSON string of a list of matching listings.
    """
    # Skeleton logic for DB query:
    # with get_db_connection() as conn:
    #     with conn.cursor() as cur:
    #         cur.execute("SELECT id, title, price_per_night FROM listings WHERE location ILIKE %s AND max_guests >= %s AND is_available = TRUE", (f"%{location}%", guests))
    #         results = cur.fetchall()
    
    # Mock return for skeleton
    mock_results = [
        {"id": 1, "title": "Seaside Villa", "price_per_night": 5000.0, "location": location},
        {"id": 2, "title": "Cozy Beach Hut", "price_per_night": 2500.0, "location": location}
    ]
    return json.dumps(mock_results)

class DetailsInput(BaseModel):
    listing_id: int = Field(description="The unique numeric ID of the property.")

@tool("get_listing_details", args_schema=DetailsInput)
def get_listing_details(listing_id: int) -> str:
    """
    Retrieves full details for a specific listing using its ID.
    Returns a JSON string of the property details.
    """
    # Skeleton DB query:
    # with get_db_connection() as conn:
    #     with conn.cursor() as cur:
    #         cur.execute("SELECT * FROM listings WHERE id = %s", (listing_id,))
    #         result = cur.fetchone()
    
    mock_result = {
        "id": listing_id,
        "title": "Seaside Villa",
        "location": "Cox's Bazar",
        "description": "A beautiful villa with a sea view.",
        "price_per_night": 5000.0,
        "max_guests": 4,
        "amenities": ["WiFi", "AC", "Pool"]
    }
    return json.dumps(mock_result)

class BookingInput(BaseModel):
    listing_id: int = Field(description="The unique numeric ID of the property to book.")
    guest_name: str = Field(description="The name of the guest making the booking.")
    check_in: date = Field(description="Check-in date.")
    check_out: date = Field(description="Check-out date.")
    guests: int = Field(description="Total number of guests.")

@tool("create_booking", args_schema=BookingInput)
def create_booking(listing_id: int, guest_name: str, check_in: date, check_out: date, guests: int) -> str:
    """
    Creates a new booking for a specific property.
    Returns a JSON string of the booking confirmation details.
    """
    # Calculate days for mock
    days = (check_out - check_in).days
    total_price = 5000.0 * max(1, days) # Mock calculation
    
    # Skeleton DB query:
    # with get_db_connection() as conn:
    #     with conn.cursor() as cur:
    #         cur.execute("INSERT INTO bookings (listing_id, guest_name, check_in, check_out, guests, total_price) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id", (...))
    #         booking_id = cur.fetchone()['id']
    #         conn.commit()
            
    mock_result = {
        "booking_id": 101,
        "status": "confirmed",
        "guest_name": guest_name,
        "total_price": total_price
    }
    return json.dumps(mock_result)
