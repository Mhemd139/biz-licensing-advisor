import { FileText } from 'lucide-react';
import { Report, Rule } from '../lib/api';

interface ObligationsProps {
  report: Report | null;
  matches: string[];
  requirementsIndex: Record<string, Rule>;
}

export default function Obligations({ report, matches, requirementsIndex }: ObligationsProps) {
  // Use report sections if available, otherwise synthesize from matches
  const sections = report?.sections || matches.map(ruleId => {
    const rule = requirementsIndex[ruleId];
    return {
      title: rule?.title || 'Unknown Requirement',
      content: rule?.desc_en || 'Details not available',
      rule_ids: [ruleId],
      priority: rule?.priority as "high" | "medium" | "low" || 'medium'
    };
  });

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const scrollToCitations = () => {
    const element = document.getElementById('citations');
    element?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-6">
          <FileText className="h-5 w-5 text-gray-600" />
          <h2 className="text-xl font-semibold text-gray-900">Key Obligations</h2>
        </div>

        <div className="space-y-4 mb-6">
          {sections.map((section, index) => (
            <div key={section.rule_ids[0] || index} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium border ${getPriorityColor(section.priority)} flex-shrink-0`}>
                  {section.priority.charAt(0).toUpperCase() + section.priority.slice(1)}
                </span>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="font-medium text-gray-900">{section.title}</h3>
                    {section.rule_ids.length > 0 && (
                      <code className="text-xs text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded">
                        {section.rule_ids[0]}
                      </code>
                    )}
                  </div>

                  <p className="text-gray-700 text-sm mb-2">
                    {section.content}
                  </p>

                  {section.rule_ids[0] && requirementsIndex[section.rule_ids[0]] && (
                    <p className="text-xs text-gray-600">
                      <span className="font-medium">Authority:</span> {requirementsIndex[section.rule_ids[0]].authority}
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        <button
          onClick={scrollToCitations}
          className="text-blue-600 hover:text-blue-800 text-sm font-medium inline-flex items-center gap-1 transition-colors"
        >
          View all {sections.length} requirements →
        </button>
      </div>
    </div>
  );
}