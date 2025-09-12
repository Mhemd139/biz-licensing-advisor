#!/usr/bin/env python3
"""
Business licensing rule matching engine.
"""

import json
import os
from typing import Dict, List, Any


def match_rules(profile: Dict[str, Any], rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Match rules based on profile criteria.
    
    Args:
        profile: Business profile with size_m2, seats, and flags
        rules: List of licensing rules
        
    Returns:
        Sorted list of matching rules
    """
    matched = []
    
    for rule in rules:
        if rule_matches(profile, rule):
            matched.append(rule)
    
    # Apply special guard logic for Police exemption
    exemption_matched = any(r["id"] == "R-Police-Exemption-NoAlcohol-<=200" for r in matched)
    if exemption_matched:
        matched = [r for r in matched 
                  if r["authority"] != "Israel Police" or r["id"] == "R-Police-Exemption-NoAlcohol-<=200"]
    
    # Sort by priority, threshold tightness, authority
    return sorted(matched, key=lambda r: (
        priority_order(r["priority"]),
        calculate_tightness(r),
        r["authority"]
    ))


def rule_matches(profile: Dict[str, Any], rule: Dict[str, Any]) -> bool:
    """Check if a single rule matches the profile."""
    triggers = rule["triggers"]
    
    # Check area bounds
    if "area" in triggers:
        area_bounds = triggers["area"]
        size = profile.get("size_m2", 0)
        if "min" in area_bounds and size < area_bounds["min"]:
            return False
        if "max" in area_bounds and size > area_bounds["max"]:
            return False
    
    # Check seats bounds  
    if "seats" in triggers:
        seat_bounds = triggers["seats"]
        seats = profile.get("seats", 0)
        if "min" in seat_bounds and seats < seat_bounds["min"]:
            return False
        if "max" in seat_bounds and seats > seat_bounds["max"]:
            return False
    
    # Check flags - all rule flags must match profile
    if "flags" in triggers:
        rule_flags = triggers["flags"]
        for flag_name, required_value in rule_flags.items():
            profile_value = profile.get(flag_name, False)
            if profile_value != required_value:
                return False
    
    return True


def priority_order(priority: str) -> int:
    """Convert priority to sort order (lower number = higher priority)."""
    return {"high": 0, "medium": 1, "low": 2}.get(priority, 3)


def calculate_tightness(rule: Dict[str, Any]) -> float:
    """Calculate threshold tightness (smaller ranges = tighter = lower number)."""
    triggers = rule["triggers"]
    tightness = 0.0
    
    if "area" in triggers:
        area = triggers["area"]
        area_min = area.get("min", 0)
        area_max = area.get("max", 1000)  # Default max if not specified
        tightness += (area_max - area_min)
    
    if "seats" in triggers:
        seats = triggers["seats"]
        seat_min = seats.get("min", 0)
        seat_max = seats.get("max", 500)  # Default max if not specified
        tightness += (seat_max - seat_min)
    
    return tightness


if __name__ == "__main__":
    # Load requirements
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "requirements.json")
    with open(data_path, 'r', encoding='utf-8') as f:
        rules = json.load(f)
    
    # Sample profile
    profile = {
        "size_m2": 120,
        "seats": 80,
        "serves_alcohol": True,
        "uses_gas": True,
        "has_misting": False,
        "offers_delivery": False
    }
    
    # Match rules
    matches = match_rules(profile, rules)
    
    print(f"Profile: {profile}")
    print(f"\nMatched {len(matches)} rules:")
    for i, rule in enumerate(matches, 1):
        print(f"{i:2d}. {rule['id']} - {rule['title']} ({rule['priority']})")