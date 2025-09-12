#!/usr/bin/env python3
"""
Tests for LLM Report Generation module.
"""

import os
import pytest
import json
from llm import call_llm, validate_report_references, ReportJSON
from matching import match_rules


@pytest.fixture
def sample_profile():
    """Sample business profile for testing."""
    return {
        "size_m2": 120,
        "seats": 80,
        "serves_alcohol": True,
        "uses_gas": True,
        "has_misting": False,
        "offers_delivery": False
    }


@pytest.fixture
def sample_rules():
    """Load actual rules from requirements.json."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "requirements.json")
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_mock_mode_enabled():
    """Test that mock mode can be enabled via environment variable."""
    os.environ["LLM_MOCK_MODE"] = "true"
    
    profile = {
        "size_m2": 50,
        "seats": 30,
        "serves_alcohol": False,
        "uses_gas": False,
        "has_misting": False,
        "offers_delivery": False
    }
    
    rules = [{
        "id": "TEST-RULE-001",
        "title": "Test Rule",
        "desc_en": "Test description",
        "desc_he": "תיאור בדיקה",
        "authority": "Test Authority",
        "priority": "medium"
    }]
    
    report = call_llm(profile, rules)
    
    assert isinstance(report, ReportJSON)
    assert report.total_rules == 1
    assert len(report.sections) > 0
    assert "TEST-RULE-001" in str(report.model_dump())


def test_report_validation_with_valid_rules(sample_profile, sample_rules):
    """Test that report validation passes with valid rule references."""
    os.environ["LLM_MOCK_MODE"] = "true"
    
    # Get some matched rules
    matched_rules = match_rules(sample_profile, sample_rules)[:3]  # Take first 3 matches
    rule_ids = [rule["id"] for rule in matched_rules]
    
    # Generate report
    report = call_llm(sample_profile, matched_rules)
    
    # Validate references
    is_valid = validate_report_references(report, rule_ids)
    assert is_valid, "Report should only reference provided rule IDs"


def test_report_validation_with_invalid_rules():
    """Test that report validation fails with invalid rule references."""
    # Create a mock report with invalid references
    from llm import ReportSection, ReportJSON
    
    invalid_report = ReportJSON(
        summary="Test summary",
        sections=[
            ReportSection(
                title="Test Section",
                content="Test content",
                rule_ids=["INVALID-RULE-ID"],
                priority="high"
            )
        ],
        total_rules=1,
        high_priority_count=1,
        recommendations=["Test recommendation"],
        authorities=["Test Authority"]
    )
    
    valid_rule_ids = ["VALID-RULE-001", "VALID-RULE-002"]
    
    is_valid = validate_report_references(invalid_report, valid_rule_ids)
    assert not is_valid, "Report validation should fail with invalid rule references"


def test_report_structure_completeness(sample_profile, sample_rules):
    """Test that generated reports have all required fields."""
    os.environ["LLM_MOCK_MODE"] = "true"
    
    matched_rules = match_rules(sample_profile, sample_rules)
    report = call_llm(sample_profile, matched_rules)
    
    # Check required fields
    assert report.summary is not None and len(report.summary) > 0
    assert isinstance(report.sections, list) and len(report.sections) > 0
    assert report.total_rules == len(matched_rules)
    assert report.high_priority_count >= 0
    assert isinstance(report.recommendations, list)
    assert isinstance(report.authorities, list)
    
    # Check section structure
    for section in report.sections:
        assert section.title is not None and len(section.title) > 0
        assert section.content is not None and len(section.content) > 0
        assert isinstance(section.rule_ids, list)
        assert section.priority in ["high", "medium", "low"]


def test_empty_rules_handling():
    """Test handling of empty rules list."""
    os.environ["LLM_MOCK_MODE"] = "true"
    
    profile = {
        "size_m2": 50,
        "seats": 30,
        "serves_alcohol": False,
        "uses_gas": False,
        "has_misting": False,
        "offers_delivery": False
    }
    
    report = call_llm(profile, [])
    
    assert isinstance(report, ReportJSON)
    assert report.total_rules == 0
    assert report.high_priority_count == 0


def test_high_priority_count_accuracy(sample_profile, sample_rules):
    """Test that high priority count is accurate."""
    os.environ["LLM_MOCK_MODE"] = "true"
    
    matched_rules = match_rules(sample_profile, sample_rules)
    expected_high_priority = sum(1 for rule in matched_rules if rule["priority"] == "high")
    
    report = call_llm(sample_profile, matched_rules)
    
    assert report.high_priority_count == expected_high_priority


def test_authorities_list_completeness(sample_profile, sample_rules):
    """Test that authorities list includes all relevant authorities."""
    os.environ["LLM_MOCK_MODE"] = "true"
    
    matched_rules = match_rules(sample_profile, sample_rules)
    expected_authorities = list(set(rule["authority"] for rule in matched_rules))
    
    report = call_llm(sample_profile, matched_rules)
    
    assert len(report.authorities) == len(expected_authorities)
    for authority in expected_authorities:
        assert authority in report.authorities


def test_input_validation():
    """Test input validation for call_llm function."""
    os.environ["LLM_MOCK_MODE"] = "true"
    
    # Test invalid profile type
    with pytest.raises(ValueError, match="Profile must be a dictionary"):
        call_llm("invalid_profile", [])
    
    # Test invalid rules type
    with pytest.raises(ValueError, match="Matched rules must be a list"):
        call_llm({}, "invalid_rules")
    
    # Test missing profile fields
    incomplete_profile = {"size_m2": 100}  # Missing required fields
    with pytest.raises(ValueError, match="Profile missing required field"):
        call_llm(incomplete_profile, [])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])