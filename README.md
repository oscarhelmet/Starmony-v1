# Starmony App Technical Specification

## 1. Technology Stack

- Backend: Python with Flask web framework
- Frontend: HTML5, CSS3, JavaScript
- Database: SQLite (for simplicity, can be upgraded to PostgreSQL later)
- API: RESTful API for communication between frontend and backend

## 2. User Interface (UI)

- Clean, transparent style with a pastel light sky blue gradient background
- Modern design with rounded edges
- Responsive layout for various screen sizes

## 3. Question Generation and Display

### 3.1 Question Generation

   - The user will select the grade, subject, and language from the corresponding dropdown or slider UI components.
   - The user will enter the chapter in a text input field.
   - The user will click the "Generate Questions" button, which will trigger the `generate_question()` function.
   - The `generate_question()` function will take the following parameters:
      - `grade`: The selected grade (e.g., P1-P3, P4-P6, S1-S3, S4-S6)
      - `subject`: The selected subject (e.g., Chinese, English, Information & Comm Tech, Science, Geography)
      - `chapter`: The entered chapter
      - `language`: The selected language (e.g., Chinese(ZH), Chinese(CN), English)
   e. The function will then call the pre-prompted LLM API (in `llm/google.py`) to generate the questions XML file in the following format:

      ```xml
      <question>
          <q id="1">
              Question
              <sq>Sub-question <blank> (be) cool.</sq>
          </q>
      </question>
      ```

### 3.2 Question Display

   - The generated XML file will be parsed using `questions.js`.
   - The parsed data will be used to create an interactive quiz UI, where the user can input answers in the text boxes created for the `<blank>` elements.


### 3.3 Question Loader
- Parse XML file
- Display interactive quiz to the user
- Generate input fields based on <ans> tags

### 3.4 Answer Submission

   - When the user submits the answers, the application will route to the `/answer` endpoint.
   - The server-side will process the user's responses and generate an XML file in the following format:

      ```xml
      <res>
          <ans id="1">user answer</ans>
          <ans id="2"></ans> <!--for empty answer-->
      </res>
      ```

## 4. Dashboard

### 4.1 Dashboard Generation

   - The server-side will call the `dashboard()` function in `dashboard.py`, passing the original question XML (`qs`) and the user's response XML (`ans`).
   - The `dashboard()` function will process the data and generate the following XML structure:

      ```xml
      <dashboard>
          <accuracy>
              <part id='a'>
                  <title>Multiplication</title>
                  <value>75</value>
              </part>
          </accuracy>

          <strength>
              <p> XXXX </p>
              <p> XXXX </p>
          </strength>

          <weakness>
              <p> XXXX </p>
              <p> XXXX </p>
          </weakness>

          <recommendation>
              <p> XXXX </p>
              <p> XXXX </p>
          </recommendation>
      </dashboard>
      ```

   - The generated dashboard XML will be handled by the `dashboard.js` file to create the UI components.


### 4.2 Dashboard Components
- Accuracy of questions
- Strengths
- Weaknesses
- Recommendations
- Analysis of incorrect questions

## 5. API Endpoints

- POST /generate-questions: Generate question set
- GET /questions: Retrieve question set
- POST /submit-answers: Submit user answers
- GET /dashboard: Retrieve dashboard data

## 6. Database Schema

### 6.1 Users Table
- id (PRIMARY KEY)
- username
- email
- password_hash
- created_at
- updated_at

### 6.2 Sessions Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY referencing Users)
- session_data (JSON)
- created_at
- updated_at

### 6.3 QuizAttempts Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY referencing Users)
- questions_xml
- answers_xml
- score
- created_at

## 7. Security Considerations

- Implement HTTPS for secure communication
- Use bcrypt for password hashing
- Implement CSRF protection
- Sanitize user inputs to prevent XSS attacks

## 8. Future Enhancements

### 8.1 Session Management
- Implement user sessions to track progress across multiple quizzes
- Store session data in the Sessions table

### 8.2 Login System
- Develop user registration and login functionality
- Implement password reset and email verification features
- Use JWT (JSON Web Tokens) for authentication

## 9. Testing

- Unit tests for backend logic
- Integration tests for API endpoints
- UI tests for frontend components
- End-to-end tests for critical user flows

## 10. Deployment

- Use Docker for containerization
- Set up CI/CD pipeline (e.g., GitHub Actions)
- Deploy to a cloud platform (e.g., Heroku, AWS, or Google Cloud)

This technical specification provides a solid foundation for building the EduTech App. It covers the main components and features you've requested, while also considering future enhancements like session management and a login system. As you start developing the app, you may need to refine and expand on certain aspects of this specification.