# Development Log

## Project Overview
Business Licensing Advisor - A system to help Israeli business owners understand regulatory requirements for restaurants based on Hebrew regulatory documentation.

## Data Processing Approach

### Manual Curation Decision
**Date**: September 12, 2025  
**Decision**: Manual curation of Hebrew PDF content instead of automated extraction

**Rationale**:
- Hebrew PDF contains complex regulatory language requiring domain expertise
- Manual curation ensures accuracy of rule interpretation
- Allows for proper mapping of triggers to business characteristics
- Reduces risk of misinterpreting legal requirements

### Data Structure Design
**Triggers Schema**: Designed 5-trigger system for business profiling
- **Numeric Variables** (2):
  - `size_m2`: Restaurant area in square meters
  - `seats`: Number of customer seats/occupancy
- **Boolean Flags** (3):
  - `serves_alcohol`: Whether business serves alcoholic beverages
  - `has_misting`: Whether business uses misting systems/cooling towers
  - `uses_gas`: Whether business uses gas equipment

**Rule Structure**:
```json
{
  "id": "unique-rule-identifier",
  "title": "Rule title in English",
  "desc_he": "Hebrew description from source",
  "desc_en": "English translation",
  "authority": "Regulatory authority (Police/MoH)",
  "priority": "high|medium|low",
  "source_ref": "PDF page/section reference",
  "triggers": {
    "seats": {"min": 1, "max": 200},
    "flags": {"serves_alcohol": true}
  }
}
```

### Curated Rules Summary
**Total Rules**: 12 licensing requirements
- **Israel Police**: 6 rules (CCTV, alcohol signage, lighting, exemptions)
- **Ministry of Health**: 6 rules (water, hygiene, temperatures, facilities)

**Special Logic**: Police exemption rule - businesses ≤200 seats + no alcohol are exempt from Police requirements except the exemption rule itself.

## Development Milestones

### M0 - Repository & Skeleton ✅
**Completed**: September 12, 2025
- Created repository structure with backend/frontend/docs/data/scripts folders
- Implemented FastAPI backend with `/health` endpoint + CORS
- Set up React frontend with basic health check fetch
- **Status**: Backend runs on port 8000, frontend on 5173

### M1 - Data Processing (ETL) ✅  
**Completed**: September 12, 2025
- **Manual Curation**: Processed Hebrew regulatory PDF into structured JSON
- **Data Validation**: Created `scripts/parse_pdf.py` with schema validation
- **Output**: `data/requirements.json` with 12 curated rules
- **Source References**: All rules include PDF page/section citations

### M2 - Matching Engine ✅
**Completed**: September 12, 2025
- **Core Logic**: `backend/matching.py` with deterministic rule matching
- **Business Profile**: Pydantic model with 5 triggers
- **Sorting**: Priority → threshold tightness → authority
- **Special Guards**: Police exemption logic implemented
- **Testing**: 5 test scenarios covering cafes, steakhouses, ghost kitchens, large halls
- **API Integration**: `/assess` endpoint returning matched rule IDs

## Technical Decisions

### Backend Stack
- **Framework**: FastAPI (Python) for async performance and automatic OpenAPI docs
- **Validation**: Pydantic models for type safety and validation
- **Testing**: Native Python with FastAPI TestClient

### Frontend Stack  
- **Framework**: React + Vite for fast development
- **Styling**: Basic CSS (functionality over aesthetics per task requirements)

### Data Storage
- **Format**: JSON files for simplicity and version control
- **Location**: `/data/requirements.json` as single source of truth
- **Backup**: Git version control for rule change tracking

## Challenges & Solutions

### Challenge 1: Hebrew Text Processing
**Issue**: Complex Hebrew regulatory language  
**Solution**: Manual expert curation with bilingual descriptions  
**Result**: Accurate rule interpretation with proper legal references

### Challenge 2: Rule Complexity
**Issue**: Overlapping jurisdiction and exception rules  
**Solution**: Implemented special guard logic for Police exemptions  
**Result**: Correct rule filtering based on business characteristics

### Challenge 3: Testing Strategy
**Issue**: Need comprehensive coverage of business scenarios  
**Solution**: Created 5 representative test cases (cafe, steakhouse, ghost kitchen, large hall, edge cases)  
**Result**: 100% test pass rate with realistic business profiles

## Next Steps

### M3 - LLM Report Generation (In Progress)
**Target**: AI-powered report generation from matched rules
**Requirements**: 
- Integration with LLM API (OpenAI/Claude/Gemini)
- Structured report JSON (summary, obligations, actions, risks, citations)
- Mock mode for testing

### M4 - Frontend Implementation
**Target**: User-facing questionnaire and report display
**Requirements**:
- Business profile form with 5 inputs
- Report sections display
- PDF export functionality

## AI Tools Usage
**Development Assistant**: Claude Code (Anthropic)
- Code generation and architecture decisions
- Test case development
- Documentation writing
- Problem-solving and debugging

**Manual Work**:
- Hebrew PDF content analysis and translation
- Business logic rule definition
- Domain expertise for regulatory interpretation

---

*Last Updated*: September 12, 2025  
*Next Milestone*: M3 - LLM Integration