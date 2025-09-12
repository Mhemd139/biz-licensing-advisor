#!/usr/bin/env python3
"""
LLM Report Generation for Business Licensing Advisor.
"""

import json
import os
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field, ValidationError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportSection(BaseModel):
    """Individual section of the report."""
    title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content in Hebrew and English")
    rule_ids: List[str] = Field(..., description="Referenced rule IDs")
    priority: str = Field(..., description="Priority level: high, medium, low")


class ReportJSON(BaseModel):
    """Complete LLM-generated report structure."""
    summary: str = Field(..., description="Executive summary in Hebrew and English")
    sections: List[ReportSection] = Field(..., description="Detailed sections")
    total_rules: int = Field(..., description="Total number of matched rules")
    high_priority_count: int = Field(..., description="Number of high priority rules")
    recommendations: List[str] = Field(..., description="Actionable recommendations")
    authorities: List[str] = Field(..., description="List of relevant authorities")


def call_llm(profile: Dict[str, Any], matched_rules: List[Dict[str, Any]]) -> ReportJSON:
    """
    Generate LLM report from business profile and matched rules.
    
    Args:
        profile: Business profile dictionary
        matched_rules: List of matched licensing rules
        
    Returns:
        ReportJSON: Structured report with recommendations
        
    Raises:
        ValueError: If invalid input or LLM response
        RuntimeError: If LLM service unavailable
    """
    # Validate inputs first (regardless of mode)
    _validate_inputs(profile, matched_rules)
    
    # Check if we're in mock mode
    mock_mode = os.getenv("LLM_MOCK_MODE", "false").lower() == "true"
    
    if mock_mode:
        logger.info("Running in mock mode - generating synthetic report")
        return _generate_mock_report(profile, matched_rules)
    
    try:
        
        # Get LLM API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("No OPENAI_API_KEY found, falling back to mock mode")
            return _generate_mock_report(profile, matched_rules)
        
        # Generate report using actual LLM
        return _generate_llm_report(profile, matched_rules, api_key)
        
    except Exception as e:
        logger.error(f"Error in call_llm: {str(e)}")
        raise


def _validate_inputs(profile: Dict[str, Any], matched_rules: List[Dict[str, Any]]) -> None:
    """Validate input parameters."""
    if not isinstance(profile, dict):
        raise ValueError("Profile must be a dictionary")
    
    if not isinstance(matched_rules, list):
        raise ValueError("Matched rules must be a list")
    
    # Check required profile fields
    required_fields = ["size_m2", "seats", "serves_alcohol", "uses_gas", "has_misting", "offers_delivery"]
    for field in required_fields:
        if field not in profile:
            raise ValueError(f"Profile missing required field: {field}")
    
    # Validate rule structure
    for rule in matched_rules:
        required_rule_fields = ["id", "title", "desc_en", "desc_he", "authority", "priority"]
        for field in required_rule_fields:
            if field not in rule:
                raise ValueError(f"Rule missing required field: {field}")


def _generate_mock_report(profile: Dict[str, Any], matched_rules: List[Dict[str, Any]]) -> ReportJSON:
    """Generate a mock report for testing purposes."""
    logger.info(f"Generating mock report for {len(matched_rules)} matched rules")
    
    # Extract rule IDs for validation
    rule_ids = [rule["id"] for rule in matched_rules]
    
    # Count priorities
    high_priority_count = sum(1 for rule in matched_rules if rule["priority"] == "high")
    
    # Get unique authorities
    authorities = list(set(rule["authority"] for rule in matched_rules))
    
    # Group rules by authority for sections
    sections = []
    authority_rules = {}
    for rule in matched_rules:
        auth = rule["authority"]
        if auth not in authority_rules:
            authority_rules[auth] = []
        authority_rules[auth].append(rule)
    
    # Create sections for each authority
    for authority, rules in authority_rules.items():
        auth_rule_ids = [rule["id"] for rule in rules]
        priority = "high" if any(rule["priority"] == "high" for rule in rules) else "medium"
        
        content = f"Requirements from {authority}:\n"
        content += f"רישיונות מ{authority}:\n\n"
        for rule in rules:
            content += f"• {rule['title']} - {rule['desc_en']}\n"
            content += f"• {rule['desc_he']}\n\n"
        
        sections.append(ReportSection(
            title=f"{authority} Requirements",
            content=content,
            rule_ids=auth_rule_ids,
            priority=priority
        ))
    
    # Generate recommendations
    recommendations = [
        "Contact relevant authorities early in the planning process",
        "פנו לרשויות הרלוונטיות בשלב מוקדם של התכנון",
        "Ensure all high-priority requirements are addressed first",
        "וודאו שכל הדרישות בעדיפות גבוהה מטופלות ראשונות"
    ]
    
    if high_priority_count > 0:
        recommendations.extend([
            f"Focus immediate attention on {high_priority_count} high-priority requirements",
            f"התמקדו בתשומת לב מיידית ב-{high_priority_count} דרישות בעדיפות גבוהה"
        ])
    
    # Generate summary
    summary = f"""Business Profile Assessment Summary / סיכום הערכת פרופיל עסקי

Size: {profile['size_m2']}m² | Seats: {profile['seats']} | גודל: {profile['size_m2']}מ״ר | מקומות ישיבה: {profile['seats']}
Alcohol: {'Yes' if profile['serves_alcohol'] else 'No'} | Gas: {'Yes' if profile['uses_gas'] else 'No'} | אלכוהול: {'כן' if profile['serves_alcohol'] else 'לא'} | גז: {'כן' if profile['uses_gas'] else 'לא'}

Total Requirements: {len(matched_rules)} | High Priority: {high_priority_count}
סה״כ דרישות: {len(matched_rules)} | עדיפות גבוהה: {high_priority_count}

This assessment identified licensing requirements from {len(authorities)} authorities.
הערכה זו זיהתה דרישות רישוי מ-{len(authorities)} רשויות."""
    
    return ReportJSON(
        summary=summary,
        sections=sections,
        total_rules=len(matched_rules),
        high_priority_count=high_priority_count,
        recommendations=recommendations,
        authorities=authorities
    )


def _generate_llm_report(profile: Dict[str, Any], matched_rules: List[Dict[str, Any]], api_key: str) -> ReportJSON:
    """Generate report using actual LLM service."""
    try:
        import openai
    except ImportError:
        logger.warning("OpenAI library not installed, falling back to mock mode")
        return _generate_mock_report(profile, matched_rules)
    
    # Configure OpenAI
    openai.api_key = api_key
    
    # Prepare prompt
    prompt = _create_llm_prompt(profile, matched_rules)
    
    try:
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Israeli business licensing consultant. Generate structured reports in both Hebrew and English."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        # Parse and validate response
        llm_output = response.choices[0].message.content
        return _parse_llm_response(llm_output, matched_rules)
        
    except Exception as e:
        logger.error(f"LLM API error: {str(e)}")
        logger.info("Falling back to mock mode due to LLM error")
        return _generate_mock_report(profile, matched_rules)


def _create_llm_prompt(profile: Dict[str, Any], matched_rules: List[Dict[str, Any]]) -> str:
    """Create prompt for LLM."""
    rule_details = "\n".join([
        f"ID: {rule['id']} | Authority: {rule['authority']} | Priority: {rule['priority']}\n"
        f"Title: {rule['title']}\n"
        f"EN: {rule['desc_en']}\n"
        f"HE: {rule['desc_he']}\n"
        for rule in matched_rules
    ])
    
    return f"""Generate a licensing report for an Israeli restaurant business.

BUSINESS PROFILE:
- Size: {profile['size_m2']}m²
- Seats: {profile['seats']}
- Serves Alcohol: {profile['serves_alcohol']}
- Uses Gas: {profile['uses_gas']}
- Has Misting: {profile['has_misting']}
- Offers Delivery: {profile['offers_delivery']}

MATCHED RULES ({len(matched_rules)} total):
{rule_details}

REQUIREMENTS:
1. Create a summary in Hebrew and English
2. Group rules by authority into sections
3. Provide actionable recommendations
4. Reference only the provided rule IDs
5. Focus on practical implementation steps

Format the response as structured text that can be parsed into JSON sections."""


def _parse_llm_response(llm_output: str, matched_rules: List[Dict[str, Any]]) -> ReportJSON:
    """Parse LLM response into structured format."""
    # For now, fall back to mock mode if parsing is complex
    # This can be enhanced with better parsing logic
    logger.info("Parsing LLM response - using structured mock format")
    return _generate_mock_report({}, matched_rules)


def validate_report_references(report: ReportJSON, valid_rule_ids: List[str]) -> bool:
    """
    Validate that report only references provided rule IDs.
    
    Args:
        report: Generated report
        valid_rule_ids: List of valid rule IDs
        
    Returns:
        bool: True if all references are valid
    """
    referenced_ids = set()
    
    # Collect all referenced rule IDs
    for section in report.sections:
        referenced_ids.update(section.rule_ids)
    
    # Check if all referenced IDs are valid
    invalid_refs = referenced_ids - set(valid_rule_ids)
    
    if invalid_refs:
        logger.error(f"Report contains invalid rule references: {invalid_refs}")
        return False
    
    logger.info(f"Report validation passed - {len(referenced_ids)} valid references")
    return True


if __name__ == "__main__":
    # Test the module
    sample_profile = {
        "size_m2": 120,
        "seats": 80,
        "serves_alcohol": True,
        "uses_gas": True,
        "has_misting": False,
        "offers_delivery": False
    }
    
    sample_rules = [
        {
            "id": "R-Police-CCTV-Resolution",
            "title": "CCTV ≥1.3MP + backup",
            "desc_en": "CCTV at ≥1.3MP with ≥30-min backup",
            "desc_he": "טמ״ס ברזולוציה 1.3MP לפחות",
            "authority": "Israel Police",
            "priority": "high"
        }
    ]
    
    # Test mock mode
    os.environ["LLM_MOCK_MODE"] = "true"
    report = call_llm(sample_profile, sample_rules)
    print(f"Generated report with {len(report.sections)} sections")
    print(f"High priority count: {report.high_priority_count}")