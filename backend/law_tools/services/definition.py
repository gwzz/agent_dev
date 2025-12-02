"""Legal definition service for legal agent."""
from typing import Dict, Any
import re


def get_legal_definition(term: str) -> Dict[str, Any]:
    """
    Get legal definitions for specific legal terms.
    
    Args:
        term: Legal term to define
        
    Returns:
        Dictionary containing the legal definition
    """
    # Simulated legal definitions
    legal_definitions = {
        "due process": {
            "term": "Due Process",
            "definition": "The constitutional guarantee that an individual will be given notice and an opportunity to be heard before being deprived of life, liberty, or property by the government.",
            "context": "Fifth and Fourteenth Amendments to the U.S. Constitution",
            "types": ["Procedural Due Process", "Substantive Due Process"]
        },
        "stare decisis": {
            "term": "Stare Decisis",
            "definition": "The doctrine that courts should follow precedents established by previous decisions when ruling on similar cases.",
            "context": "Legal precedent and case law interpretation",
            "importance": "Promotes consistency and predictability in the judicial system"
        },
        "burden of proof": {
            "term": "Burden of Proof",
            "definition": "The obligation to present evidence supporting one's assertions in a legal proceeding. In criminal cases, the burden is on the prosecution to prove guilt beyond a reasonable doubt. In civil cases, the burden is usually on the plaintiff to prove their case by a preponderance of evidence.",
            "context": "Both criminal and civil law",
            "standards": ["Beyond a reasonable doubt", "Preponderance of evidence", "Clear and convincing evidence"]
        },
        "habeas corpus": {
            "term": "Habeas Corpus",
            "definition": "A legal action through which a person can seek relief from unlawful detention. The right to habeas corpus protects individuals from being held in custody unlawfully.",
            "context": "Constitutional protection against unlawful imprisonment",
            "meaning": "Literally means 'you shall have the body' in Latin"
        },
        "fiduciary duty": {
            "term": "Fiduciary Duty",
            "definition": "A legal obligation to act in the best interests of another party. Fiduciary relationships exist when one party is expected to act in the other's best interests, such as between attorneys and clients, or corporate directors and shareholders.",
            "context": "Corporate law, trusts, and professional responsibilities",
            "components": ["Duty of care", "Duty of loyalty", "Duty of good faith"]
        },
        "double jeopardy": {
            "term": "Double Jeopardy",
            "definition": "The constitutional protection preventing someone from being tried twice for the same offense. This protection is provided by the Fifth Amendment to the U.S. Constitution.",
            "context": "Criminal law",
            "purpose": "Protects individuals from the government's power to bring successive prosecutions for the same conduct"
        },
        "ex post facto": {
            "term": "Ex Post Facto",
            "definition": "A law that retroactively changes the legal consequences of actions that were committed before the law was enacted. The U.S. Constitution prohibits ex post facto criminal laws.",
            "context": "Criminal law",
            "constitutional_basis": "Article I, Sections 9 and 10 of the U.S. Constitution"
        },
        "subpoena": {
            "term": "Subpoena",
            "definition": "A writ requiring a person to appear in court at a specified time and place to give testimony or produce documents.",
            "types": ["Subpoena ad testificandum (to testify)", "Subpoena duces tecum (to produce documents)"],
            "consequences": "Failure to comply can result in contempt of court charges"
        },
        "voir dire": {
            "term": "Voir Dire",
            "definition": "The process of questioning potential jurors to determine their suitability for jury service.",
            "context": "Jury selection process",
            "purpose": "To ensure an impartial jury by identifying potential biases"
        },
        "tort": {
            "term": "Tort",
            "definition": "A wrongful act (other than breach of contract) that results in harm or injury to another and leads to civil liability.",
            "types": ["Intentional torts", "Negligence", "Strict liability"],
            "examples": ["Assault", "Battery", "Defamation", "Negligence"]
        }
    }
    
    # Convert term to lowercase for matching
    term_lower = term.lower()
    
    # Find matching definition
    result = None
    for key, definition in legal_definitions.items():
        if term_lower in key or key in term_lower:
            result = definition
            break
    
    # If no exact match, search in definition text
    if result is None:
        for key, definition in legal_definitions.items():
            if (term_lower in definition["definition"].lower() or
                any(term_lower in component.lower() for component in definition.get("components", [])) or
                any(term_lower in context.lower() for context in [definition.get("context", "")])):
                result = definition
                break
    
    if result is None:
        # Generate a basic response for unknown terms
        result = {
            "term": term,
            "definition": f"The legal definition of '{term}' may require consultation with legal dictionaries or professional legal resources.",
            "context": "General legal terminology",
            "note": "This is a general reference. For legal advice, consult with a qualified attorney."
        }
    
    return {
        "status": "success",
        "term": result["term"],
        "definition": result["definition"],
        "context": result.get("context", "General legal concept"),
        "details": result
    }