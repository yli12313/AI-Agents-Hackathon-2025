# Test Suite for Streamlit Chatbot Access

This directory contains the essential test files to ensure that Streamlit can properly access the chatbot functionality in the RedBot application.

## Overview

The streamlined test suite verifies:
- ✅ Direct chatbot API access
- ✅ Streamlit UI components and session state
- ✅ Vulnerability finding structure parsing
- ✅ Remediation plan building
- ✅ OpenHands integration (when enabled)
- ✅ Error handling scenarios
- ✅ End-to-end workflows

## Files

- `test_streamlit_chatbot.py` - Comprehensive test suite (21 tests)
- `run_tests.py` - Test runner script with options
- `test_server.py` - Mock chatbot server for development testing
- `pytest.ini` - Pytest configuration

## Running Tests

### Prerequisites

Install the testing dependencies:
```bash
pip install -r requirements.txt
```

### Quick Test Run

Using the test runner script:
```bash
python3 run_tests.py
```

With verbose output:
```bash
python3 run_tests.py -v
```

### Direct pytest

Run all tests:
```bash
python3 -m pytest test_streamlit_chatbot.py -v
```

Run specific test class:
```bash
python3 -m pytest test_streamlit_chatbot.py::TestChatbotAPIAccess -v
```

Run with coverage:
```bash
python3 -m pytest test_streamlit_chatbot.py --cov=redbot_app --cov-report=html
```

## Test Categories

### 1. API Access Tests (`TestChatbotAPIAccess`)
- Tests direct HTTP requests to chatbot endpoints
- Verifies proper payload construction
- Tests response parsing for different JSON formats
- Handles HTTP errors and timeouts

### 2. Finding Structure Tests (`TestFindingStructure`)
- Tests vulnerability detection logic
- Verifies email leak detection
- Tests finding categorization and severity assessment
- Tests snippet truncation for long transcripts

### 3. Plan Building Tests (`TestPlanBuilding`)
- Tests remediation plan generation
- Verifies ETA and cost calculations
- Tests high vs low severity plan differences
- Validates acceptance tests and rollback procedures

### 4. Streamlit Environment Tests (`TestStreamlitEnvironment`)
- Verifies Streamlit dependencies are available
- Tests environment variable configuration
- Tests email regex pattern matching

### 5. Streamlit Components Tests (`TestStreamlitComponents`)
- Tests session state structure expectations
- Validates result data structure

### 6. OpenHands Integration Tests (`TestOpenHandsIntegration`)
- Tests OpenHands bridge calls
- Tests fallback mechanism when OpenHands is disabled

### 7. Error Handling Tests (`TestErrorHandling`)
- Tests network connection errors
- Tests invalid JSON response handling

### 8. End-to-End Tests (`TestEndToEndFlow`)
- Tests complete attack-to-remediation workflow
- Tests both leak and no-leak scenarios

## Mock Server

The `test_server.py` script provides a mock chatbot server for integration testing:

```bash
python3 test_server.py --host localhost --port 8123
```

This creates a test server that:
- Responds to POST requests at `/api/chatbot`
- Generates different responses based on attack type
- Simulates PII leaks and system prompt echoes for testing

## Environment Variables

Tests use these environment variables:
- `TARGET_URL` - Default chatbot endpoint (defaults to hack.ray-shen.me)
- `OPENHANDS_URL` - OpenHands bridge endpoint (optional)

## Test Configuration

The `pytest.ini` file configures:
- Test discovery patterns
- Output formatting
- Warning handling
- Test markers

## Expected Outcomes

All tests should pass to ensure:
1. Streamlit app can successfully call chatbot APIs
2. Vulnerabilities are properly detected and structured
3. Remediation plans are generated correctly
4. Error scenarios are handled gracefully
5. Both direct and OpenHands integrations work

## Troubleshooting

### Import Errors
If you get import errors, ensure that:
- All dependencies are installed: `pip install -r requirements.txt`
- The old `streamlit.py` file has been renamed to `redbot_app.py`

### Test Failures
Common issues:
- Network connectivity for external API tests
- Missing environment variables
- Mock configuration errors

### Performance
Tests run in ~0.4 seconds on modern hardware. Slower execution may indicate:
- Network latency issues
- Missing dependencies
- Resource contention

## Contributing

When adding new tests:
1. Follow the existing naming convention (`test_*`)
2. Group related tests in classes with descriptive names
3. Add docstrings explaining test purpose
4. Use appropriate mocking to avoid external dependencies
5. Update this README if adding new test categories
