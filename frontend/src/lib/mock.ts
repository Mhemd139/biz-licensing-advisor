import { AssessmentResult, Rule } from './api';

export const mockAssessmentResult: AssessmentResult = {
  matches: [
    "R-Police-CCTV-Resolution",
    "R-Police-CCTV-Placement",
    "R-Police-Alcohol-Minors-Sign",
    "R-MoH-Water-Quality",
    "R-MoH-Gas-Safety-Ventilation",
    "R-MoH-Food-Temperature-Monitor",
    "R-MoH-Hygiene-Staff-Training",
    "R-MoH-Delivery-Food-Safety",
    "R-MoH-Kitchen-Ventilation",
    "R-MoH-Waste-Management"
  ],
  report: {
    summary: "Your restaurant requires licensing from 2 authorities: Israel Police (due to alcohol service) and Ministry of Health (standard food safety). Most requirements are straightforward but require proper documentation and equipment installation.",
    sections: [
      {
        title: "CCTV ≥1.3MP + backup",
        content: "Install CCTV system with minimum 1.3MP resolution and 30-minute backup power. Required for establishments serving alcohol.",
        rule_ids: ["R-Police-CCTV-Resolution"],
        priority: "high"
      },
      {
        title: "CCTV placement at entrance & facade",
        content: "Position cameras at entrance (inward) and facade covering 10m outward.",
        rule_ids: ["R-Police-CCTV-Placement"],
        priority: "medium"
      },
      {
        title: "Signage: no alcohol under 18",
        content: "Display entrance sign prohibiting alcohol sales to minors.",
        rule_ids: ["R-Police-Alcohol-Minors-Sign"],
        priority: "high"
      },
      {
        title: "Water quality testing",
        content: "Conduct regular water quality tests and maintain documentation.",
        rule_ids: ["R-MoH-Water-Quality"],
        priority: "high"
      },
      {
        title: "Gas equipment ventilation",
        content: "Install proper ventilation for gas cooking equipment.",
        rule_ids: ["R-MoH-Gas-Safety-Ventilation"],
        priority: "high"
      },
      {
        title: "Temperature monitoring systems",
        content: "Implement food storage temperature monitoring and logging.",
        rule_ids: ["R-MoH-Food-Temperature-Monitor"],
        priority: "medium"
      }
    ],
    total_rules: 10,
    high_priority_count: 4,
    recommendations: [
      "Contact licensed CCTV installer for system quote and installation timeline",
      "Schedule Ministry of Health pre-inspection to review kitchen setup",
      "Order required signage for alcohol service restrictions",
      "Begin staff training on food safety and hygiene protocols"
    ],
    authorities: ["Israel Police", "Ministry of Health"]
  }
};

export const mockRequirements: Rule[] = [
  {
    id: "R-Police-CCTV-Resolution",
    title: "CCTV ≥1.3MP + backup",
    desc_he: "טמ\"ס ברזולוציה 1.3MP לפחות, גיבוי חצי שעה להקלטה ולספקי כוח.",
    desc_en: "CCTV at ≥1.3MP with ≥30-min backup for recorder and camera power.",
    authority: "Israel Police",
    priority: "high",
    source_ref: "§3.3.1(1,3)",
    triggers: { flags: { serves_alcohol: true } }
  },
  {
    id: "R-Police-CCTV-Placement",
    title: "CCTV placement at entrance & facade",
    desc_he: "מצלמות בכניסה פנימה ולכיוון חזית העסק עד 10 מ'.",
    desc_en: "Place cameras at entrance (inward) and on facade covering up to 10m outward.",
    authority: "Israel Police",
    priority: "medium",
    source_ref: "§3.3.2(1–2)",
    triggers: { flags: { serves_alcohol: true } }
  },
  {
    id: "R-Police-Alcohol-Minors-Sign",
    title: "Signage: no alcohol under 18",
    desc_he: "שילוט בכניסה: אסור למכור/להגיש משקאות משכרים למי שטרם מלאו לו 18.",
    desc_en: "Entrance sign: alcohol may not be sold/served to under-18.",
    authority: "Israel Police",
    priority: "high",
    source_ref: "§3.6.1",
    triggers: { flags: { serves_alcohol: true } }
  },
  {
    id: "R-MoH-Water-Quality",
    title: "Water quality testing",
    desc_he: "בדיקות איכות מים תקופתיות ותיעוד התוצאות.",
    desc_en: "Regular water quality testing and documentation of results.",
    authority: "Ministry of Health",
    priority: "high",
    source_ref: "§4.2.1",
    triggers: {}
  },
  {
    id: "R-MoH-Gas-Safety-Ventilation",
    title: "Gas equipment ventilation",
    desc_he: "אוורור מתאים לציוד גז במטבח.",
    desc_en: "Proper ventilation for gas equipment in kitchen.",
    authority: "Ministry of Health",
    priority: "high",
    source_ref: "§4.5.2(1–3)",
    triggers: { flags: { uses_gas: true } }
  },
  {
    id: "R-MoH-Food-Temperature-Monitor",
    title: "Temperature monitoring systems",
    desc_he: "מערכות ניטור טמפרטורה למזון.",
    desc_en: "Food temperature monitoring systems.",
    authority: "Ministry of Health",
    priority: "medium",
    source_ref: "§4.3.4",
    triggers: {}
  }
];