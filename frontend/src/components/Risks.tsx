import { AlertTriangle } from 'lucide-react';
import { Report } from '../lib/api';

interface RisksProps {
  report: Report | null;
}

export default function Risks({ report }: RisksProps) {
  // Generate generic risks since backend doesn't provide specific ones
  const risks = [
    'Operating without proper licenses may result in fines and forced closure',
    'Non-compliance with safety regulations poses risks to customers and staff',
    'Delayed licensing applications may extend your time to market'
  ];

  const alertTypes = [
    { bg: 'bg-yellow-50', border: 'border-yellow-200', text: 'text-yellow-800', icon: 'text-yellow-600' },
    { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-800', icon: 'text-red-600' },
    { bg: 'bg-blue-50', border: 'border-blue-200', text: 'text-blue-800', icon: 'text-blue-600' },
  ];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-6">
          <AlertTriangle className="h-5 w-5 text-gray-600" />
          <h2 className="text-xl font-semibold text-gray-900">Risks & Compliance Warnings</h2>
        </div>

        <div className="space-y-4">
          {risks.slice(0, 3).map((risk, index) => {
            const alertStyle = alertTypes[index] || alertTypes[0];

            return (
              <div
                key={index}
                className={`rounded-lg border p-4 ${alertStyle.bg} ${alertStyle.border}`}
              >
                <div className="flex items-start gap-3">
                  <AlertTriangle className={`h-5 w-5 flex-shrink-0 mt-0.5 ${alertStyle.icon}`} />
                  <p className={`text-sm leading-relaxed ${alertStyle.text}`}>
                    {risk}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}