# Data Schema Documentation

## Requirements Data Structure

### File Location
`/data/requirements.json` - Single source of truth for licensing rules

### Schema Overview
```json
[
  {
    "id": "string",
    "title": "string",
    "desc_he": "string",
    "desc_en": "string",
    "authority": "string",
    "priority": "string",
    "source_ref": "string",
    "triggers": {
      "area": { "min": number, "max": number },
      "seats": { "min": number, "max": number },
      "flags": { "flag_name": boolean }
    }
  }
]
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✅ | Unique identifier (e.g., "R-Police-CCTV-Resolution") |
| `title` | string | ✅ | Short English rule description |
| `desc_he` | string | ✅ | Hebrew description from source document |
| `desc_en` | string | ✅ | English translation/explanation |
| `authority` | string | ✅ | Regulatory body ("Israel Police", "Ministry of Health") |
| `priority` | string | ✅ | Rule importance ("high", "medium", "low") |
| `source_ref` | string | ✅ | PDF page/section reference |
| `triggers` | object | ✅ | Conditions that trigger this rule |

### Trigger Schema

#### Numeric Bounds
```json
{
  "area": { "min": 50, "max": 200 },  // Square meters
  "seats": { "min": 10, "max": 100 }  // Number of seats
}
```

#### Boolean Flags
```json
{
  "flags": {
    "serves_alcohol": true,
    "uses_gas": false,
    "has_misting": true,
    "offers_delivery": false
  }
}
```

## Business Profile Schema

### Input Format
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

### Field Definitions
| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `size_m2` | integer | 1-1000+ | Restaurant area in square meters |
| `seats` | integer | 1-500+ | Number of customer seats/occupancy |
| `serves_alcohol` | boolean | true/false | Serves alcoholic beverages |
| `uses_gas` | boolean | true/false | Uses gas equipment/cooking |
| `has_misting` | boolean | true/false | Uses misting/cooling systems |
| `offers_delivery` | boolean | true/false | Offers delivery services |

## Report Schema

### LLM Generated Report
```json
{
  "summary": "string",
  "police_requirements": ["string"],
  "health_requirements": ["string"],
  "recommendations": ["string"]
}
```

## Sample Data

### Example Rule
```json
{
  "id": "R-Police-CCTV-Resolution",
  "title": "CCTV ≥1.3MP + backup",
  "desc_he": "טמ\"ס ברזולוציה 1.3MP לפחות, גיבוי חצי שעה להקלטה ולספקי כוח.",
  "desc_en": "CCTV at ≥1.3MP with ≥30-min backup for recorder and camera power.",
  "authority": "Israel Police",
  "priority": "high",
  "source_ref": "§3.3.1(1,3)",
  "triggers": {
    "flags": { "serves_alcohol": true }
  }
}
```

### Example Business Profile
```json
{
  "size_m2": 85,
  "seats": 45,
  "serves_alcohol": false,
  "uses_gas": true,
  "has_misting": false,
  "offers_delivery": true
}
```

## Data Validation

### JSON Schema Validation
- All required fields must be present
- Numeric values must be positive integers
- Boolean flags must be true/false
- Unique rule IDs across all entries
- Valid authority names from approved list

### Business Logic Validation
- Police exemption rule: ≤200 seats + no alcohol = exempt from Police rules
- Rule references in reports must match provided rule IDs
- Trigger conditions must be logically consistent

## Authorities Coverage

### Israel Police (7 rules)
- CCTV requirements (resolution, placement, retention)
- Alcohol signage and age verification
- Lighting requirements
- Exemption conditions

### Ministry of Health (10 rules)
- Water quality and testing
- Food safety and hygiene
- Temperature monitoring
- Gas equipment safety
- Delivery service requirements
- Misting system regulations

## Database Design Notes

### Storage Format
- **Current**: JSON files for simplicity and version control
- **Future**: Could migrate to PostgreSQL/SQLite for complex queries
- **Backup**: Git version control tracks all rule changes

### Performance
- 17 rules total - small enough for in-memory processing
- No database overhead for matching operations
- Fast startup and deployment