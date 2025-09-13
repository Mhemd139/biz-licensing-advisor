You are editing my Licensing Advisor frontend. Recreate the UI exactly as described below (based on screenshots), using React + Tailwind (no CSS files). Keep code clean, accessible, and responsive.

### Tech + constraints
- Files live under `frontend/` (Vite + React). If missing, create them.
- Use Tailwind utility classes. No external UI kits.
- You may use `lucide-react` for icons (Help, Settings, etc.). If not available, inline minimal SVGs.
- Add simple toast using a lightweight custom component (no library import).
- Provide a mock mode that renders example data if API fails or `import.meta.env.VITE_MOCK === '1'`.

### Endpoints
- POST `${import.meta.env.VITE_API_BASE ?? "http://localhost:8000"}/assess`
  Request JSON:
  {
    "size_m2": number,
    "seats": number,
    "serves_alcohol": boolean,
    "uses_gas": boolean,
    "delivery": boolean,
    "has_misting": boolean
  }
  Response JSON (current or near-term final):
  {
    "matches": [ "R-..." ],
    "report": {
      "summary": string,
      "key_obligations": [
        { "rule_id": string, "title": string, "what": string, "why": string, "priority": "high"|"medium"|"low" }
      ],
      "actions_next_7_days": [string],
      "risks": [string],
      "citations": [ { "rule_id": string, "source_ref": string } ]
    } | null
  }
- GET `${API_BASE}/requirements` returns an array of full rules.
- If `report` is null, synthesize a minimal view by mapping `matches[]` to rule objects from `/requirements`.

### UI to build (sections in order)
1) **Header**
   - Left: small circular icon (scales of justice) + “Business Licensing Advisor” (bold).
   - Right: two icon buttons (Help, Settings).
   - Thin bottom border.

2) **Assessment Card (Form)**
   - Title: “Restaurant Assessment”
   - Subtext: “Enter your restaurant details to get personalized licensing requirements and compliance guidance.”
   - Two inputs in a 2-column grid (stack on mobile):
     - “Restaurant Size (m²) *” (number)
     - “Seating Capacity *” (number)
   - “Restaurant Features” line, then three pill-style toggles (checkboxes):
     - Uses Gas Equipment
     - Serves Meat
     - Offers Delivery
     (rounded-lg containers with subtle border; selected state highlighted)
   - Primary button (right aligned): “Assess Requirements” with search icon.
   - When submitting: show loading state on button.

3) **Assessment Summary (after submit)**
   - Right top: “Export PDF” pill button with download icon.
   - Three stat cards side-by-side (stack on mobile):
     - **Total Requirements** (big number, neutral gray)
     - **High Priority** (big number, soft red background)
     - **Est. Processing Days** (big number, soft green background)
   - Below cards: one paragraph summary from `report.summary` (or synthesized if mock).

4) **Key Obligations (list)**
   - Section header with small doc icon: “Key Obligations”
   - For each obligation:
     - Badge on the left for priority (High/Medium/Low with color)
     - Title bold + small code (rule id)
     - Short description (`what` sentence)
     - “Authority: …” line if we can map from `/requirements`.
   - Link under list: “View all N requirements →” (scrolls to citations table).

5) **Next 7 Days – Priority Actions**
   - Title with calendar icon.
   - Vertical list of 1–4 pill rows, each prefixed by a circled number (1..4).

6) **Risks & Compliance Warnings**
   - Title with warning icon.
   - Three alert rows (yellow info, red danger, blue info). Rounded corners, soft background.

7) **Legal References & Citations (table)**
   - Title with document icon.
   - Table with columns: Rule ID (blue link-style), Requirement, Legal Source (e.g., “PDF p.7 §3.4”)
   - Populate from `report.citations` by joining with `/requirements` to get titles. If joining fails, render minimal info.

8) **Toast**
   - After a successful assess, show a non-blocking toast: “Report is ready”.
   - Auto-dismiss after 3–4s. Provide an `aria-live="polite"` region.

9) **Export to PDF**
   - On click “Export PDF”: open a print-optimized view and call `window.print()`. Add a simple `@media print` set via a `<style>` tag or inline tailwind `print:` utilities to hide header/help/settings and show a clean report.

### Component structure
Create these files (TypeScript or JS is fine; prefer TS if vite config allows):
- `frontend/src/App.tsx` (or `App.jsx`): page composition + routes (single page).
- `frontend/src/components/Header.tsx`
- `frontend/src/components/AssessmentForm.tsx`
- `frontend/src/components/Summary.tsx`
- `frontend/src/components/Obligations.tsx`
- `frontend/src/components/NextActions.tsx`
- `frontend/src/components/Risks.tsx`
- `frontend/src/components/CitationsTable.tsx`
- `frontend/src/components/Toast.tsx`
- `frontend/src/lib/api.ts` — client helpers:
  - `assess(profile)` returns `{matches, report}`
  - `getRequirements()` returns rules
- `frontend/src/lib/mock.ts` — provide one realistic mock response covering:
  - ~10 matched rule IDs
  - report.summary (2–3 sentences)
  - 5–6 obligations with mixed priorities
  - 4 next-7-days actions
  - 3 risk strings
  - citations array mapping to rule ids + source_ref

### State shape (App)
```ts
type Profile = {
  size_m2: number; seats: number;
  serves_alcohol: boolean; uses_gas: boolean; delivery: boolean; has_misting: boolean;
};
type Obligation = { rule_id: string; title: string; what: string; why?: string; priority: "high"|"medium"|"low" };
type Citation = { rule_id: string; source_ref: string };

type Report = {
  summary: string;
  key_obligations: Obligation[];
  actions_next_7_days: string[];
  risks: string[];
  citations: Citation[];
} | null;

type AssessmentResult = {
  matches: string[];
  report: Report;
};

type AppState = {
  profile: Profile;
  loading: boolean;
  error?: string;
  result?: AssessmentResult;
  requirementsIndex?: Record<string, any>; // id -> rule
};



UX details

Disable submit if required inputs missing.

On submit: loading=true, clear previous error.

If API 200:

Save result in state, show toast “Report is ready”.

Compute metrics:

total requirements = report ? report.key_obligations.length : matches.length

high priority count = number of obligations with priority high (or 0 if null).

est. days = simple heuristic: high*2 + (total-high)*1 (fallback)

If API fails or returns report: null, fetch /requirements and:

Map matches to rule objects for the Key Obligations (title from rule, what from rule.desc_en).

Create default actions_next_7_days and risks (generic text).

Add anchor “View all N requirements →” that scrolls to the citations table using an id="citations".

Accessibility

Proper <label for> & id on inputs.

Group features in a <fieldset><legend>Restaurant Features</legend></fieldset>.

Buttons have aria-busy when loading.

Acceptance checks

Form shows two numeric inputs + three pill checkboxes + primary CTA.

After submit, toast appears and all sections render in order:
Summary → Key Obligations → Next 7 Days → Risks → Citations.

“Export PDF” triggers print dialog with a clean layout.

Works in mobile (stacked) and desktop (3-column stat cards).

If backend is down, mock mode still shows a complete report UI.

Deliverables

All files created/updated with working imports.

Add a top-level frontend/README.md with instructions:

VITE_API_BASE=http://localhost:8000

VITE_MOCK=0|1

