import { useState, useEffect } from 'react';
import Header from './components/Header';
import AssessmentForm from './components/AssessmentForm';
import Summary from './components/Summary';
import Obligations from './components/Obligations';
import NextActions from './components/NextActions';
import CitationsTable from './components/CitationsTable';
import Toast from './components/Toast';
import { assess, getRequirements, Profile, AssessmentResult, Rule } from './lib/api';

interface AppState {
  profile: Profile;
  loading: boolean;
  error?: string;
  result?: AssessmentResult;
  requirementsIndex: Record<string, Rule>;
  showToast: boolean;
}

function App() {
  const [state, setState] = useState<AppState>({
    profile: {
      size_m2: 0,
      seats: 0,
      serves_alcohol: false,
      uses_gas: false,
      offers_delivery: false,
      has_misting: false,
    },
    loading: false,
    requirementsIndex: {},
    showToast: false,
  });

  // Load requirements on mount
  useEffect(() => {
    const loadRequirements = async () => {
      try {
        const requirements = await getRequirements();
        console.log('Loaded requirements count:', requirements.length);
        const index = requirements.reduce((acc, rule) => {
          acc[rule.id] = rule;
          return acc;
        }, {} as Record<string, Rule>);
        console.log('Has CCTV Signage rule:', !!index['R-Police-CCTV-Signage']);
        console.log('CCTV rule details:', index['R-Police-CCTV-Signage']);
        setState(prev => ({ ...prev, requirementsIndex: index }));
      } catch (error) {
        console.error('Failed to load requirements:', error);
        setState(prev => ({ ...prev, error: 'Failed to load requirements' }));
      }
    };

    loadRequirements();
  }, []);

  const handleFormSubmit = async (profile: Profile) => {
    setState(prev => ({ ...prev, loading: true, error: undefined }));

    try {
      const result = await assess(profile);

      // Debug logging
      console.log('API Response:', result);
      console.log('Matches count:', result.matches?.length);
      console.log('Report total_rules:', result.report?.total_rules);
      console.log('Report sections count:', result.report?.sections?.length);

      // If report is null, synthesize a basic one
      if (!result.report) {
        const sections = result.matches.map(ruleId => {
          const rule = state.requirementsIndex[ruleId];
          return {
            title: rule?.title || 'Unknown Requirement',
            content: rule?.desc_en || 'Details not available',
            rule_ids: [ruleId],
            priority: (rule?.priority as "high" | "medium" | "low") || 'medium'
          };
        });

        const highPriorityCount = sections.filter(s => s.priority === 'high').length;
        const authorities = Array.from(new Set(result.matches
          .map(ruleId => state.requirementsIndex[ruleId]?.authority)
          .filter(Boolean)
        ));

        result.report = {
          summary: `Your restaurant matches ${result.matches.length} licensing requirements. Review the detailed obligations below and prioritize high-priority items for faster compliance.`,
          sections,
          total_rules: result.matches.length,
          high_priority_count: highPriorityCount,
          recommendations: [
            'Contact relevant authorities to confirm specific requirements',
            'Gather required documentation and certificates',
            'Schedule necessary inspections with regulatory bodies',
            'Begin implementation of high-priority compliance measures'
          ],
          authorities
        };
      }

      setState(prev => ({
        ...prev,
        loading: false,
        result,
        showToast: true
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Assessment failed'
      }));
    }
  };

  const handleExportPDF = () => {
    // Create print styles
    const printStyles = `
      <style>
        @media print {
          .no-print { display: none !important; }
          body { font-size: 12pt; line-height: 1.5; color: black; }
          .print\\:block { display: block !important; }
        }
      </style>
    `;

    // Add styles to document head temporarily
    const styleElement = document.createElement('div');
    styleElement.innerHTML = printStyles;
    document.head.appendChild(styleElement);

    // Trigger print
    window.print();

    // Remove styles after a delay
    setTimeout(() => {
      document.head.removeChild(styleElement);
    }, 1000);
  };

  const handleResetForm = () => {
    setState(prev => ({
      ...prev,
      result: undefined,
      error: undefined,
      showToast: false
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="no-print">
        <Header />
      </div>

      <main className="py-8 px-4 sm:px-6 lg:px-8">
        {!state.result ? (
          <AssessmentForm onSubmit={handleFormSubmit} loading={state.loading} />
        ) : (
          <div className="space-y-8">
            <Summary
              report={state.result.report}
              matchesCount={state.result.matches.length}
              onExportPDF={handleExportPDF}
            />
            <Obligations
              report={state.result.report}
              matches={state.result.matches}
              requirementsIndex={state.requirementsIndex}
            />
            <NextActions
              report={state.result.report}
              matches={state.result.matches}
              requirementsIndex={state.requirementsIndex}
            />
            <CitationsTable
              report={state.result.report}
              matches={state.result.matches}
              requirementsIndex={state.requirementsIndex}
            />

            {/* Back to Form Button */}
            <div className="max-w-4xl mx-auto no-print">
              <div className="text-center">
                <button
                  onClick={handleResetForm}
                  className="inline-flex items-center px-6 py-3 border border-gray-300 rounded-lg text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                >
                  ← New Assessment
                </button>
              </div>
            </div>
          </div>
        )}

        {state.showToast && (
          <Toast
            message="Report is ready"
            onClose={() => setState(prev => ({ ...prev, showToast: false }))}
          />
        )}
      </main>
    </div>
  );
}

export default App;