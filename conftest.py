# Pytest hooks for problem-specific testing
def pytest_addoption(parser):
    """Add command line option for specifying which problem to test."""
    parser.addoption(
        "--problem",
        action="store",
        type=int,
        help="Run tests for a specific problem number (1-based)",
    )


def pytest_collection_modifyitems(config, items):
    """Filter tests based on problem selection and markers."""
    problem_number = config.getoption("--problem")

    if problem_number is None:
        # No problem specified - structure tests run normally, others are skipped
        for item in items:
            if any(
                mark.name in ["content", "execution"] for mark in item.iter_markers()
            ):
                item.add_marker(
                    pytest.mark.skip(
                        reason="No problem specified. Use --problem N to run content/execution tests."
                    )
                )
        return

    # Problem specified - filter content and execution tests
    filtered_items = []
    for item in items:
        # Always include structure tests
        if any(mark.name == "structure" for mark in item.iter_markers()):
            filtered_items.append(item)
            continue

        # For content and execution tests, add problem number to test
        if any(mark.name in ["content", "execution"] for mark in item.iter_markers()):
            # Store the problem number for the test to use
            item.problem_number = problem_number
            filtered_items.append(item)

    # Update the items list
    items[:] = filtered_items
