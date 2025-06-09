# BMW Car Price Predictor Project

This project aims to predict the price of BMW Series 3 cars based on various features. It encompasses web scraping, data analysis, model training, and a user-facing application.

## Project Structure

The project is organized into the following main directories:

-   `scrapping/`: Contains scripts for collecting car data from web sources.
-   `csvs/`: Stores the raw data obtained from scraping.
-   `main.ipynb`: A Jupyter Notebook detailing the data processing, exploratory data analysis (EDA), feature engineering, and model training pipeline.
-   `backend/`: Includes a Flask API to serve the trained machine learning model.
-   `frontend/`: A React-based application that allows users to interact with the model and get price predictions.
-   `docker-compose.yml`: For orchestrating the backend and frontend services using Docker.
-   `requirements.txt`: Python dependencies for the backend and Jupyter Notebook.

## Workflow

1.  **Data Collection (Scrapping)**:
    *   The `scrapping/autovit_scrap.py` script is used to scrape data for BMW Series 3 cars from Autovit.ro.
    *   It extracts details like model, engine size, horsepower, year, mileage, fuel type, location, price, and URL.
    *   The script handles pagination and saves the collected data into CSV files in the `csvs/` directory.
    *   **Note**: The script relies on specific HTML class names which might change over time, potentially requiring updates.

2.  **Data Analysis and Model Training (Jupyter Notebook - `main.ipynb`)**:
    *   **Data Loading and Cleaning**: Loads data from the CSVs, handles duplicates, and cleans the price column.
    *   **Exploratory Data Analysis (EDA)**: Analyzes feature distributions, correlations (log-transforming price due to skewness), and the impact of categorical features on price.
    *   **Feature Engineering**:
        *   Creates `Car Age` from `Year`.
        *   Extracts `Is_xDrive` and `Engine_Badge` from the `Model` string.
        *   Simplifies `Fuel Type` and maps `Location` to broader `Region` categories.
        *   One-hot encodes categorical features and standardizes numerical features.
    *   **Model Selection and Training**:
        *   Splits data into training and testing sets.
        *   Trains and evaluates several regression models (Linear Regression, Ridge, Lasso, Random Forest, Gradient Boosting).
        *   Gradient Boosting Regressor is identified as the best performer.
    *   **Saving Artifacts**: The trained Gradient Boosting model (`best_model.pkl`), scaler (`scaler.pkl`), and training column names (`training_columns.json`) are saved to `backend/notebook_output/`.
    *   **Prediction Function**: A `predict_price` function is defined to encapsulate preprocessing and prediction for new data.

3.  **Backend Service (`backend/`)**:
    *   A Flask application (`backend/main.py`) serves the trained model.
    *   It exposes a `/predict` endpoint that accepts car features as JSON input.
    *   The backend uses the `predict_price` function (adapted from the notebook) to preprocess the input and return the predicted price.
    *   The service can be run directly or containerized using the provided `backend/Dockerfile`.
    *   **Dependencies**: Listed in `backend/requirements.txt`.
    *   **Model Artifacts**: Expects `best_model.pkl`, `scaler.pkl`, and `training_columns.json` to be in `backend/notebook_output/`.

4.  **Frontend Application (`frontend/`)**:
    *   A React-based single-page application.
    *   Provides a user interface for inputting car features (Engine Size, Horse Power, Kilometers, Year, xDrive, Fuel Type, Region, Engine Badge).
    *   Sends the input data to the backend's `/predict` endpoint.
    *   Displays the predicted price received from the backend.
    *   Can be run in development mode (`npm start`) or built for production (`npm run build`).
    *   Can also be containerized using the `frontend/Dockerfile`.
    *   **Dependencies**: Listed in `frontend/package.json`.

## Setup and Running the Project

### 1. Scrapping (Optional - if new data is needed)

```bash
cd scrapping
# Ensure Python and necessary libraries (requests, beautifulsoup4, pandas) are installed
python autovit_scrap.py
```
This will generate a new CSV file in the `csvs/` directory.

### 2. Model Training (Optional - if retraining is needed)

*   Open and run the `main.ipynb` Jupyter Notebook.
*   Ensure all dependencies from `requirements.txt` (at the root or a similar environment) are installed.
*   This will regenerate the model artifacts in `backend/notebook_output/`.

### 3. Running Backend and Frontend with Docker Compose (Recommended)

This is the easiest way to run the full application.

```bash
# Ensure Docker and Docker Compose are installed
docker-compose up --build
```
*   The backend will be accessible at `http://localhost:8000`.
*   The frontend will be accessible at `http://localhost:3000`.

### 4. Running Backend Manually

```bash
cd backend
# Ensure Python and dependencies from backend/requirements.txt are installed
# (e.g., pip install -r requirements.txt)
python main.py
```
The backend will run on `http://localhost:5000` (or the port specified in `main.py`).

### 5. Running Frontend Manually

```bash
cd frontend
# Ensure Node.js and npm are installed
npm install
npm start
```
The frontend development server will typically open the application in your browser at `http://localhost:3000`.

## Key Technologies

*   **Python**: For scripting, data analysis, and backend development.
    *   **Pandas**: Data manipulation and analysis.
    *   **Scikit-learn**: Machine learning model training and evaluation.
    *   **Beautiful Soup**: Web scraping.
    *   **Requests**: HTTP requests for scraping.
    *   **Flask**: Backend API framework.
    *   **Joblib**: Saving and loading Python objects (models, scalers).
*   **Jupyter Notebook**: Interactive data science and model development.
*   **React**: Frontend JavaScript library for building the user interface.
*   **Docker & Docker Compose**: Containerization and orchestration of services.
*   **HTML/CSS**: Frontend structure and styling.

## Future Considerations

*   **Scraper Robustness**: Update the scraper to be less dependent on specific HTML class names, perhaps using more general selectors or a different scraping library.
*   **Error Handling**: Enhance error handling in both backend and frontend.
*   **Input Validation**: More comprehensive input validation on the frontend and backend.
*   **Model Monitoring**: Implement a system for monitoring model performance over time.
*   **CI/CD**: Set up a continuous integration and deployment pipeline.
*   **Advanced Features**: Consider adding features like price range estimation, confidence intervals, or explanations for predictions.
