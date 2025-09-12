#!/usr/bin/env python3
"""
Test cases for the matching engine.
"""

import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matching import match_rules


def get_ids(rules):
    """Extract rule IDs from rules list."""
    return [rule["id"] for rule in rules]


def load_rules():
    """Load rules from requirements.json."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "requirements.json")
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_cafe_exempt():
    """Cafe with no alcohol should trigger Police exemption."""
    rules = load_rules()
    profile = {
        "size_m2": 50,
        "seats": 100,
        "serves_alcohol": False,
        "uses_gas": False,
        "has_misting": False,
        "offers_delivery": False
    }
    
    matches = match_rules(profile, rules)
    ids = get_ids(matches)
    
    # Should include exemption rule
    assert "R-Police-Exemption-NoAlcohol-<=200" in ids
    # Should NOT include other Police rules
    assert "R-Police-CCTV-Resolution" not in ids
    assert "R-Police-CCTV-Placement" not in ids
    assert "R-Police-Alcohol-Minors-Sign" not in ids
    # Should include MoH rules
    assert "R-MoH-Food-Temps" in ids


def test_steakhouse():
    """Steakhouse with alcohol should include Police rules."""
    rules = load_rules()
    profile = {
        "size_m2": 120,
        "seats": 80,
        "serves_alcohol": True,
        "uses_gas": True,
        "has_misting": False,
        "offers_delivery": False
    }
    
    matches = match_rules(profile, rules)
    ids = get_ids(matches)
    
    # Should include Police CCTV and alcohol rules
    assert "R-Police-CCTV-Resolution" in ids
    assert "R-Police-CCTV-Placement" in ids
    assert "R-Police-Alcohol-Minors-Sign" in ids
    # Should include MoH rules
    assert "R-MoH-Food-Temps" in ids
    assert "R-MoH-Sewage-Fat-Separator" in ids
    # Should include Fire rules (uses_gas=True)
    assert "R-Fire-Gas-Compliance" in ids
    assert "R-Fire-Gas-Shutoff" in ids


def test_ghost_kitchen():
    """Ghost kitchen (delivery only) should be exempt from Police."""
    rules = load_rules()
    profile = {
        "size_m2": 20,
        "seats": 0,
        "serves_alcohol": False,
        "uses_gas": False,
        "has_misting": False,
        "offers_delivery": True
    }
    
    matches = match_rules(profile, rules)
    ids = get_ids(matches)
    
    # Should include exemption (0 seats ≤ 200, no alcohol)
    assert "R-Police-Exemption-NoAlcohol-<=200" in ids
    # Should NOT include other Police rules
    assert "R-Police-CCTV-Resolution" not in ids
    # Should NOT include MoH rules requiring seats ≥ 1
    assert "R-MoH-Food-Temps" not in ids
    # Ghost kitchen with 0 seats has minimal requirements
    # Should include delivery rules (offers_delivery=True)
    assert "R-MoH-Delivery-Temperature-Control" in ids
    assert "R-MoH-Delivery-Containers" in ids


def test_large_hall():
    """Large hall exceeds exemption threshold."""
    rules = load_rules()
    profile = {
        "size_m2": 500,
        "seats": 350,
        "serves_alcohol": False,
        "uses_gas": True,
        "has_misting": False,
        "offers_delivery": False
    }
    
    matches = match_rules(profile, rules)
    ids = get_ids(matches)
    
    # Exemption should NOT apply (350 > 200 seats)
    assert "R-Police-Exemption-NoAlcohol-<=200" not in ids
    # Should include Police lighting rule (general)
    assert "R-Police-Exterior-Lighting" in ids
    # Should include MoH rules
    assert "R-MoH-Food-Temps" in ids
    # Should include Fire rules (uses_gas=True) 
    assert "R-Fire-Gas-Compliance" in ids


def test_edge_thresholds():
    """Edge case: exactly 200 seats, no alcohol, has misting."""
    rules = load_rules()
    profile = {
        "size_m2": 200,
        "seats": 200,
        "serves_alcohol": False,
        "uses_gas": False,
        "has_misting": True,
        "offers_delivery": False
    }
    
    matches = match_rules(profile, rules)
    ids = get_ids(matches)
    
    # Should trigger exemption (200 ≤ 200, no alcohol)
    assert "R-Police-Exemption-NoAlcohol-<=200" in ids
    # Should NOT include other Police rules
    assert "R-Police-CCTV-Resolution" not in ids
    # Should include MoH Legionella rule (has_misting=True)
    assert "R-MoH-Legionella-Misting" in ids
    # Should include general MoH rules
    assert "R-MoH-Food-Temps" in ids


if __name__ == "__main__":
    test_cafe_exempt()
    test_steakhouse()
    test_ghost_kitchen()
    test_large_hall()
    test_edge_thresholds()
    print("All tests passed!")