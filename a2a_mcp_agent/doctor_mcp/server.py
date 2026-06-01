from fastmcp import FastMCP
import json
import os

# Create an MCP server
mcp = FastMCP("Doctor Search Server")

# Path to the doctors.json file
DOCTORS_FILE = "doctors.json"

def load_doctors():
    """Load doctors from the local json file."""
    if not os.path.exists(DOCTORS_FILE):
        return []
    with open(DOCTORS_FILE, "r") as f:
        return json.load(f)

@mcp.tool()
def list_doctors(state: str = None, city: str = None) -> list:
    """
    Returns a list of doctors filtered by state and/or city.
    
    Args:
        state: The US state code to filter by (e.g., 'GA', 'TX').
        city: The city name to filter by (e.g., 'Atlanta', 'Houston').
    """
    doctors = load_doctors()
    
    # Filter based on provided criteria
    filtered = []
    for d in doctors:
        address = d.get("address", {})
        d_state = address.get("state", "").lower()
        d_city = address.get("city", "").lower()
        
        match_state = (state.lower() == d_state) if state else True
        match_city = (city.lower() == d_city) if city else True
        
        if match_state and match_city:
            filtered.append(d)
            
    return filtered

if __name__ == "__main__":
    # Run as an HTTP (Streamable HTTP) server on port 8001
    mcp.run(transport="http", port=8001, host="0.0.0.0")
