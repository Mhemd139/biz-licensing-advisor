#!/usr/bin/env python3
"""
Comprehensive LLM Integration Tests
Tests both mock mode and real LLM functionality
"""

import os
import sys
import pytest
import json

# Add parent directory to Python path to import backend modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from llm import call_llm, validate_report_references, ReportJSON
from matching import match_rules


class TestLLMIntegration:
    """Test suite for LLM integration validation"""
    
    @pytest.fixture
    def sample_rules(self):
        """Load actual rules from requirements.json"""
        data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "requirements.json")
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @pytest.fixture
    def test_profiles(self):
        """Test business profiles for validation"""
        return [
            {
                "name": "Small cafe",
                "profile": {
                    "size_m2": 40,
                    "seats": 20,
                    "serves_alcohol": False,
                    "uses_gas": False,
                    "has_misting": False,
                    "offers_delivery": False
                }
            },
            {
                "name": "Medium restaurant with alcohol",
                "profile": {
                    "size_m2": 120,
                    "seats": 80,
                    "serves_alcohol": True,
                    "uses_gas": True,
                    "has_misting": False,
                    "offers_delivery": True
                }
            },
            {
                "name": "Large restaurant full features",
                "profile": {
                    "size_m2": 250,
                    "seats": 180,
                    "serves_alcohol": True,
                    "uses_gas": True,
                    "has_misting": True,
                    "offers_delivery": True
                }
            }
        ]
    
    def test_mock_mode_functionality(self, sample_rules, test_profiles):
        """Test that mock mode works correctly"""
        os.environ["LLM_MOCK_MODE"] = "true"
        
        for test_case in test_profiles:
            profile = test_case["profile"]
            name = test_case["name"]
            
            # Get matched rules
            matched_rules = match_rules(profile, sample_rules)
            rule_ids = [rule["id"] for rule in matched_rules]
            
            # Generate report
            report = call_llm(profile, matched_rules)
            
            # Validate report structure
            assert isinstance(report, ReportJSON), f"Report should be ReportJSON instance for {name}"
            assert report.total_rules == len(matched_rules), f"Total rules mismatch for {name}"
            assert len(report.sections) > 0, f"Report should have sections for {name}"
            assert len(report.summary) > 0, f"Report should have summary for {name}"
            assert isinstance(report.recommendations, list), f"Recommendations should be list for {name}"
            assert isinstance(report.authorities, list), f"Authorities should be list for {name}"
            
            # Validate rule references
            is_valid = validate_report_references(report, rule_ids)
            assert is_valid, f"Report contains invalid rule references for {name}"
            
            print(f"✓ Mock mode test passed for {name}: {len(matched_rules)} rules, {len(report.sections)} sections")
    
    def test_real_llm_mode_with_api_key(self, sample_rules, test_profiles):
        """Test real LLM mode when API key is available"""
        # Check if OpenAI API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            pytest.skip("OPENAI_API_KEY not available - skipping real LLM tests")
        
        # Disable mock mode to test real LLM
        os.environ["LLM_MOCK_MODE"] = "false"
        
        # Test with one profile to avoid excessive API usage
        test_case = test_profiles[1]  # Medium restaurant
        profile = test_case["profile"]
        name = test_case["name"]
        
        matched_rules = match_rules(profile, sample_rules)
        rule_ids = [rule["id"] for rule in matched_rules]
        
        try:
            # Generate report using real LLM
            report = call_llm(profile, matched_rules)
            
            # Validate report structure
            assert isinstance(report, ReportJSON), f"Real LLM report should be ReportJSON instance"
            assert report.total_rules == len(matched_rules), f"Real LLM total rules mismatch"
            assert len(report.sections) > 0, f"Real LLM report should have sections"
            assert len(report.summary) > 0, f"Real LLM report should have summary"
            
            # Validate rule references
            is_valid = validate_report_references(report, rule_ids)
            assert is_valid, f"Real LLM report contains invalid rule references"
            
            print(f"✓ Real LLM test passed for {name}: Generated report with {len(report.sections)} sections")
            
        except Exception as e:
            pytest.fail(f"Real LLM test failed: {str(e)}")
    
    def test_fallback_to_mock_mode(self, sample_rules, test_profiles):
        """Test that system falls back to mock mode when LLM fails"""
        # Set invalid API key to trigger fallback
        os.environ["OPENAI_API_KEY"] = "invalid_key"
        os.environ["LLM_MOCK_MODE"] = "false"
        
        profile = test_profiles[0]["profile"]
        matched_rules = match_rules(profile, sample_rules)
        
        # Should fallback to mock mode gracefully
        report = call_llm(profile, matched_rules)
        
        assert isinstance(report, ReportJSON), "Should fallback to mock mode"
        assert report.total_rules == len(matched_rules), "Fallback should work correctly"
        
        print("✓ Fallback to mock mode test passed")
    
    def test_report_quality_metrics(self, sample_rules, test_profiles):
        """Test report quality and content validation"""
        os.environ["LLM_MOCK_MODE"] = "true"
        
        for test_case in test_profiles:
            profile = test_case["profile"]
            matched_rules = match_rules(profile, sample_rules)
            report = call_llm(profile, matched_rules)
            
            # Check bilingual content
            assert "עסקי" in report.summary or "רישיונות" in report.summary, "Should contain Hebrew content"
            assert "business" in report.summary.lower() or "requirements" in report.summary.lower(), "Should contain English content"
            
            # Check authority grouping
            expected_authorities = list(set(rule["authority"] for rule in matched_rules))
            assert len(report.authorities) == len(expected_authorities), "Should list all relevant authorities"
            
            # Check priority accuracy
            expected_high_priority = sum(1 for rule in matched_rules if rule["priority"] == "high")
            assert report.high_priority_count == expected_high_priority, "High priority count should be accurate"
            
            # Check recommendations exist
            assert len(report.recommendations) > 0, "Should provide recommendations"
            
            print(f"✓ Quality metrics passed for {test_case['name']}")
    
    def test_error_handling_validation(self, sample_rules):
        """Test comprehensive error handling"""
        os.environ["LLM_MOCK_MODE"] = "true"
        
        # Test invalid profile types
        with pytest.raises(ValueError, match="Profile must be a dictionary"):
            call_llm("invalid", sample_rules)
        
        # Test invalid rules types
        valid_profile = {
            "size_m2": 100, "seats": 50, "serves_alcohol": False,
            "uses_gas": False, "has_misting": False, "offers_delivery": False
        }
        with pytest.raises(ValueError, match="Matched rules must be a list"):
            call_llm(valid_profile, "invalid")
        
        # Test missing profile fields
        incomplete_profile = {"size_m2": 100}
        with pytest.raises(ValueError, match="Profile missing required field"):
            call_llm(incomplete_profile, sample_rules)
        
        # Test invalid rule structure
        invalid_rules = [{"invalid": "rule"}]
        with pytest.raises(ValueError, match="Rule missing required field"):
            call_llm(valid_profile, invalid_rules)
        
        print("✓ Error handling validation passed")
    
    def test_performance_benchmarks(self, sample_rules, test_profiles):
        """Test performance metrics"""
        import time
        os.environ["LLM_MOCK_MODE"] = "true"
        
        profile = test_profiles[1]["profile"]  # Medium complexity
        matched_rules = match_rules(profile, sample_rules)
        
        # Measure mock mode performance
        start_time = time.time()
        report = call_llm(profile, matched_rules)
        end_time = time.time()
        
        mock_duration = end_time - start_time
        assert mock_duration < 1.0, f"Mock mode should be fast (<1s), took {mock_duration:.3f}s"
        
        # Measure validation performance
        rule_ids = [rule["id"] for rule in matched_rules]
        start_time = time.time()
        is_valid = validate_report_references(report, rule_ids)
        end_time = time.time()
        
        validation_duration = end_time - start_time
        assert validation_duration < 0.1, f"Validation should be fast (<0.1s), took {validation_duration:.3f}s"
        assert is_valid, "Validation should pass"
        
        print(f"✓ Performance benchmarks: Mock={mock_duration:.3f}s, Validation={validation_duration:.3f}s")


def test_integration_summary():
    """Summary test to validate overall integration"""
    print("\n" + "="*60)
    print("LLM INTEGRATION VALIDATION SUMMARY")
    print("="*60)
    
    # Check environment setup
    mock_mode = os.getenv("LLM_MOCK_MODE", "false").lower() == "true"
    api_key_available = bool(os.getenv("OPENAI_API_KEY"))
    
    print(f"Mock Mode: {'✓ Enabled' if mock_mode else '✗ Disabled'}")
    print(f"OpenAI API Key: {'✓ Available' if api_key_available else '✗ Not Available'}")
    
    if not mock_mode and not api_key_available:
        print("⚠️  WARNING: No API key and mock mode disabled - LLM will fallback to mock")
    elif mock_mode:
        print("ℹ️  INFO: Running in mock mode - no API calls will be made")
    else:
        print("ℹ️  INFO: Real LLM mode available - API calls will be made")
    
    print("="*60)


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "-s"])