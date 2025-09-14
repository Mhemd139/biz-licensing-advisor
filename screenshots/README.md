# Screenshots Instructions

## Required Screenshots for Submission

Take the following 3 screenshots and save them in this directory:

### 1. Questionnaire Interface (`questionnaire.png`)
- Start both backend and frontend servers
- Navigate to http://localhost:5173
- Show the business profile questionnaire form
- **Capture**: Full questionnaire with form fields visible

### 2. Generated Report (`report.png`)
- Fill out and submit the questionnaire
- Wait for the report to generate
- Scroll to show the complete report
- **Capture**: Generated licensing report with sections visible

### 3. API Documentation (`swagger.png`)
- Navigate to http://localhost:8000/docs
- Show the FastAPI Swagger documentation
- **Capture**: API endpoints and interactive documentation

## How to Take Screenshots

### For Questionnaire and Report:
1. Start backend:
   ```bash
   cd backend
   uvicorn app:app --reload
   ```

2. Start frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open http://localhost:5173 in browser
4. Take screenshot of questionnaire
5. Fill form and submit to get report
6. Take screenshot of generated report

### For API Documentation:
1. Ensure backend is running
2. Open http://localhost:8000/docs in browser
3. Take screenshot of Swagger interface

## Screenshot Requirements
- **Format**: PNG
- **Quality**: High resolution
- **Content**: Full page or relevant sections
- **Names**: Exactly as specified above

## File Naming
- `questionnaire.png` - Business questionnaire form
- `report.png` - Generated licensing report
- `swagger.png` - FastAPI documentation interface