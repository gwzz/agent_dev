"""Recent cases information service for legal agent."""
from typing import Dict, Any, List
import datetime


def get_recent_cases(law_area: str) -> Dict[str, Any]:
    """
    Get information about recent significant legal cases.
    
    Args:
        law_area: Area of law to search for recent cases (e.g., constitutional, corporate, criminal)
        
    Returns:
        Dictionary containing recent case information
    """
    # Simulated recent cases data
    cases_data = {
        "constitutional": [
            {
                "name": "Dobbs v. Jackson Women's Health Organization",
                "citation": "597 U.S. ___ (2022)",
                "date": "2022-06-24",
                "court": "Supreme Court of the United States",
                "significance": "Overturned Roe v. Wade, holding that the Constitution does not confer a right to abortion",
                "impact": "Returned the authority to regulate abortion to the people and their elected representatives"
            },
            {
                "name": "Students for Fair Admissions, Inc. v. Harvard",
                "citation": "599 U.S. ___ (2023)",
                "date": "2023-06-29",
                "court": "Supreme Court of the United States",
                "significance": "Ruled that race-conscious admissions programs at Harvard and UNC were unconstitutional",
                "impact": "Effectively ended affirmative action in college admissions"
            },
            {
                "name": "West Virginia v. EPA",
                "citation": "597 U.S. ___ (2022)",
                "date": "2022-06-30",
                "court": "Supreme Court of the United States",
                "significance": "Limited EPA's authority to regulate carbon emissions from power plants",
                "impact": "Applied the 'major questions doctrine' to limit administrative agency power"
            }
        ],
        "corporate": [
            {
                "name": "Salman v. United States",
                "citation": "579 U.S. ___ (2016)",
                "date": "2016-12-06",
                "court": "Supreme Court of the United States",
                "significance": "Held that a tippee receives 'meaningful personal benefit' when trading on material, nonpublic information",
                "impact": "Expanded liability for insider trading based on gift theory"
            },
            {
                "name": "Coty Germany GmbH v. Parfums de Courcelles S.A.",
                "citation": "C-282/19, EU:C:2020:893",
                "date": "2020-11-19",
                "court": "Court of Justice of the European Union",
                "significance": "Addressed trademark rights and parallel imports in the EU",
                "impact": "Clarified limitations on trademark enforcement against parallel imports"
            }
        ],
        "criminal": [
            {
                "name": "Riley v. California",
                "citation": "573 U.S. 373 (2014)",
                "date": "2014-06-25",
                "court": "Supreme Court of the United States",
                "significance": "Held that police generally may not search digital information on a cell phone seized from an individual who has been arrested",
                "impact": "Established that digital privacy rights require warrant protection for cell phone searches"
            },
            {
                "name": "Carpenter v. United States",
                "citation": "585 U.S. ___ (2018)",
                "date": "2018-06-22",
                "court": "Supreme Court of the United States",
                "significance": "Required law enforcement to obtain a warrant before acquiring historical cell phone location data",
                "impact": "Strengthened Fourth Amendment protection for digital location data"
            }
        ],
        "privacy": [
            {
                "name": "Carpenter v. United States",
                "citation": "585 U.S. ___ (2018)",
                "date": "2018-06-22",
                "court": "Supreme Court of the United States",
                "significance": "Required law enforcement to obtain a warrant before acquiring historical cell phone location data",
                "impact": "Strengthened Fourth Amendment protection for digital location data"
            },
            {
                "name": "Riley v. California",
                "citation": "573 U.S. 373 (2014)",
                "date": "2014-06-25",
                "court": "Supreme Court of the United States",
                "significance": "Held that police generally may not search digital information on a cell phone seized from an individual who has been arrested",
                "impact": "Established that digital privacy rights require warrant protection for cell phone searches"
            }
        ]
    }
    
    # Convert query to lowercase for matching
    query_lower = law_area.lower()
    
    # Find relevant cases based on law area
    matched_cases = []
    for area, cases in cases_data.items():
        if query_lower in area:
            matched_cases.extend(cases)
            break
    
    # If no exact match, try to match partial keywords
    if not matched_cases:
        for area, cases in cases_data.items():
            if any(keyword in area for keyword in ["constitutional", "corporate", "criminal", "privacy"]):
                if (query_lower in "constitutional" or query_lower in "civil rights" or 
                    query_lower in "rights" or query_lower in "first amendment"):
                    matched_cases.extend(cases_data["constitutional"])
                    break
                elif (query_lower in "corporate" or query_lower in "business" or 
                      query_lower in "company" or query_lower in "securities"):
                    matched_cases.extend(cases_data["corporate"])
                    break
                elif (query_lower in "criminal" or query_lower in "crime" or 
                      query_lower in "felony" or query_lower in "misdemeanor"):
                    matched_cases.extend(cases_data["criminal"])
                    break
                elif (query_lower in "privacy" or query_lower in "gdpr" or 
                      query_lower in "data protection"):
                    matched_cases.extend(cases_data["privacy"])
                    break
    
    # If still no matches, return general info
    if not matched_cases:
        matched_cases = [{
            "name": f"Recent developments in {law_area}",
            "citation": "N/A",
            "date": str(datetime.date.today()),
            "court": "Various",
            "significance": f"Information about recent legal developments in the area of {law_area}",
            "impact": f"General information about trends in {law_area} law may require further legal research"
        }]
    
    # Limit to most recent 3 cases
    recent_cases = matched_cases[:3]
    
    return {
        "status": "success",
        "law_area": law_area,
        "total_cases_found": len(matched_cases),
        "recent_cases": recent_cases,
        "description": f"Recent significant legal cases in the area of {law_area}. These cases represent important legal precedents and developments in this field."
    }