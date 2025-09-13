import { Calendar } from 'lucide-react';
import { Report, Rule } from '../lib/api';

interface NextActionsProps {
  report: Report | null;
  matches: string[];
  requirementsIndex: Record<string, Rule>;
}

interface ActionItem {
  text: string;
  ruleIds: string[];
  priority: 'high' | 'medium' | 'low';
}

export default function NextActions({ report, matches, requirementsIndex }: NextActionsProps) {
  // Generate rule-specific actions based on matched requirements
  const generateRuleSpecificActions = (): ActionItem[] => {
    const actions: ActionItem[] = [];
    const highPriorityRules = matches.filter(id => requirementsIndex[id]?.priority === 'high');
    const mediumPriorityRules = matches.filter(id => requirementsIndex[id]?.priority === 'medium');

    // Group by authority for focused actions
    const authoritiesWithRules = Array.from(new Set(
      matches.map(id => requirementsIndex[id]?.authority).filter(Boolean)
    ));

    // High priority CCTV setup (if applicable)
    const cctvRules = matches.filter(id => id.includes('CCTV'));
    if (cctvRules.length > 0) {
      actions.push({
        text: `Install and configure CCTV system with proper resolution, placement, and signage requirements`,
        ruleIds: cctvRules,
        priority: 'high'
      });
    }

    // Fire safety equipment
    const fireRules = matches.filter(id =>
      requirementsIndex[id]?.authority === 'Fire & Rescue Authority'
    );
    if (fireRules.length > 0) {
      actions.push({
        text: `Implement fire safety measures including gas shutoffs, suppression systems, and safety equipment`,
        ruleIds: fireRules,
        priority: 'high'
      });
    }

    // Health department requirements
    const healthRules = matches.filter(id =>
      requirementsIndex[id]?.authority === 'Ministry of Health'
    );
    if (healthRules.length > 0) {
      actions.push({
        text: `Address health department requirements for food handling, temperature control, and sanitation`,
        ruleIds: healthRules,
        priority: 'high'
      });
    }

    // Authority contact actions
    authoritiesWithRules.forEach(authority => {
      const authorityRules = matches.filter(id => requirementsIndex[id]?.authority === authority);
      actions.push({
        text: `Contact ${authority} to confirm specific requirements and schedule inspections`,
        ruleIds: authorityRules,
        priority: 'medium'
      });
    });

    // Documentation gathering
    if (matches.length > 0) {
      actions.push({
        text: `Gather required documentation, certificates, and permits for all applicable requirements`,
        ruleIds: matches,
        priority: 'medium'
      });
    }

    return actions.slice(0, 7); // Limit to 7 actions for "Next 7 Days"
  };

  const actions = generateRuleSpecificActions();

  // Fallback to report recommendations if available, otherwise use generated actions
  const finalActions = report?.recommendations?.length ?
    report.recommendations.map((text, index) => ({
      text,
      ruleIds: matches, // Generic association
      priority: index < 2 ? 'high' : 'medium' as 'high' | 'medium' | 'low'
    })) : actions;

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-600';
      case 'medium': return 'bg-yellow-600';
      case 'low': return 'bg-green-600';
      default: return 'bg-blue-600';
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-6">
          <Calendar className="h-5 w-5 text-gray-600" />
          <h2 className="text-xl font-semibold text-gray-900">Next 7 Days – Priority Actions</h2>
        </div>

        <div className="space-y-3">
          {finalActions.map((action, index) => (
            <div key={index} className="flex items-start gap-3">
              <div className={`flex-shrink-0 w-6 h-6 text-white rounded-full flex items-center justify-center text-sm font-medium ${getPriorityColor(action.priority)}`}>
                {index + 1}
              </div>
              <div className="flex-1 bg-gray-50 rounded-lg px-4 py-3">
                <p className="text-gray-800 text-sm leading-relaxed">
                  {action.text}
                  {action.ruleIds.length > 0 && (
                    <span className="block mt-2 text-xs text-gray-500">
                      Related rules: {action.ruleIds.map(id => `(${id})`).join(', ')}
                    </span>
                  )}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}