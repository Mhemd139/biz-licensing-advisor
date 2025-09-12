#!/usr/bin/env python3
"""
ETL script for business licensing requirements.
Validates and processes requirements.json from PDF source.
"""

import json
import os
from typing import Dict, List, Any
import pdfplumber

def extract_rules_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """Extract rules from a PDF file. Placeholder implementation."""
    """Attempt to parse rules directly from the Hebrew PDF."""
    rules = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            # Example: naive filtering for "סעיף" or "דרישות"
            for line in text.splitlines():
                if "דרישות" in line or "סעיף" in line:
                    rules.append({
                        "id": f"PDF-{page_number}-{len(rules)+1}",
                        "title": line.strip()[:60],
                        "desc_he": line.strip(),
                        "desc_en": "TODO: manual translation",
                        "authority": "TODO",
                        "priority": "medium",
                        "source_ref": f"PDF p.{page_number}",
                        "triggers": {}
                    })
    return rules
def validate_rule_schema(rule: Dict[str, Any]) -> bool:
    """Validate a single rule against required schema."""
    required_fields = ["id", "title", "desc_he", "desc_en", "authority", "priority", "source_ref", "triggers"]
    
    for field in required_fields:
        if field not in rule:
            print(f"Missing required field '{field}' in rule {rule.get('id', 'unknown')}")
            return False
    
    # Validate priority values
    if rule["priority"] not in ["high", "medium", "low"]:
        print(f"Invalid priority '{rule['priority']}' in rule {rule['id']}")
        return False
    
    # Validate triggers structure
    if not isinstance(rule["triggers"], dict):
        print(f"Invalid triggers structure in rule {rule['id']}")
        return False
    
    return True

def load_requirements() -> List[Dict[str, Any]]:
    """Load and validate requirements.json."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "requirements.json")
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            requirements = json.load(f)
    except FileNotFoundError:
        print(f"Error: {data_path} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in requirements.json: {e}")
        return []
    
    if not isinstance(requirements, list):
        print("Error: requirements.json must contain a list of rules")
        return []
    
    return requirements

def main():
    """Main validation and processing function."""
    print("🔍 Loading requirements.json...")
    requirements = load_requirements()
    
    if not requirements:
        print("❌ No requirements loaded")
        return 1
    
    print(f"📋 Found {len(requirements)} rules")
    
    valid_count = 0
    authorities = set()
    
    for i, rule in enumerate(requirements):
        print(f"  Rule {i+1}: {rule.get('id', 'unknown')}")
        
        if validate_rule_schema(rule):
            valid_count += 1
            authorities.add(rule["authority"])
        else:
            print(f"    ❌ Validation failed")
            continue
            
        print(f"    ✅ Valid - {rule['title']}")
        print(f"       Source: {rule['source_ref']}")
    
    print(f"\n📊 Summary:")
    print(f"   Total rules: {len(requirements)}")
    print(f"   Valid rules: {valid_count}")
    print(f"   Authorities: {', '.join(sorted(authorities))}")
    
    if valid_count == len(requirements):
        print("✅ All rules passed validation")
        return 0
    else:
        print(f"❌ {len(requirements) - valid_count} rules failed validation")
        return 1

if __name__ == "__main__":
    exit(main())