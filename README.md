# RainCast - Rain Prediction Web Application

RainCast is a modular, high-performance Django web application designed to predict rain forecasts for specified locations and dates. It integrates user authentication (signup/login), stores search histories, reads database configurations securely from a local JSON config, and uses the open-source Open-Meteo Weather APIs.

## Tech Stack & Highlights
- **Backend**: Django 4.2 (Modular app structure: `accounts` and `weather`)
- **Database**: PostgreSQL 14 (tracks users and queries)
- **APIs**: Open-Meteo Geocoding & Weather Forecast APIs (No API keys required)
- **Frontend**: Clean Vanilla CSS with responsive grid layout, glassmorphic card widgets, loading states, and live history logs injected via AJAX fetch.
- **Design Philosophy**: Object-Oriented Class-Based Views (CBVs) and clean separation of concerns.

---

## Installation & Setup

### 1. Database Setup
Ensure PostgreSQL is installed and running locally on port `5432`.

Create the PostgreSQL database and superuser. You can run the following SQL commands in your psql console:
```sql
CREATE ROLE postgres WITH LOGIN SUPERUSER PASSWORD 'password';
CREATE DATABASE django_task_db OWNER postgres;
```

### 2. Configuration Setup
Create a `config.json` file in the root of the project (if not present) with the database credentials:
```json
{
  "DB_NAME": "django_task_db",
  "DB_USER": "postgres",
  "DB_PASSWORD": "password",
  "DB_HOST": "127.0.0.1",
  "DB_PORT": "5432"
}
```

### 3. Virtual Environment & Dependencies
Create the virtual environment, activate it, and install all required packages:
```bash
# Create and activate environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Database Migrations
Run the Django migration commands to initialize the schemas:
```bash
python manage.py makemigrations accounts weather
python manage.py migrate
```

### 5. Running the Application
Start the Django development server:
```bash
python manage.py runserver
```
The application will be available at [http://localhost:8000](http://localhost:8000).

---

## API Endpoints Documentation

All requests targeting authentication pages or prediction endpoints are protected and managed using Class-Based Views (CBVs).

### 1. User Sign Up
- **Endpoint**: `/accounts/signup/`
- **Method**: `POST`
- **Form Data**:
  - `username`: unique string identifier
  - `email`: user's email address
  - `password1`: account password
  - `password2`: confirmation password

### 2. User Login
- **Endpoint**: `/accounts/login/`
- **Method**: `POST`
- **Form Data**:
  - `username`: username string
  - `password`: password string

### 3. Prediction API View
- **Endpoint**: `/api/predict/`
- **Method**: `POST`
- **Content-Type**: `application/json` (or standard form data)
- **Authentication**: Session cookie required (User must be logged in)

#### JSON Request Payload (Input)
```json
{
  "location": "Paris",
  "start_date": "2026-06-06",
  "end_date": "2026-06-08"
}
```

#### JSON Response Payload (Output)
```json
{
  "success": true,
  "data": {
    "id": 1,
    "location": "Paris, Île-de-France, France",
    "start_date": "2026-06-06",
    "end_date": "2026-06-08",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "rain_sum": 1.25,
    "precipitation_probability": 40.0,
    "is_rainy": true,
    "created_at": "2026-06-06 12:35:00"
  }
}
```

---

## Testing Endpoints with CURL

Django incorporates CSRF (Cross-Site Request Forgery) protection by default on POST routes. To test the API endpoints using Curl, you must extract and provide the CSRF tokens and persist session cookies.

Follow this sequential procedure:

### 1. Retrieve the CSRF Token and Init Cookies
Fetch the login page to initialize a `cookies.txt` file containing the CSRF token:
```bash
curl -c cookies.txt http://localhost:8000/accounts/login/
```

### 2. Login to Authenticate the Session
Extract the CSRF token from the saved cookie file and submit the login credentials. This updates `cookies.txt` with your authenticated session:
```bash
# 1. Extract the token value from the cookies
CSRF_TOKEN=$(grep csrftoken cookies.txt | awk '{print $7}')

# 2. POST the login credentials along with the CSRF token
curl -b cookies.txt -c cookies.txt \
  -d "username=your_username" \
  -d "password=your_password" \
  -d "csrfmiddlewaretoken=$CSRF_TOKEN" \
  -H "Referer: http://localhost:8000/accounts/login/" \
  http://localhost:8000/accounts/login/
```

### 3. Execute the Weather Prediction API Call
Use the authenticated session cookie and fresh CSRF token to call the prediction endpoint:
```bash
# 1. Retrieve the updated CSRF token
CSRF_TOKEN=$(grep csrftoken cookies.txt | awk '{print $7}')

# 2. Call the prediction API with location and date parameters
curl -b cookies.txt \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $CSRF_TOKEN" \
  -H "Referer: http://localhost:8000/" \
  -d '{"location": "Tokyo", "start_date": "2026-06-06", "end_date": "2026-06-09"}' \
  http://localhost:8000/api/predict/
```

---

## Running Automated Tests
Run the Django unit tests to verify database migrations, page routing, credentials checks, and mock API predictions:
```bash
python manage.py test
```
