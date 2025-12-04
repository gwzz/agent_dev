from law_expert.agent import root_agent


def test_law_agent_basic():
    """Test that the law agent can process basic legal questions."""
    # Test legal definition query
    result = root_agent.run_live("What is due process?")
    assert result is not None
    print("✓ Legal definition query test passed")

    # Test jurisdiction query
    result = root_agent.run_live("What is the jurisdiction of federal courts?")
    assert result is not None
    print("✓ Jurisdiction query test passed")

    # Test statute query
    result = root_agent.run_live("Tell me about the US Constitution")
    assert result is not None
    print("✓ Statute query test passed")

    # Test case law query
    result = root_agent.run_live("What are recent privacy cases?")
    assert result is not None
    print("✓ Case law query test passed")

    print("All law agent tests passed!")


if __name__ == "__main__":
    test_law_agent_basic()