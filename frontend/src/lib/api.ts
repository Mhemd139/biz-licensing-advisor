export interface Profile {
  size_m2: number;
  seats: number;
  serves_alcohol: boolean;
  uses_gas: boolean;
  offers_delivery: boolean;
  has_misting: boolean;
}

export interface ReportSection {
  title: string;
  content: string;
  rule_ids: string[];
  priority: "high" | "medium" | "low";
}

export interface Report {
  summary: string;
  sections: ReportSection[];
  total_rules: number;
  high_priority_count: number;
  recommendations: string[];
  authorities: string[];
}

export interface AssessmentResult {
  matches: string[];
  report: Report | null;
}

export interface Rule {
  id: string;
  title: string;
  desc_he: string;
  desc_en: string;
  authority: string;
  priority: string;
  source_ref: string;
  triggers: any;
}

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export async function assess(profile: Profile): Promise<AssessmentResult> {
  const response = await fetch(`${API_BASE}/assess`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(profile),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

export async function getRequirements(): Promise<Rule[]> {
  const response = await fetch(`${API_BASE}/requirements`);

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const data = await response.json();
  return data.requirements || [];
}