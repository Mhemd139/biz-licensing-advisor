# Matching Algorithm Documentation

## Overview
The matching engine (`backend/matching.py`) implements deterministic rule matching logic that filters Israeli restaurant licensing requirements based on business characteristics.

## Business Profile Schema
The system uses 5 trigger characteristics to profile businesses:

### Numeric Variables
- **`size_m2`**: Restaurant area in square meters
- **`seats`**: Number of customer seats/occupancy

### Boolean Flags
- **`serves_alcohol`**: Whether business serves alcoholic beverages
- **`uses_gas`**: Whether business uses gas equipment
- **`has_misting`**: Whether business uses misting systems/cooling towers
- **`offers_delivery`**: Whether business offers delivery services

## Rule Matching Logic

### 1. Basic Matching (`rule_matches`)
For each rule, the algorithm checks if the business profile satisfies all trigger conditions:

```python
def rule_matches(profile, rule):
    triggers = rule["triggers"]

    # Check numeric bounds (area, seats)
    if "area" in triggers:
        # Must be within min/max bounds

    if "seats" in triggers:
        # Must be within min/max bounds

    # Check boolean flags - ALL must match exactly
    if "flags" in triggers:
        # Profile flags must equal rule requirements
```

### 2. Special Guard Logic (Police Exemption)
The system implements special logic for Israeli Police regulations:

**Rule**: Businesses ≤200 seats + no alcohol are exempt from Police requirements

```python
exemption_matched = any(r["id"] == "R-Police-Exemption-NoAlcohol-<=200" for r in matched)
if exemption_matched:
    # Remove ALL Police rules except the exemption rule itself
    matched = [r for r in matched
              if r["authority"] != "Israel Police" or r["id"] == "R-Police-Exemption-NoAlcohol-<=200"]
```

### 3. Sorting Algorithm
Matched rules are sorted by:

1. **Priority** (high → medium → low)
2. **Threshold Tightness** (smaller ranges first)
3. **Authority** (alphabetical)

```python
return sorted(matched, key=lambda r: (
    priority_order(r["priority"]),      # 0=high, 1=medium, 2=low
    calculate_tightness(r),             # smaller range = lower number
    r["authority"]                      # alphabetical
))
```

## Tightness Calculation
Rules with more specific triggers (smaller ranges) are considered "tighter" and ranked higher:

```python
def calculate_tightness(rule):
    tightness = 0.0

    if "area" in triggers:
        area_range = area_max - area_min
        tightness += area_range

    if "seats" in triggers:
        seat_range = seat_max - seat_min
        tightness += seat_range

    return tightness  # Lower = tighter = higher priority
```

## Example Matching Flow

**Input Profile**:
```json
{
  "size_m2": 120,
  "seats": 80,
  "serves_alcohol": true,
  "uses_gas": true,
  "has_misting": false,
  "offers_delivery": false
}
```

**Matching Steps**:
1. **Filter**: Check all 17 rules against profile triggers
2. **Guard Logic**: Apply Police exemption rules (not applicable - serves alcohol)
3. **Sort**: Order by priority → tightness → authority
4. **Result**: ~10-12 applicable rules for this steakhouse profile

## Authority Coverage
- **Israel Police**: 7 rules (CCTV, alcohol signage, lighting, exemptions)
- **Ministry of Health**: 10 rules (water, hygiene, temperatures, facilities, gas safety, delivery)

## Algorithm Guarantees
- **Deterministic**: Same input always produces same output
- **Complete**: All applicable rules are identified
- **Consistent**: Sorting order is stable and predictable
- **Guard-Safe**: Special exemption logic prevents contradictory requirements

## Implementation Details

### Key Functions

#### `match_rules(profile, rules)`
Main entry point that:
1. Filters all rules against profile
2. Applies special guard logic
3. Sorts results by priority/tightness/authority
4. Returns final matched rule list

#### `rule_matches(profile, rule)`
Core matching logic:
- Checks numeric bounds (area, seats)
- Validates boolean flag requirements
- Returns True if ALL conditions match

#### `calculate_tightness(rule)`
Prioritization helper:
- Sums range sizes for area/seats triggers
- Lower values indicate more specific rules
- Used for consistent sort ordering

### Performance
- **Complexity**: O(n log n) where n = total rules
- **Typical Runtime**: <100ms for 17 rules
- **Memory Usage**: Minimal (rules loaded once)

### Testing
Covered scenarios in `/backend/tests/test_matching.py`:
1. Small restaurant (no alcohol, basic requirements)
2. Large steakhouse (alcohol + gas, full Police requirements)
3. Medium cafe (selective triggers)
4. Exemption edge cases (≤200 seats, no alcohol)
5. Boundary conditions (exact threshold matches)