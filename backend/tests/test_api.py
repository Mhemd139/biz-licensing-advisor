#!/usr/bin/env python3
"""
Test cases for FastAPI endpoints.
"""

import json
import os
import sys
from fastapi.testclient import TestClient

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

client = TestClient(app)


def test_health_endpoint():
    """Test /health endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_requirements_endpoint():
    """Test /requirements endpoint loads and returns rules."""
    response = client.get("/requirements")
    assert response.status_code == 200
    
    data = response.json()
    assert "requirements" in data
    assert "count" in data
    assert isinstance(data["requirements"], list)
    assert data["count"] > 0
    
    # Check first rule has required fields
    if data["requirements"]:
        rule = data["requirements"][0]
        required_fields = ["id", "title", "desc_he", "desc_en", "authority", "priority", "source_ref", "triggers"]
        for field in required_fields:
            assert field in rule


def test_assess_steakhouse():
    """Test /assess endpoint with steakhouse profile."""
    profile = {
        "size_m2": 120,
        "seats": 80,
        "serves_alcohol": True,
        "uses_gas": True,
        "delivery": False,
        "has_misting": False
    }
    
    response = client.post("/assess", json=profile)
    assert response.status_code == 200
    
    data = response.json()
    assert "matches" in data
    assert "report" in data
    assert isinstance(data["matches"], list)
    assert len(data["matches"]) > 0
    
    # Should include Police rules (alcohol served)
    matches = data["matches"]
    police_rules = [rule_id for rule_id in matches if "Police" in rule_id]
    assert len(police_rules) > 0


def test_assess_cafe_exempt():
    """Test /assess endpoint with cafe profile (Police exempt)."""
    profile = {
        "size_m2": 50,
        "seats": 100,
        "serves_alcohol": False,
        "uses_gas": False,
        "delivery": False,
        "has_misting": False
    }
    
    response = client.post("/assess", json=profile)
    assert response.status_code == 200
    
    data = response.json()
    matches = data["matches"]
    
    # Should include exemption
    assert "R-Police-Exemption-NoAlcohol-<=200" in matches
    # Should NOT include other Police rules
    police_others = [rule_id for rule_id in matches if "Police" in rule_id and "Exemption" not in rule_id]
    assert len(police_others) == 0


def test_assess_ghost_kitchen():
    """Test /assess endpoint with ghost kitchen (0 seats)."""
    profile = {
        "size_m2": 20,
        "seats": 0,
        "serves_alcohol": False,
        "uses_gas": False,
        "delivery": True,
        "has_misting": False
    }
    
    response = client.post("/assess", json=profile)
    assert response.status_code == 200
    
    data = response.json()
    matches = data["matches"]
    
    # Should include exemption
    assert "R-Police-Exemption-NoAlcohol-<=200" in matches
    # Should have minimal matches (0 seats excludes many MoH rules)
    assert len(matches) <= 3


def test_assess_invalid_data():
    """Test /assess endpoint with invalid data."""
    # Missing required field
    invalid_profile = {
        "size_m2": 100,
        "seats": 50
        # Missing other required fields
    }
    
    response = client.post("/assess", json=invalid_profile)
    assert response.status_code == 422  # FastAPI validation error


def test_assess_large_hall():
    """Test /assess endpoint with large hall (exceeds exemption)."""
    profile = {
        "size_m2": 500,
        "seats": 350,
        "serves_alcohol": False,
        "uses_gas": True,
        "delivery": False,
        "has_misting": False
    }
    
    response = client.post("/assess", json=profile)
    assert response.status_code == 200
    
    data = response.json()
    matches = data["matches"]
    
    # Should NOT include exemption (350 > 200 seats)
    assert "R-Police-Exemption-NoAlcohol-<=200" not in matches
    # Should include Police lighting rule
    assert "R-Police-Exterior-Lighting" in matches


if __name__ == "__main__":
    test_health_endpoint()
    test_requirements_endpoint()
    test_assess_steakhouse()
    test_assess_cafe_exempt()
    test_assess_ghost_kitchen()
    test_assess_invalid_data()
    test_assess_large_hall()
    print("All API tests passed!")