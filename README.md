# calorties-api

### Directory Structure
The project directory structure is organized as follows:
```
- .env-vars.json
- .gcs-client.json
- .gitignore
- .env
- .flake8
- .pre-commit-config.yaml
- Dockerfile
- requirements.txt
- app/
  - schemas.py
  - routes.py
  - models.py
  - database.py
  - auth.py
  - security.py
  - main.py
  - gcs.py
```
The files and directories in the project are structured as follows:

- `.env-vars.json`: Contains environment variables used by the application.
- `.gcs-client.json`: Client credentials file for interacting with Google Cloud Storage (GCS).
- `.gitignore`: Specifies which files and directories should be ignored by Git version control.
- `.env`: Stores environment variables specific to the development or production environment.
- `.flake8`: Configuration settings for the Flake8 code linter.
- `.pre-commit-config.yaml`: Configuration file for pre-commit hooks.
- `Dockerfile`: Used to create a Docker image for the application.
- `requirements.txt`: Lists the Python dependencies required by the application.
- `app/`: Directory containing the application-specific code.
  - `schemas.py`: Data schemas or models used in the application.
  - `routes.py`: Routing logic for the API, defining the endpoints and actions.
  - `models.py`: Database models or object-relational mapping (ORM) definitions.
  - `database.py`: Handles the database connection and related operations.
  - `auth.py`: Authentication and authorization logic for the API.
  - `security.py`: Security-related functions or middleware for the application.
  - `main.py`: Entry point of the application, where the API server is started.
  - `gcs.py`: Functions or classes for interacting with Google Cloud Storage.

### Running the Code
To run the code for the API project, follow these steps:

#### Uvicorn
- Ensure you have Python installed or activated virtual environment on your system.
- Clone the Git repository using the command: `git clone <repository-url>`
- Change into the project directory: `cd <project-directory>`
- Set up the environment variables by creating a `.env` file and populating it with the necessary values.
- Export environment variables to active session: `source .env && export $(sed '/^#/d' .env | cut -d= -f1)`.
- Install the required Python dependencies by running: `pip install -r requirements.txt`
- Start the API server using Uvicorn: `uvicorn app.main:app --port 8080 --reload`
- The API should now be running locally on `http://localhost:8080`.

#### Docker
- Ensure you have Docker installed on your system.
- Clone the Git repository using the command: `git clone <repository-url>`
- Change into the project directory: `cd <project-directory>`
- Set up the environment variables by creating a `.env` file and populating it with the necessary values.
- Build the Docker image by running: `docker build -t calorties-api .`
- Run the Docker container: `docker run -p 8080:8080 calorties-api`
- The API should now be running locally on `http://localhost:8080`.

#### Cloud Run
- Set up a Google Cloud Platform (GCP) project and enable the Cloud Run API.
- Ensure you have the Google Cloud SDK (gcloud) installed or actiated google cloud shell on your system.
- Clone the Git repository using the command: `git clone <repository-url>`.
- Change into the project directory: `cd <project-directory>`.
- Set up the environment variables by creating a `.env` file and populating it with the necessary values.
- Build a Docker image for the project: `gcloud builds submit --tag gcr.io/<project-id>/calorties-api`
- Deploy the Docker image to Cloud Run: `gcloud run deploy <service-name> --image gcr.io/<project-id>/calorties-api --platform managed`
- Follow the prompts to choose the project, region, and service name for the deployment.
- Once the deployment is complete, you will be provided with the URL for your API.

That's it! You have successfully set up and run the API project locally.
