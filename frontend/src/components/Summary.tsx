import { Download } from 'lucide-react';
import { Report } from '../lib/api';

interface SummaryProps {
  report: Report | null;
  matchesCount: number;
  onExportPDF: () => void;
}

export default function Summary({ report, matchesCount, onExportPDF }: SummaryProps) {
  const totalRequirements = report ? report.total_rules : matchesCount;
  const highPriorityCount = report ? report.high_priority_count : 0;

  // Simple heuristic: high*2 + (total-high)*1
  const estimatedDays = highPriorityCount * 2 + (totalRequirements - highPriorityCount) * 1;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        {/* Header with Export Button */}
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Assessment Summary
            </h2>
          </div>
          <button
            onClick={onExportPDF}
            className="inline-flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors text-sm font-medium"
          >
            <Download className="h-4 w-4" />
            Export PDF
          </button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-gray-50 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-gray-900 mb-1">
              {totalRequirements}
            </div>
            <div className="text-sm text-gray-600">Total Requirements</div>
          </div>

          <div className="bg-red-50 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-red-600 mb-1">
              {highPriorityCount}
            </div>
            <div className="text-sm text-red-700">High Priority</div>
          </div>

          <div className="bg-green-50 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-green-600 mb-1">
              {estimatedDays}
            </div>
            <div className="text-sm text-green-700">Est. Processing Days</div>
          </div>
        </div>

        {/* Summary Text */}
        <div className="prose max-w-none">
          <p className="text-gray-700 leading-relaxed">
            {report?.summary ||
              `Your restaurant matches ${totalRequirements} licensing requirements. Review the detailed obligations below and prioritize high-priority items for faster compliance.`
            }
          </p>
        </div>
      </div>
    </div>
  );
}