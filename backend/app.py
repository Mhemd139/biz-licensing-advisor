from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import uvicorn
import logging
from matching import match_rules
from llm import call_llm, validate_report_references

app = FastAPI()

# Allow FE port 5173
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BusinessProfile(BaseModel):
    size_m2: int
    seats: int
    serves_alcohol: bool
    uses_gas: bool
    has_misting: bool
    offers_delivery: bool


def load_rules():
    """Load rules from requirements.json."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "requirements.json")
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/requirements")
def get_requirements():
    try:
        requirements = load_rules()
        return {"requirements": requirements, "count": len(requirements)}
    except FileNotFoundError:
        return {"requirements": [], "count": 0, "error": "Requirements file not found"}


@app.post("/assess")
def assess_business(profile: BusinessProfile):
    """Assess business profile against licensing requirements."""
    try:
        rules = load_rules()
        profile_dict = profile.model_dump()
        matches = match_rules(profile_dict, rules)
        match_ids = [rule["id"] for rule in matches]
        
        # Generate LLM report
        try:
            report = call_llm(profile_dict, matches)
            
            # Validate that report only references provided rule IDs
            if not validate_report_references(report, match_ids):
                raise ValueError("Report contains invalid rule references")
            
            return {
                "matches": match_ids,
                "report": report.model_dump()
            }
            
        except Exception as llm_error:
            logging.error(f"LLM report generation failed: {str(llm_error)}")
            return {
                "matches": match_ids,
                "report": None,
                "error": f"Report generation failed: {str(llm_error)}"
            }
        
    except Exception as e:
        return {"error": str(e), "matches": [], "report": None}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
