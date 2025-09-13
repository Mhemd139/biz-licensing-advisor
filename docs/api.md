# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the API server is running.

**Response:**
```json
{
  "status": "ok"
}
```

### 2. Get All Requirements
**GET** `/requirements`

Retrieve all licensing requirements from the database.

**Response:**
```json
{
  "requirements": [
    {
      "id": "R-Police-CCTV-Resolution",
      "title": "CCTV ≥1.3MP + backup",
      "desc_he": "טמ\"ס ברזולוציה 1.3MP לפחות...",
      "desc_en": "CCTV at ≥1.3MP with ≥30-min backup...",
      "authority": "Israel Police",
      "priority": "high",
      "source_ref": "§3.3.1(1,3)",
      "triggers": {
        "flags": { "serves_alcohol": true }
      }
    }
  ],
  "count": 17
}
```

### 3. Assess Business Profile
**POST** `/assess`

Submit business profile and receive personalized licensing report.

**Request Body:**
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

**Response:**
```json
{
  "matches": [
    "R-Police-CCTV-Resolution",
    "R-Police-CCTV-Placement",
    "R-MoH-Water-Quality",
    "R-MoH-Gas-Safety-Ventilation"
  ],
  "report": {
    "summary": "Your restaurant requires licensing from 2 authorities...",
    "police_requirements": [
      "Install CCTV system with ≥1.3MP resolution",
      "Place cameras at entrance and facade"
    ],
    "health_requirements": [
      "Ensure water quality testing",
      "Install proper gas ventilation"
    ],
    "recommendations": [
      "Start with Police licensing first",
      "Schedule health inspection after setup",
      "Budget for CCTV system installation"
    ]
  }
}
```

## Business Profile Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `size_m2` | integer | ✅ | Restaurant area in square meters |
| `seats` | integer | ✅ | Number of customer seats/occupancy |
| `serves_alcohol` | boolean | ✅ | Whether business serves alcoholic beverages |
| `uses_gas` | boolean | ✅ | Whether business uses gas equipment |
| `has_misting` | boolean | ✅ | Whether business uses misting/cooling systems |
| `offers_delivery` | boolean | ✅ | Whether business offers delivery services |

## Error Handling

### 400 Bad Request
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "size_m2"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "error": "Requirements file not found",
  "matches": [],
  "report": null
}
```

## CORS Configuration
The API allows requests from:
- `http://localhost:5173` (frontend development server)

## LLM Integration
The `/assess` endpoint integrates with OpenAI GPT-3.5-turbo to generate intelligent reports:
- **Model**: `gpt-3.5-turbo`
- **Max Tokens**: 1000
- **Temperature**: 0.3
- **Validation**: Reports are validated to only reference provided rule IDs

## Development
```bash
# Start development server
cd backend
uvicorn app:app --reload

# Server runs on http://localhost:8000
# API docs available at http://localhost:8000/docs
```