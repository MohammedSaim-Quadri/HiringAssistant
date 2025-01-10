# AI Hiring Assistant

## Overview
The AI Hiring Assistant is an intelligent and interactive Streamlit-based application designed to assist recruitment agencies in streamlining their candidate screening process. It collects detailed candidate information, generates customized technical questions based on the candidate’s expertise, and facilitates an iterative Q&A flow to assess technical proficiency.

## Features
- **Candidate Information Collection**: 
  - Collects essential details like name, contact information, experience, desired position, and technical expertise.
  - Stores data securely for future reference.

- **Dynamic Question Generation**:
  - Generates technical interview questions tailored to the candidate’s experience, desired position, and tech stack.
  - Questions are based on open-source models, avoiding additional costs for API usage.

- **Iterative Q&A Flow**:
  - Presents one question at a time, collecting responses iteratively.
  - Allows for dynamic question refinement based on candidate answers.

- **Admin Dashboard**:
  - Enables admins to view, manage, and analyze candidate data.
  - Provides secure authentication for admin access.

- **Database Integration**:
  - Saves candidate data and their answers for further evaluation.
  - Supports retrieval of stored data for admin review.

## Setup and Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/ai-hiring-assistant.git
   cd ai-hiring-assistant
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv hiring_assistant_env
   source hiring_assistant_env/bin/activate  # On Windows: hiring_assistant_env\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   streamlit run assistant.py
   ```

5. **Access the Application**:
   Open your web browser and navigate to the URL displayed in the terminal (e.g., `http://localhost:8501`).

## Usage Instructions
### Candidate Workflow
1. **Candidate Information Form**:
   - Fill out the form with details like name, email, years of experience, desired position, location, and tech stack.
   - Submit the form to proceed to the technical questions.

2. **Technical Questions**:
   - Answer the questions generated based on your tech stack.
   - Each answer is saved, and the next question is presented iteratively.

3. **Review and Submit**:
   - Once all questions are answered, review your responses.
   - Responses are securely saved to the database.

### Admin Workflow
1. **Admin Login**:
   - Enter valid admin credentials to access the dashboard.

2. **Dashboard Features**:
   - View candidate details and their answers.
   - Manage and analyze data for further action.

## Technical Details
### Core Components
- **Streamlit**: 
  - Provides an intuitive and interactive front-end for candidates and admins.

- **Prompt Engineering**: 
  - Generates relevant technical questions using open-source models based on candidate input.

- **Session State**:
  - Manages application state across candidate workflows.

- **Database Integration**:
  - Saves candidate details and answers securely for retrieval and review.

### Key Files
- `assistant.py`: Main application logic for candidate interaction.
- `prompts.py`: Logic for generating technical interview questions.
- `utils.py`: Helper functions, including database integration and model initialization.
- `requirements.txt`: List of dependencies for the application.

## Customization
1. **Admin Credentials**:
   - Update the `authenticate_admin` function in `assistant.py` to set desired admin username and password.

2. **Database Integration**:
   - Modify the database-related functions in `utils.py` to integrate with your preferred database.

3. **Question Generation**:
   - Customize the `get_technical_prompt_with_context` function in `prompts.py` to refine question generation logic.

## Known Issues
- Invalid data formats may occasionally cause errors during answer display.
- Ensure that the input data adheres to the expected format to avoid interruptions.

## Future Enhancements
- Advanced NLP-based question generation.
- Enhanced admin analytics with visualizations.
- Multi-language support for diverse candidates.

## Contribution Guidelines
1. Fork the repository and create a new branch for your feature.
2. Submit a pull request with a detailed description of changes made.
3. Ensure all contributions adhere to the existing coding style and conventions.

## Support
For any issues or feature requests, please open an issue on the GitHub repository or contact the maintainer directly.
