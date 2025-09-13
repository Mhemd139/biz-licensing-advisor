import { Calendar } from 'lucide-react';
import { Report } from '../lib/api';

interface NextActionsProps {
  report: Report | null;
}

export default function NextActions({ report }: NextActionsProps) {
  const actions = report?.recommendations || [
    'Contact relevant authorities to confirm specific requirements for your business',
    'Gather required documentation and certificates',
    'Schedule necessary inspections with regulatory bodies',
    'Begin implementation of high-priority compliance measures'
  ];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-6">
          <Calendar className="h-5 w-5 text-gray-600" />
          <h2 className="text-xl font-semibold text-gray-900">Next 7 Days – Priority Actions</h2>
        </div>

        <div className="space-y-3">
          {actions.map((action, index) => (
            <div key={index} className="flex items-start gap-3">
              <div className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                {index + 1}
              </div>
              <div className="flex-1 bg-gray-50 rounded-lg px-4 py-3">
                <p className="text-gray-800 text-sm leading-relaxed">{action}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}