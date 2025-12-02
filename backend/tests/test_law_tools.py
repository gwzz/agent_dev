from law_tools.services import (
    get_jurisdiction_info,
    get_statute_info,
    get_recent_cases,
    get_legal_definition,
)


def test_jurisdiction_service():
    """Test the jurisdiction information service."""
    result = get_jurisdiction_info("federal")
    assert result["status"] == "success"
    assert "federal" in result["jurisdiction"].lower()
    print("✓ Jurisdiction service test passed")


def test_statute_service():
    """Test the statute information service."""
    result = get_statute_info("us_constitution")
    assert result["status"] == "success"
    assert "constitution" in result["statute_name"].lower()
    print("✓ Statute service test passed")


def test_recent_cases_service():
    """Test the recent cases service."""
    result = get_recent_cases("constitutional")
    assert result["status"] == "success"
    assert "constitutional" in result["law_area"]
    print("✓ Recent cases service test passed")


def test_legal_definition_service():
    """Test the legal definition service."""
    result = get_legal_definition("due process")
    assert result["status"] == "success"
    assert "due process" in result["term"].lower()
    print("✓ Legal definition service test passed")


def test_all_law_services():
    """Run all law service tests."""
    test_jurisdiction_service()
    test_statute_service()
    test_recent_cases_service()
    test_legal_definition_service()
    print("All law service tests passed!")


if __name__ == "__main__":
    test_all_law_services()