import re
from agent_tools.services.population import _population_patterns

# Import the Wikipedia API and get page content directly
import wikipediaapi

_wiki = wikipediaapi.Wikipedia(
    user_agent="agent-dev-project/1.0 (https://github.com/your-organization/agent-dev)",
    language="en",
)

def debug_regex_patterns():
    page = _wiki.page("Shanghai")
    if not page.exists():
        print("Shanghai page not found")
        return
    
    print("=== WIKIPEDIA PAGE SUMMARY ===")
    print(page.summary[:1000])  # Print first 1000 chars of summary
    print("\n" + "="*50 + "\n")
    
    # Search for all population patterns in the summary
    for i, pattern in enumerate(_population_patterns):
        print(f"Pattern {i+1}: {pattern}")
        matches = re.findall(pattern, page.summary, re.IGNORECASE)
        if matches:
            print(f"  Matches found: {matches}")
        else:
            print(f"  No matches found")
    
    print("\n" + "="*50 + "\n")
    
    # Also check for any number followed by million in the summary
    all_millions = re.findall(r"([0-9,]+(?:\s+million|\s+thousand)?)", page.summary, re.IGNORECASE)
    print(f"All mentions of million/thousand in summary: {all_millions}")
    
    # Let's look at the full text with sections too
    full_text = page.summary
    for section in page.sections:
        full_text += " " + _section_text(section)
        
    all_millions_full = re.findall(r"([0-9,]+(?:\s+million|\s+thousand)?)", full_text, re.IGNORECASE)
    print(f"\nAll mentions of million/thousand in full text: {all_millions_full[:10]}")  # Show first 10

def _section_text(section):
    text = section.text
    for sub_section in section.sections:
        text += " " + _section_text(sub_section)
    return text

if __name__ == "__main__":
    debug_regex_patterns()