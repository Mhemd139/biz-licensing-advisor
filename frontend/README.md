# Business Licensing Advisor - Frontend

React frontend for the Business Licensing Advisor system.

## Environment Variables

Create a `.env` file in the frontend directory:

```bash
VITE_API_BASE=http://localhost:8000
VITE_MOCK=0
```

### Configuration Options

- `VITE_API_BASE`: Backend API URL (default: http://localhost:8000)
- `VITE_MOCK`: Set to `1` to enable mock mode, `0` for real API calls

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Features

- **Responsive Design**: Works on desktop and mobile
- **Mock Mode**: Fallback data when API is unavailable
- **PDF Export**: Print-friendly report generation
- **Accessibility**: ARIA labels, keyboard navigation, screen reader support
- **Error Handling**: Graceful degradation with user-friendly messages

## Components

- `Header`: Navigation with help/settings icons
- `AssessmentForm`: Business profile questionnaire
- `Summary`: Results overview with metrics
- `Obligations`: Key requirements list
- `NextActions`: Priority action items
- `Risks`: Compliance warnings
- `CitationsTable`: Legal references
- `Toast`: Success notifications

## Technology Stack

- **React 19**: UI framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Icons
- **Vite**: Build tool and dev server
