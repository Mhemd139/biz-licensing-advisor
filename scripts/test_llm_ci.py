#!/usr/bin/env python3
"""
CI test script for LLM functionality in mock mode.
This script verifies that the LLM module works correctly without requiring API keys.
"""

import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from llm import call_llm, validate_report_references
from matching import match_rules


def test_mock_mode_ci():
    """Test LLM functionality in mock mode for CI environment."""
    print("Starting LLM CI tests...")
    
    # Ensure mock mode is enabled
    os.environ["LLM_MOCK_MODE"] = "true"
    
    # Load rules
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'requirements.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        rules = json.load(f)
    
    print(f"Loaded {len(rules)} rules from requirements.json")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Small restaurant without alcohol",
            "profile": {
                "size_m2": 50,
                "seats": 25,
                "serves_alcohol": False,
                "uses_gas": True,
                "has_misting": False,
                "offers_delivery": False
            }
        },
        {
            "name": "Large restaurant with alcohol",
            "profile": {
                "size_m2": 200,
                "seats": 150,
                "serves_alcohol": True,
                "uses_gas": True,
                "has_misting": False,
                "offers_delivery": True
            }
        },
        {
            "name": "Medium restaurant with delivery",
            "profile": {
                "size_m2": 120,
                "seats": 80,
                "serves_alcohol": False,
                "uses_gas": True,
                "has_misting": True,
                "offers_delivery": True
            }
        }
    ]
    
    all_tests_passed = True
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\nTest {i}: {scenario['name']}")
        print(f"Profile: {scenario['profile']}")
        
        try:
            # Match rules
            matched_rules = match_rules(scenario['profile'], rules)
            rule_ids = [rule['id'] for rule in matched_rules]
            print(f"Matched {len(matched_rules)} rules")
            
            # Generate report
            report = call_llm(scenario['profile'], matched_rules)
            print(f"Generated report with {len(report.sections)} sections")
            
            # Validate report structure
            assert report.total_rules == len(matched_rules), f"Total rules mismatch: {report.total_rules} != {len(matched_rules)}"
            assert len(report.sections) > 0, "Report must have at least one section"
            assert len(report.summary) > 0, "Report must have a summary"
            assert isinstance(report.recommendations, list), "Recommendations must be a list"
            assert isinstance(report.authorities, list), "Authorities must be a list"
            
            # Validate rule references
            is_valid = validate_report_references(report, rule_ids)
            assert is_valid, "Report contains invalid rule references"
            
            print(f"[PASS] Test {i} PASSED")
            
        except Exception as e:
            print(f"[FAIL] Test {i} FAILED: {str(e)}")
            all_tests_passed = False
    
    # Test error handling
    print(f"\nTest 4: Error handling")
    try:
        # Test with invalid profile
        try:
            call_llm("invalid", [])
            print("[FAIL] Should have raised ValueError for invalid profile")
            all_tests_passed = False
        except ValueError:
            print("[PASS] Correctly handled invalid profile")
        
        # Test with invalid rules
        valid_profile = {"size_m2": 100, "seats": 50, "serves_alcohol": False, "uses_gas": False, "has_misting": False, "offers_delivery": False}
        try:
            call_llm(valid_profile, "invalid")
            print("[FAIL] Should have raised ValueError for invalid rules")
            all_tests_passed = False
        except ValueError:
            print("[PASS] Correctly handled invalid rules")
            
    except Exception as e:
        print(f"[FAIL] Error handling test failed: {str(e)}")
        all_tests_passed = False
    
    # Summary
    print(f"\n{'='*50}")
    if all_tests_passed:
        print("SUCCESS: ALL TESTS PASSED - LLM mock mode is working correctly!")
        return 0
    else:
        print("ERROR: SOME TESTS FAILED - Check the output above")
        return 1


if __name__ == "__main__":
    exit_code = test_mock_mode_ci()
    sys.exit(exit_code)