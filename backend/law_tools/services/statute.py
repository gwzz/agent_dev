"""Statute information service for legal agent."""
import re
from typing import Dict, Any, List


def get_statute_info(statute_query: str) -> Dict[str, Any]:
    """
    Get information about specific statutes or laws.
    
    Args:
        statute_query: Name, number, or description of the statute to look up
        
    Returns:
        Dictionary containing statute information
    """
    # Simulated statute data
    statute_data = {
        "us_constitution": {
            "name": "United States Constitution",
            "official_name": "Constitution of the United States",
            "jurisdiction": "Federal",
            "enacted": "1787",
            "amendments": 27,
            "key_provisions": [
                "First Amendment: Freedom of speech, religion, and press",
                "Fourth Amendment: Protection against unreasonable searches",
                "Fifth Amendment: Right against self-incrimination",
                "Fourteenth Amendment: Equal protection under the law"
            ],
            "description": "The supreme law of the United States, establishing the structure of the federal government and fundamental rights of citizens."
        },
        "cpra": {
            "name": "California Consumer Privacy Act",
            "official_name": "California Consumer Privacy Act (CCPA)",
            "jurisdiction": "California",
            "enacted": "2018",
            "effective_date": "2020-01-01",
            "purpose": "To enhance privacy rights and consumer protection for residents of California",
            "key_provisions": [
                "Right to know what personal information is collected",
                "Right to delete personal information",
                "Right to opt-out of sale of personal information",
                "Right to non-discrimination for exercising privacy rights"
            ],
            "description": "A comprehensive privacy law that grants California residents significant control over their personal information."
        },
        "gdpr": {
            "name": "GDPR",
            "official_name": "General Data Protection Regulation (EU)",
            "jurisdiction": "European Union",
            "enacted": "2016",
            "effective_date": "2018-05-25",
            "purpose": "To protect the privacy and personal data of EU citizens",
            "key_provisions": [
                "Right to access personal data",
                "Right to be forgotten",
                "Data portability",
                "Consent requirements for data processing"
            ],
            "description": "Regulation on data protection and privacy in the European Union and European Economic Area."
        },
        "hipaa": {
            "name": "HIPAA",
            "official_name": "Health Insurance Portability and Accountability Act",
            "jurisdiction": "Federal",
            "enacted": "1996",
            "purpose": "To protect health information privacy and security",
            "key_provisions": [
                "Privacy Rule: Protects individually identifiable health information",
                "Security Rule: Sets standards for electronic protected health information",
                "Breach Notification Rule: Requires notification of breaches"
            ],
            "description": "Federal law that provides data privacy and security provisions for safeguarding medical information."
        },
        "sox": {
            "name": "SOX",
            "official_name": "Sarbanes-Oxley Act",
            "jurisdiction": "Federal",
            "enacted": "2002",
            "purpose": "To protect investors from fraudulent accounting practices",
            "key_provisions": [
                "Corporate responsibility for financial reports",
                "Enhanced criminal penalties",
                "Accountability of corporate executives",
                "Protection for whistleblowers"
            ],
            "description": "Federal law that established sweeping auditing and financial regulations for public companies."
        }
    }
    
    # Convert query to lowercase for matching
    query_lower = statute_query.lower()
    
    # Find matching statute based on name, official name, or key provisions
    result = None
    for key, data in statute_data.items():
        if (query_lower in data["name"].lower() or 
            query_lower in data["official_name"].lower() or 
            any(query_lower in prov.lower() for prov in data["key_provisions"])):
            result = data
            break
    
    if result is None:
        # Generate a basic response for unknown statutes
        result = {
            "name": f"{statute_query}",
            "official_name": f"{statute_query}",
            "jurisdiction": "Unknown",
            "enacted": "Unknown",
            "purpose": f"Information about {statute_query}",
            "key_provisions": [f"Details about {statute_query} may not be readily available in the current database"],
            "description": f"Information about {statute_query} statute. More detailed information may require consultation with legal resources."
        }
    
    return {
        "status": "success",
        "statute_name": result["name"],
        "official_name": result["official_name"],
        "jurisdiction": result["jurisdiction"],
        "enacted": result["enacted"],
        "purpose": result["purpose"],
        "key_provisions": result["key_provisions"],
        "description": result["description"]
    }