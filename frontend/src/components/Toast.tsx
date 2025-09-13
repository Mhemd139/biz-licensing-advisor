import { useEffect } from 'react';
import { CheckCircle, X } from 'lucide-react';

interface ToastProps {
  message: string;
  onClose: () => void;
  duration?: number;
}

export default function Toast({ message, onClose, duration = 4000 }: ToastProps) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [onClose, duration]);

  return (
    <div className="fixed top-4 right-4 z-50">
      <div
        className="bg-green-50 border border-green-200 rounded-lg px-4 py-3 shadow-lg flex items-center gap-3 max-w-md"
        role="alert"
        aria-live="polite"
      >
        <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0" />
        <p className="text-green-800 text-sm font-medium flex-1">{message}</p>
        <button
          onClick={onClose}
          className="text-green-600 hover:text-green-800 flex-shrink-0"
          aria-label="Close notification"
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}