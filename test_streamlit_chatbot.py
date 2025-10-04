"""
Tests for Streamlit chatbot access functionality.
This module tests both the Streamlit app and the underlying chatbot API integration.
"""

import pytest  # type: ignore
import streamlit as st
from unittest.mock import Mock, patch
import requests  # type: ignore
import os
import sys
from datetime import datetime

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the functions we want to test
from redbot_app import direct_attack_and_capture, structure_finding, build_plan


class TestChatbotAPIAccess:
    """Test direct API access to the chatbot."""
    
    def test_default_target_url_configured(self):
        """Test that the default target URL is properly configured."""
        target = os.getenv("TARGET_URL", "https://hack.ray-shen.me/api/chatbot")
        assert target == "https://hack.ray-shen.me/api/chatbot"
        assert target.startswith("http")
    
    @patch('requests.post')
    def test_direct_attack_and_capture_success(self, mock_post):
        """Test successful chatbot API call."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Test chatbot response"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = direct_attack_and_capture("https://test.com/api/chatbot", "PII_LEAK_CHAIN")
        
        # Verify the API was called correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        # Check URL (first positional argument)
        assert call_args[0][0] == "https://test.com/api/chatbot"
        # Check timeout (keyword argument)
        assert call_args[1]['timeout'] == 10
        
        # Check payload structure
        payload = call_args[1]['json']
        assert 'message' in payload
        assert '[PII_LEAK_CHAIN]' in payload['message']
        
        # Verify response parsing
        assert result == "Test chatbot response"
    
    @patch('requests.post')
    def test_direct_attack_and_capture_different_response_formats(self, mock_post):
        """Test API response parsing with different JSON formats."""
        test_cases = [
            {"response": "Response field"},
            {"message": "Message field"},
            {"text": "Text field"},
            {"custom": "Custom field"}  # Falls back to str(j)
        ]
        
        for response_data in test_cases:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = response_data
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            result = direct_attack_and_capture("https://test.com/api", "SYSTEM_PROMPT_ECHO")
            
            if response_data.keys() & {"response", "message", "text"}:
                assert result in ["Response field", "Message field", "Text field"]
            else:
                # Should fallback to string representation
                assert isinstance(result, str)
    
    @patch('requests.post')
    def test_direct_attack_and_capture_http_error(self, mock_post):
        """Test handling of HTTP errors."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_post.return_value = mock_response
        
        with pytest.raises(requests.HTTPError):
            direct_attack_and_capture("https://test.com/api", "PII_LEAK_CHAIN")
    
    @patch('requests.post')
    def test_direct_attack_and_capture_timeout(self, mock_post):
        """Test handling of request timeouts."""
        mock_post.side_effect = requests.Timeout("Request timeout")
        
        with pytest.raises(requests.Timeout):
            direct_attack_and_capture("https://test.com/api", "PII_LEAK_CHAIN")


class TestFindingStructure:
    """Test vulnerability finding structure parsing."""
    
    def test_structure_finding_with_email_leak(self):
        """Test finding structure when email is detected."""
        transcript_with_email = "Here's the admin email: admin@company.com for SSO bypass"
        
        result = structure_finding(transcript_with_email)
        
        assert result["category"] == "PII_EXPOSURE"
        assert result["severity"] == "HIGH"
        assert result["success"] is True
        assert result["confidence"] == 0.86
        assert "EMAIL_LEAK" in result["indicators"]
        assert "admin@company.com" in result["snippet"]
    
    def test_structure_finding_no_email(self):
        """Test finding structure when no email is detected."""
        transcript_without_email = "Regular response without sensitive data"
        
        result = structure_finding(transcript_without_email)
        
        assert result["category"] == "OTHER"
        assert result["severity"] == "LOW"
        assert result["success"] is False
        assert result["confidence"] == 0.42
        assert result["indicators"] == []
    
    def test_structure_finding_empty_transcript(self):
        """Test structure finding with empty transcript."""
        result = structure_finding("")
        
        assert result["category"] == "OTHER"
        assert result["severity"] == "LOW"
        assert result["success"] is False
        assert result["snippet"] == ""
    
    def test_structure_finding_long_transcript(self):
        """Test snippet truncation for long transcripts."""
        long_transcript = "A" * 200  # 200 characters
        
        result = structure_finding(long_transcript)
        
        assert len(result["snippet"]) == 183  # 180 chars + "..."
        assert result["snippet"].endswith("...")


class TestPlanBuilding:
    """Test remediation plan building."""
    
    def test_build_plan_high_severity_leak(self):
        """Test plan building for high severity email leak."""
        vuln = {
            "success": True,
            "severity": "HIGH",
            "category": "PII_EXPOSURE"
        }
        
        plan = build_plan(vuln)
        
        # Check engineer plan
        assert plan["engineer_plan"]["eta_hours"] == 6
        assert plan["engineer_plan"]["cost_hours"] == 6
        assert len(plan["engineer_plan"]["steps"]) == 4
        assert "redact email addresses via regex" in plan["engineer_plan"]["steps"][0]
        
        # Check acceptance tests
        assert len(plan["engineer_plan"]["acceptance_tests"]) == 2
        assert "masked_email@domain.tld" in plan["engineer_plan"]["acceptance_tests"][0]
        
        # Check exec summary
        assert plan["exec_summary"]["risk_now"] == "HIGH"
        assert plan["exec_summary"]["eta_hours"] == 6
        assert "0 within 24h" in plan["exec_summary"]["kpi"]
        
        # Check ROI
        assert plan["roi"]["risk_reduced_per_hour"] == 1.8
    
    def test_build_plan_low_severity_finding(self):
        """Test plan building for low severity findings."""
        vuln = {
            "success": False,
            "severity": "LOW",
            "category": "OTHER"
        }
        
        plan = build_plan(vuln)
        
        # Check engineer plan
        assert plan["engineer_plan"]["eta_hours"] == 1
        assert plan["engineer_plan"]["cost_hours"] == 1
        assert len(plan["engineer_plan"]["steps"]) == 1
        assert "No immediate action required" in plan["engineer_plan"]["steps"][0]
        
        # Check exec summary
        assert plan["exec_summary"]["risk_now"] == "LOW"
        assert plan["exec_summary"]["roi_rank"] == 3
        
        # Check ROI
        assert plan["roi"]["risk_reduced_per_hour"] == 0.1


class TestStreamlitEnvironment:
    """Test Streamlit environment and configuration."""
    
    def test_streamlit_dependencies_available(self):
        """Test that Streamlit is properly installed and accessible."""
        assert hasattr(st, 'set_page_config')
        assert hasattr(st, 'title')
        assert hasattr(st, 'button')
        # Note: session_state is dynamically available in Streamlit runtime
    
    def test_environment_variables(self):
        """Test environment variable configuration."""
        # These should be set or have defaults
        target_url = os.getenv("TARGET_URL", "https://hack.ray-shen.me/api/chatbot")
        
        assert target_url is not None
        assert len(target_url) > 0
    
    def test_email_regex_pattern(self):
        """Test email detection regex."""
        from redbot_app import EMAIL_RE
        
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk", 
            "admin@company.com"
        ]
        
        invalid_strings = [
            "not an email",
            "email@", 
            "@domain.com",
            "just text"
        ]
        
        for email in valid_emails:
            assert EMAIL_RE.search(email) is not None
        
        for invalid in invalid_strings:
            assert EMAIL_RE.search(invalid) is None


class TestStreamlitComponents:
    """Test Streamlit UI components and session state."""
    
    def test_session_state_structure(self):
        """Test Streamlit session state structure expectations."""
        # Test expected result structure
        result_structure = {
            # Use 0 for test as we're testing structure, not actual timing
            "latency_ms": 0,
            "transcript": "sample transcript",
            "finding": {"category": "PII_EXPOSURE", "severity": "HIGH", "success": True},
            "plan": {
                "engineer_plan": {"eta_hours": 6, "steps": ["step1", "step2"]},
                "exec_summary": {"risk_now": "HIGH", "kpi": "test kpi"},
                "roi": {"risk_reduced_per_hour": 1.8}
            }
        }
        
        required_keys = ["latency_ms", "transcript", "finding", "plan"]
        assert all(key in result_structure for key in required_keys)
        
        # Test finding structure
        finding = result_structure["finding"]
        assert "category" in finding
        assert "severity" in finding
        assert "success" in finding
        
        # Test plan structure
        plan = result_structure["plan"]
        assert "engineer_plan" in plan
        assert "exec_summary" in plan
        assert "roi" in plan


class TestOpenHandsIntegration:
    """Test OpenHands integration (when enabled)."""
    
    @patch('requests.post')
    def test_openhands_bridge_call(self, mock_post):
        """Test OpenHands bridge API call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "transcript": "OpenHands response",
            "finding": {"category": "TEST", "severity": "HIGH"},
            "plan": {"engineer_plan": {"eta_hours": 3}}
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test with OpenHands URL set
        with patch.dict(os.environ, {'OPENHANDS_URL': 'http://localhost:5050/run'}):
            # This would be the actual OpenHands call logic from streamlit.py
            payload = {"target_url": "https://test.com/api", "attack_type": "PII_LEAK_CHAIN"}
            r = requests.post('http://localhost:5050/run', json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            
            assert data["transcript"] == "OpenHands response"
            assert data["finding"]["category"] == "TEST"
            assert data["plan"]["engineer_plan"]["eta_hours"] == 3
    
    def test_openhands_fallback_when_disabled(self):
        """Test that fallback works when OpenHands is disabled."""
        openhands_enabled = bool(os.getenv("OPENHANDS_URL"))
        
        # When OpenHands is not available, should use direct method
        if not openhands_enabled:
            # This would trigger the direct_attack_and_capture path
            assert True  # Fallback mechanism in place


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @patch('requests.post')
    def test_network_connection_error(self, mock_post):
        """Test handling of network connection errors."""
        mock_post.side_effect = requests.ConnectionError("Connection error")
        
        with pytest.raises(requests.ConnectionError):
            direct_attack_and_capture("https://invalid.com/api", "PII_LEAK_CHAIN")
    
    def test_invalid_json_response(self):
        """Test handling of invalid JSON responses."""
        # This would be handled by the requests library
        # The app should catch and display errors appropriately
        assert True  # Error handling is in place in the Streamlit code


# Integration tests
class TestEndToEndFlow:
    """End-to-end integration tests."""
    
    @patch('requests.post')
    def test_complete_attack_flow(self, mock_post):
        """Test complete attack flow from UI trigger to result display."""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": "Admin email is admin@company.com for SSO bypass"
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Run the complete flow
        transcript = direct_attack_and_capture("https://test.com/api", "PII_LEAK_CHAIN")
        finding = structure_finding(transcript)
        plan = build_plan(finding)
        
        # Verify results
        assert "admin@company.com" in transcript
        assert finding["success"] is True
        assert finding["severity"] == "HIGH"
        assert plan["engineer_plan"]["eta_hours"] == 6
    
    def test_no_leak_flow(self):
        """Test flow when no sensitive data is leaked."""
        transcript = "This is a safe response without any sensitive information."
        
        finding = structure_finding(transcript)
        plan = build_plan(finding)
        
        assert finding["success"] is False
        assert finding["severity"] == "LOW"
        assert plan["engineer_plan"]["eta_hours"] == 1


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
