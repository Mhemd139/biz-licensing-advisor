import { useState } from 'react';
import { Search } from 'lucide-react';
import { Profile } from '../lib/api';

interface AssessmentFormProps {
  onSubmit: (profile: Profile) => void;
  loading: boolean;
}

export default function AssessmentForm({ onSubmit, loading }: AssessmentFormProps) {
  const [profile, setProfile] = useState<Profile>({
    size_m2: 0,
    seats: 0,
    serves_alcohol: false,
    uses_gas: false,
    offers_delivery: false,
    has_misting: false,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(profile);
  };

  const isValid = profile.size_m2 > 0 && profile.seats > 0;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Restaurant Assessment
          </h2>
          <p className="text-gray-600">
            Enter your restaurant details to get personalized licensing requirements and compliance guidance.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Size and Seats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="size_m2" className="block text-sm font-medium text-gray-700 mb-2">
                Restaurant Size (m²) *
              </label>
              <input
                type="number"
                id="size_m2"
                min="1"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                value={profile.size_m2 || ''}
                onChange={(e) => setProfile({ ...profile, size_m2: parseInt(e.target.value) || 0 })}
              />
            </div>

            <div>
              <label htmlFor="seats" className="block text-sm font-medium text-gray-700 mb-2">
                Seating Capacity *
              </label>
              <input
                type="number"
                id="seats"
                min="1"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                value={profile.seats || ''}
                onChange={(e) => setProfile({ ...profile, seats: parseInt(e.target.value) || 0 })}
              />
            </div>
          </div>

          {/* Restaurant Features */}
          <fieldset>
            <legend className="block text-sm font-medium text-gray-700 mb-3">
              Restaurant Features
            </legend>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {[
                { key: 'uses_gas' as keyof Profile, label: 'Uses Gas Equipment' },
                { key: 'serves_alcohol' as keyof Profile, label: 'Serves Alcohol' },
                { key: 'offers_delivery' as keyof Profile, label: 'Offers Delivery' }
              ].map(({ key, label }) => (
                <label
                  key={key}
                  className={`relative flex items-center justify-center px-4 py-3 rounded-lg border cursor-pointer transition-colors ${
                    profile[key]
                      ? 'bg-blue-50 border-blue-200 text-blue-700'
                      : 'bg-gray-50 border-gray-200 text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <input
                    type="checkbox"
                    className="sr-only"
                    checked={profile[key] as boolean}
                    onChange={(e) => setProfile({ ...profile, [key]: e.target.checked })}
                  />
                  <span className="text-sm font-medium">{label}</span>
                </label>
              ))}
            </div>
          </fieldset>

          {/* Submit Button */}
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={!isValid || loading}
              aria-busy={loading}
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:ring-4 focus:ring-blue-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Search className="h-4 w-4" />
              )}
              {loading ? 'Assessing...' : 'Assess Requirements'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}