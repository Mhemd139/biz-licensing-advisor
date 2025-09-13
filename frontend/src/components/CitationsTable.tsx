import { FileText } from 'lucide-react';
import { Report, Rule } from '../lib/api';

interface CitationsTableProps {
  report: Report | null;
  matches: string[];
  requirementsIndex: Record<string, Rule>;
}

export default function CitationsTable({ report, matches, requirementsIndex }: CitationsTableProps) {
  // Create citations from matches and report sections
  const citations = matches.map(ruleId => {
    const rule = requirementsIndex[ruleId];
    return {
      rule_id: ruleId,
      source_ref: rule?.source_ref || 'N/A'
    };
  });

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6" id="citations">
        <div className="flex items-center gap-2 mb-6">
          <FileText className="h-5 w-5 text-gray-600" />
          <h2 className="text-xl font-semibold text-gray-900">Legal References & Citations</h2>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Rule ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Requirement
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Legal Source
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {citations.map((citation, index) => {
                const rule = requirementsIndex[citation.rule_id];
                return (
                  <tr key={citation.rule_id} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <code className="text-sm text-blue-600 font-medium">
                        {citation.rule_id}
                      </code>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900">
                        {rule?.title || 'Unknown Requirement'}
                      </div>
                      {rule?.authority && (
                        <div className="text-xs text-gray-500 mt-1">
                          {rule.authority}
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {citation.source_ref}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {citations.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No citations available
          </div>
        )}
      </div>
    </div>
  );
}