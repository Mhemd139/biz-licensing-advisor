#!/usr/bin/env python3
"""
Complete LLM Function Tests - Tests all LLM functionality with API integration
"""

import os
import sys
import pytest
import json
import time
from dotenv import load_dotenv

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

from llm import call_llm, validate_report_references, ReportJSON, ReportSection
from matching import match_rules


@pytest.fixture
def sample_rules():
    """Load actual rules from requirements.json"""
    data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "requirements.json")
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def test_profiles():
    """Various business profiles for comprehensive testing"""
    return [
        {
            "name": "Small cafe no alcohol",
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


# Core API Testing Functions

def test_api_key_availability():
    """Test if OpenAI API key is properly loaded"""
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None, "OPENAI_API_KEY must be set in environment"
    assert api_key.startswith("sk-"), "API key should start with 'sk-'"
    assert len(api_key) > 20, "API key seems too short"
    print(f"[SUCCESS] API key loaded: {api_key[:10]}...{api_key[-4:]}")


def test_api_key_validation():
    """Test API key validation"""
    # Temporarily remove API key
    original_key = os.getenv("OPENAI_API_KEY")
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
    os.environ["LLM_MOCK_MODE"] = "false"
    
    profile = {"size_m2": 100, "seats": 50, "serves_alcohol": False, "uses_gas": False, "has_misting": False, "offers_delivery": False}
    
    # Should raise RuntimeError when no API key
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY is required"):
        call_llm(profile, [])
    
    # Restore API key
    if original_key:
        os.environ["OPENAI_API_KEY"] = original_key
        
    print("[PASS] API key validation test passed")


def test_real_api_mode_functionality(sample_rules, test_profiles):
    """Test real OpenAI API integration"""
    # Enable real API mode
    os.environ["LLM_MOCK_MODE"] = "false"
    
    # Test with medium complexity profile to avoid excessive API usage
    test_case = test_profiles[1]  # Medium restaurant
    profile = test_case["profile"]
    name = test_case["name"]
    
    matched_rules = match_rules(profile, sample_rules)
    rule_ids = [rule["id"] for rule in matched_rules]
    
    print(f"Testing real API with {name}: {len(matched_rules)} rules")
    
    start_time = time.time()
    report = call_llm(profile, matched_rules)
    end_time = time.time()
    
    # Validate structure
    assert isinstance(report, ReportJSON), "Real API should return ReportJSON"
    assert report.total_rules == len(matched_rules), "Total rules should match"
    assert len(report.sections) > 0, "Should have sections"
    assert len(report.summary) > 0, "Should have summary"
    
    # Validate references
    is_valid = validate_report_references(report, rule_ids)
    assert is_valid, "Real API report should have valid references"
    
    duration = end_time - start_time
    print(f"[PASS] Real API test passed in {duration:.2f}s")
    print(f"  Generated {len(report.sections)} sections")
    print(f"  High priority rules: {report.high_priority_count}")
    print(f"  Authorities: {', '.join(report.authorities)}")


def test_report_quality_validation(sample_rules, test_profiles):
    """Test comprehensive report quality with API"""
    os.environ["LLM_MOCK_MODE"] = "false"
    
    # Test with small profile to minimize API usage
    profile = test_profiles[0]["profile"]
    matched_rules = match_rules(profile, sample_rules)
    
    report = call_llm(profile, matched_rules)
    
    # Content quality tests
    assert "business" in report.summary.lower() or "עסק" in report.summary, "Should contain business context"
    assert len(report.recommendations) > 0, "Should provide recommendations"
    
    # Authority coverage
    expected_authorities = list(set(rule["authority"] for rule in matched_rules))
    assert len(report.authorities) == len(expected_authorities), "Should cover all authorities"
    
    # Priority accuracy
    expected_high = sum(1 for rule in matched_rules if rule["priority"] == "high")
    assert report.high_priority_count == expected_high, "High priority count should be accurate"
    
    print("[PASS] Report quality validation passed")


def test_api_performance_benchmarks(sample_rules, test_profiles):
    """Test API response times and performance"""
    os.environ["LLM_MOCK_MODE"] = "false"
    
    profile = test_profiles[0]["profile"]  # Small cafe for speed
    matched_rules = match_rules(profile, sample_rules)
    
    # Performance test
    start_time = time.time()
    report = call_llm(profile, matched_rules)
    end_time = time.time()
    
    duration = end_time - start_time
    assert duration < 30.0, f"API call should complete within 30s, took {duration:.2f}s"
    
    print(f"[PASS] API Performance: {duration:.2f}s for {len(matched_rules)} rules")
    
    # Validate the report was properly generated
    assert isinstance(report, ReportJSON), "Should return valid report"
    assert len(report.sections) > 0, "Should generate content"


def test_api_error_handling(sample_rules, test_profiles):
    """Test API error handling - should fail properly without fallback"""
    # Test with invalid API key
    original_key = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "sk-invalid_key_for_testing"
    os.environ["LLM_MOCK_MODE"] = "false"
    
    profile = test_profiles[0]["profile"]
    matched_rules = match_rules(profile, sample_rules)
    
    # Should raise RuntimeError when API fails
    with pytest.raises(RuntimeError, match="LLM API integration failed"):
        call_llm(profile, matched_rules)
    
    # Restore original key
    if original_key:
        os.environ["OPENAI_API_KEY"] = original_key
    
    print("[PASS] API error handling test passed - properly fails without fallback")


def test_input_validation_with_api(sample_rules):
    """Test input validation works with API integration"""
    os.environ["LLM_MOCK_MODE"] = "false"
    
    # Test invalid profile
    with pytest.raises(ValueError, match="Profile must be a dictionary"):
        call_llm("invalid_profile", sample_rules[:2])
    
    # Test invalid rules
    valid_profile = {
        "size_m2": 100, "seats": 50, "serves_alcohol": False,
        "uses_gas": False, "has_misting": False, "offers_delivery": False
    }
    with pytest.raises(ValueError, match="Matched rules must be a list"):
        call_llm(valid_profile, "invalid_rules")
    
    # Test missing profile fields
    incomplete_profile = {"size_m2": 100}
    with pytest.raises(ValueError, match="Profile missing required field"):
        call_llm(incomplete_profile, sample_rules[:2])
    
    print("[PASS] Input validation tests passed")


def test_api_response_structure_consistency(sample_rules, test_profiles):
    """Test that API responses have consistent structure"""
    os.environ["LLM_MOCK_MODE"] = "false"
    
    # Test multiple profiles for consistency
    results = []
    for test_case in test_profiles[:2]:  # Test first 2 to save API calls
        profile = test_case["profile"]
        matched_rules = match_rules(profile, sample_rules)
        
        report = call_llm(profile, matched_rules)
        
        results.append({
            "name": test_case["name"],
            "total_rules": report.total_rules,
            "expected_rules": len(matched_rules),
            "high_priority": report.high_priority_count,
            "sections": len(report.sections),
            "authorities": len(report.authorities)
        })
        
        # Validate structure consistency
        assert report.total_rules == len(matched_rules), f"Rule count mismatch for {test_case['name']}"
        assert len(report.sections) > 0, f"Should have sections for {test_case['name']}"
        assert len(report.authorities) > 0, f"Should have authorities for {test_case['name']}"
    
    print("[PASS] API response structure consistency test passed")
    for result in results:
        print(f"  {result['name']}: {result['total_rules']} rules -> {result['sections']} sections")


def test_comprehensive_api_scenarios(sample_rules, test_profiles):
    """Test comprehensive scenarios with real API"""
    os.environ["LLM_MOCK_MODE"] = "false"
    
    results = []
    
    for test_case in test_profiles:
        profile = test_case["profile"]
        name = test_case["name"]
        
        matched_rules = match_rules(profile, sample_rules)
        rule_ids = [rule["id"] for rule in matched_rules]
        
        start_time = time.time()
        report = call_llm(profile, matched_rules)
        duration = time.time() - start_time
        
        # Validate each scenario
        assert isinstance(report, ReportJSON), f"Invalid report type for {name}"
        assert validate_report_references(report, rule_ids), f"Invalid references for {name}"
        
        results.append({
            "name": name,
            "rules_count": len(matched_rules),
            "sections_count": len(report.sections), 
            "duration": duration
        })
        
        print(f"[PASS] {name}: {len(matched_rules)} rules -> {len(report.sections)} sections ({duration:.2f}s)")
    
    # Summary
    total_duration = sum(r["duration"] for r in results)
    print(f"[PASS] All API scenarios completed in {total_duration:.2f}s total")


# Test execution summary
def test_summary():
    """Print test execution summary"""
    print("\n" + "="*60)
    print("LLM API TESTING SUMMARY")
    print("="*60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    mock_mode = os.getenv("LLM_MOCK_MODE", "false").lower() == "true"
    
    print(f"API Key Available: {'Yes' if api_key else 'No'}")
    print(f"Mock Mode: {'Disabled - Pure API Mode' if not mock_mode else 'Should be disabled'}")
    
    if api_key and not mock_mode:
        print("[SUCCESS] Pure API testing mode - no fallbacks")
    elif api_key and mock_mode:
        print("[WARNING] Mock mode enabled but tests expect API mode")
    else:
        print("[ERROR] No API key - tests will fail")
    
    print("="*60)


if __name__ == "__main__":
    # Load environment and run tests
    load_dotenv()
    pytest.main([__file__, "-v", "-s"])