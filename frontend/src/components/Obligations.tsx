import { FileText, Building2, Shield, Flame } from 'lucide-react';
import { Report, Rule } from '../lib/api';

interface ObligationsProps {
  report: Report | null;
  matches: string[];
  requirementsIndex: Record<string, Rule>;
}

interface GroupedRule {
  ruleId: string;
  rule: Rule;
  priority: 'high' | 'medium' | 'low';
}

interface AuthorityGroup {
  authority: string;
  rules: GroupedRule[];
  icon: React.ReactNode;
}

export default function Obligations({ report, matches, requirementsIndex }: ObligationsProps) {
  // Group rules by authority
  const groupedByAuthority = matches.reduce((acc, ruleId) => {
    const rule = requirementsIndex[ruleId];
    if (!rule) return acc;

    const authority = rule.authority;
    if (!acc[authority]) {
      acc[authority] = [];
    }

    acc[authority].push({
      ruleId,
      rule,
      priority: rule.priority as 'high' | 'medium' | 'low'
    });

    return acc;
  }, {} as Record<string, GroupedRule[]>);

  // Create authority groups with proper ordering and icons
  const authorityGroups: AuthorityGroup[] = [
    {
      authority: 'Israel Police',
      rules: groupedByAuthority['Israel Police'] || [],
      icon: <Shield className="h-5 w-5 text-blue-600" />
    },
    {
      authority: 'Ministry of Health',
      rules: groupedByAuthority['Ministry of Health'] || [],
      icon: <Building2 className="h-5 w-5 text-green-600" />
    },
    {
      authority: 'Fire & Rescue Authority',
      rules: groupedByAuthority['Fire & Rescue Authority'] || [],
      icon: <Flame className="h-5 w-5 text-red-600" />
    }
  ].filter(group => group.rules.length > 0);

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

  const totalRules = matches.length;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-6">
          <FileText className="h-5 w-5 text-gray-600" />
          <h2 className="text-xl font-semibold text-gray-900">Key Obligations</h2>
        </div>

        <div className="space-y-6 mb-6">
          {authorityGroups.map((group) => (
            <div key={group.authority} className="border border-gray-200 rounded-lg overflow-hidden">
              {/* Authority Header */}
              <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
                <div className="flex items-center gap-2">
                  {group.icon}
                  <h3 className="font-semibold text-gray-900">{group.authority}</h3>
                  <span className="text-sm text-gray-500">({group.rules.length} requirements)</span>
                </div>
              </div>

              {/* Rules List */}
              <div className="divide-y divide-gray-100">
                {group.rules.map(({ ruleId, rule, priority }) => (
                  <div key={ruleId} className="p-4">
                    <div className="flex items-start gap-3">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium border ${getPriorityColor(priority)} flex-shrink-0 mt-0.5`}>
                        {priority.charAt(0).toUpperCase() + priority.slice(1)}
                      </span>

                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-2">
                          <h4 className="font-medium text-gray-900 text-sm">{rule.title}</h4>
                          <code className="text-xs text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded">
                            {ruleId}
                          </code>
                        </div>

                        <p className="text-gray-700 text-sm mb-2">
                          {rule.desc_en || 'Details not available'}
                        </p>

                        <p className="text-xs text-gray-500">
                          <span className="font-medium">Source:</span> {rule.source_ref || 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <button
          onClick={scrollToCitations}
          className="text-blue-600 hover:text-blue-800 text-sm font-medium inline-flex items-center gap-1 transition-colors"
        >
          View all {totalRules} requirements →
        </button>
      </div>
    </div>
  );
}