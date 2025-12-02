"""Jurisdiction information service for legal agent."""
import random
from typing import Dict, Any, List


def get_jurisdiction_info(jurisdiction: str) -> Dict[str, Any]:
    """
    Get information about legal jurisdictions.
    
    Args:
        jurisdiction: Name of the jurisdiction to look up
        
    Returns:
        Dictionary containing jurisdiction information
    """
    # Simulated jurisdiction data
    jurisdiction_data = {
        "federal": {
            "name": "Federal Courts (United States)",
            "level": "Federal",
            "types": ["Supreme Court", "Circuit Courts of Appeal", "District Courts"],
            "coverage": "Matters involving federal law, constitutional issues, interstate commerce",
            "highest_court": "Supreme Court of the United States"
        },
        "california": {
            "name": "California State Courts",
            "level": "State",
            "types": ["Supreme Court", "Courts of Appeal", "Superior Courts"],
            "coverage": "State law matters within California",
            "highest_court": "California Supreme Court"
        },
        "new york": {
            "name": "New York State Courts",
            "level": "State",
            "types": ["Court of Appeals", "Appellate Division", "Supreme Court", "County Courts"],
            "coverage": "State law matters within New York",
            "highest_court": "Court of Appeals of New York"
        },
        "texas": {
            "name": "Texas State Courts",
            "level": "State",
            "types": ["Supreme Court", "Court of Criminal Appeals", "Courts of Appeals", "District Courts"],
            "coverage": "State law matters within Texas",
            "highest_court": "Texas Supreme Court"
        }
    }
    
    # Convert jurisdiction to lowercase and remove spaces for comparison
    lookup_key = jurisdiction.lower().replace(' ', '').replace('-', '')
    
    # Find matching jurisdiction
    result = None
    for key, data in jurisdiction_data.items():
        if key in lookup_key or lookup_key in key:
            result = data
            break
    
    if result is None:
        # Generate a basic response for unknown jurisdictions
        result = {
            "name": f"{jurisdiction.title()} Jurisdiction",
            "level": "Unknown",
            "types": ["Unknown Court Types"],
            "coverage": f"Legal matters within {jurisdiction} jurisdiction",
            "highest_court": f"{jurisdiction.title()} Supreme Court" if jurisdiction.lower() != 'federal' else "Supreme Court of the United States"
        }
    
    return {
        "status": "success",
        "jurisdiction": result["name"],
        "level": result["level"],
        "court_types": result["types"],
        "coverage": result["coverage"],
        "highest_court": result["highest_court"],
        "description": f"Information about the {result['name']} legal system, which is a {result['level'].lower()} jurisdiction handling {result['coverage'].lower()}. The highest court in this jurisdiction is the {result['highest_court']}."
    }