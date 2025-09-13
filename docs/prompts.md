# Development Prompts Documentation

This document contains both development prompts and LLM system prompts for the Business Licensing Advisor system.

## LLM System Prompts

### System Prompt for Report Generation

```
You are an expert Israeli business licensing consultant. Generate structured reports in both Hebrew and English.
```

### Main Report Generation Prompt Template

Used in `backend/llm.py` for generating licensing reports:

```
Generate a licensing report for an Israeli restaurant business.

BUSINESS PROFILE:
- Size: {size_m2}m²
- Seats: {seats}
- Serves Alcohol: {serves_alcohol}
- Uses Gas: {uses_gas}
- Has Misting: {has_misting}
- Offers Delivery: {offers_delivery}

MATCHED RULES ({total_rules} total):
{rule_details}

REQUIREMENTS:
1. Start with a brief summary paragraph
2. Create sections for each authority with specific requirements
3. End with actionable recommendations

FORMAT YOUR RESPONSE AS:

## Summary
[Brief overview of licensing requirements]

## Israel Police Requirements
[List specific police requirements if any]

## Ministry of Health Requirements
[List specific health requirements if any]

## Fire & Rescue Authority Requirements
[List specific fire requirements if any]

## Recommendations
- [Actionable recommendation 1]
- [Actionable recommendation 2]
- [Actionable recommendation 3]

Use clear headers and bullet points. Include both Hebrew and English where relevant.
```

### LLM Configuration
- **Model**: `gpt-3.5-turbo` (optimized for speed)
- **Temperature**: `0.3`
- **Max Tokens**: `1000` (reduced from 2000 for faster response)

## Development User Prompts

### Prompt : Initial LLM Implementation Request
```
Looking at the TODO.md file, the next step would be M3  LLM Report Generation:

  ## M3  LLM Report Generation (4h)
  - [ ] `/backend/llm.py`: `call_llm(profile, matched_rules) -> ReportJSON`
  - [ ] Add guardrails + schema validation
  - [ ] Implement mock mode (env flag)
  - [ ] Acceptance:
    - [ ] Returns valid JSON referencing only provided `rule_ids`
    - [ ] Mock mode works in CI

  This involves:
  1. Creating an LLM integration module (backend/llm.py)
  2. Building a function that takes the business profile and matched rules and generates a smart report
   using AI
  3. Adding proper error handling and validation   
  4. Creating a mock mode for testing without API calls

  This is the core AI functionality that will transform the raw rule matches into clear, personalized 
  reports for business owners.

start it now
```

### Prompt : Commit Message Request
```
create a commit message, make it minimal yet describing , and send it to me , dont commit by ur self , just give me the commit message
```

### Prompt : Documentation Request
```
I added a file called prompts.md , u have to document my prompts 
the ones ive used and the ones I will use as its a part of the taskitself , u can look in task.md for any further explanations about this , also analyze task.md to look for anything else I might have missed that is required to do in the task , aside of the codings parts of course ,like documentations and else
```

### Prompt : Clarification on Documentation
```
write the prompts I wrote to u , not the prompts of ur response
```

### Prompt : Simplification Request
```
do not write the milestones , the todo , or future prompts I might use , plain and simple , the prompts I used to develop , my requests only
```

### Prompt : LLM Validation Test Request
```
create a test inside the backend that will validate that the llm works perfectly well , also tell when u need the openai api
```

### Prompt : OpenAI API Key Integration
```
sk-proj-*******

this is the open ai api key , itegrate it into an env
```

### Prompt : API Integration Issue Analysis
```
Log pattern:

HTTP 200
Parsing LLM response - using structured mock format
ERROR: 'size_m2'
Falling back to mock mode


Meaning: the API call completes (you wait 20–50s), then your parser raises KeyError: 'size_m2', discards the LLM result, and does extra local work to regenerate a mock. That exception doesn't add a ton of time by itself, but it wastes the already-paid network time and causes repeated calls across tests.

Root cause: your "structured mock format" parser expects fields (e.g., size_m2) in the LLM output that the real model isn't returning. So the integration path is effectively: call API → throw away → fallback to mock.
```

### Prompt : Disable Mock Mode Fallback
```
please also disable the feature of falling back to mock mode in all tests , I dont want mock at all , it either works or not
```

### Prompt : Fix .env Path Issue
```
  - ✅ API Key Present + Valid: Works normally with real LLM
  - ❌ API Key Missing: Raises RuntimeError("OPENAI_API_KEY is required")
  - ❌ API Key Invalid: Raises RuntimeError("LLM API integration failed")
  - ❌ OpenAI Library Missing: Raises RuntimeError("OpenAI library not
  installed")
  - ❌ LLM Response Parsing Fails: Raises RuntimeError("Failed to parse LLM
  response") with debug output

fix those , as u know the .env exists in the biz-licensing-advisor , while the llm.py exists in the backend folder , maybe thats the reason it doesnt find the openai api key ecen tho it exists
```

### Prompt : Performance Optimization Request
```
all tests passed , can u check v at the matching milstone in todo.md , also give me a simple message to commit , and also I have to know something , for 15 rules applied to a business it takes 40 secs to give back a result , but I think results can be given in an instanous manner , is my intuition wrong somehow?
```

### Prompt : Speed Optimization Implementation
```
do those changes please then ,   - Use gpt-3.5-turbo instead of gpt-4 for 5-10x speed improvement
  - Reduce max_tokens to 1000 if the reports don't need to be that long
  and dont forget putting my prompts in the file prompts.md
```

### Prompt : Documentation Reorganization
```
i will be moving prompts.md into docs f, we also have dev-logs so u can make the necessary
  changes , also ive seen it its too complex , simplify it and make it shorter , also dont forget to
  keep inputting my prompts into the file prompts.md , however for folder ai/ make a new file called
  tools.md , which contains claude code for coding and debugging , chatgpt for system planning and mvp
   and replit for the mock web app reference since I already have a mock web app via replit cause I
  needed to see how would the webapp look like and what would my produce actually act like for the
  perfect user experience

  also dont forget to add the fact that we used gpt3.5 turbo + max tokens is 1000
```

### Prompt : Task Analysis and M3 Gap Filling
```
ALWAYS REMEMBER TO ADD MY PROMPTS INTO PROMPTS.MD FILE like the previous prompt

now start filling the gaps we needed to fill in milestone M3 before we continue over to m4
```

### Prompt : Start M4 Frontend
```
lets start m4?
```

### Prompt : Check Documentation Requirements
```
for now look please into the task.md file and tell me if there is a part of the documentation that we might have missed
especially the part about the matching algorithm
```

### Prompt : Create Missing Documentation
```
yes please
```

### Prompt : M4 Frontend Implementation
```
okay for the m4 frontend , I have made a file named frontendui.md , make it and make sure to read it well , its a prompt for execution on how would the ui look , however dont be too attached to it , make the necessary changes to make things work
```

### Prompt : LLM Accuracy Improvement Request
```
yes please
```

### Prompt : Debug Missing CCTV Signage Rule
```
yes lets go on , save the future prompts of mine in the prompts.md
```

### Prompt : Analysis of Fixed Report Results
```
Issues / Weak Points

CCTV Signage

In your Legal References & Citations table, you list R-Police-CCTV-Signage as:

Unknown Requirement — N/A

But the spec explicitly requires signage at the entrance and near exterior cameras (§3.3.1(2)). Your JSON has the correct rule:

{
  "id": "R-Police-CCTV-Signage",
  "title": "CCTV area surveillance signage",
  "source_ref": "§3.3.5",
  ...
}

You're losing the mapping when generating the report. Probably a bug in your rule lookup/rendering (string mismatch between source_ref and your parser).

[Additional analysis about grouping, terminology, and actions provided...]

the report was Assessment Summary 14 Total Requirements 8 High Priority 22 Est. Processing Days...
```

### Prompt : Authority Misattribution and Rule Grouping Issues
```
⚠️ Still Problematic

Key Obligations Section is Merging Rules

Example:

Under Fire & Rescue, you wrote one block that includes gas compliance, shutoff, hood suppression, and exterior lighting (!).

But Exterior Lighting belongs to Police, not Fire.

This looks like your grouping logic is mixing obligations incorrectly.

Same under Israel Police: you lump resolution, alcohol minors signage, placement, and lighting into one "CCTV" block.

➝ This is misleading: users think "Exterior lighting" is Fire Authority when it's actually Police (§3.4).

Medium Priority Rules Not Reflected in Key Obligations

Your Key Obligations text is only summarizing some of them (and even merging them).

Users will see the Citations table has 14 rules, but the Key Obligations only "explains" ~9 of them.

Authority Misattribution

As noted:

Exterior lighting is listed under Fire in Key Obligations → incorrect.

Toilets and no-smoking signage are in the MoH block, which is fine, but they are all lumped together with food and sewage — again reducing clarity.

if u want go over docs/pdf file , and read the pdf file to get the actual hebrew written rules and citations to verify the veridicts and whatelse , also please record my promts in promots.md
```

### Prompt : Fix Key Obligations Presentation Layer
```
I have a webapp that generates licensing compliance reports. The rule engine itself is firing correctly (the right rules are matched), but the **presentation layer is wrong**.

The issue is in the "Key Obligations" section specifically. Rules are being:
- Collapsed into generic narrative blocks instead of being clearly itemized
- Incorrectly grouped/attributed to wrong authorities (e.g. Police rules showing under Fire Authority)
- Not reflecting accurate priority counts (High Priority count doesn't match what's displayed)

Please fix this issue so that:
- Each triggered rule is shown under the correct authority
- Rules are not collapsed into generic narrative lumps; they should be itemized clearly
- Priorities are accurately reflected
- No rules get misattributed to the wrong authority

Keep everything else unchanged (Assessment Summary, Next 7 Days Actions, Legal References table are working fine).
```

### Prompt : Add Rule ID Tags to Next Actions
```
In Next 7 Days, tag items with rule IDs (e.g., "(R-MoH-Food-Temps)") for traceability.
```

### Prompt : Request Commit Message
```
give me a commit message make it simple and clear
```