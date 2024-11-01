# Bus Booking Project

## [Documentation](https://docs.google.com/document/d/1X3Rd19y_iBWKK9mHp12V298aLuHh6Z2xqw06ztuetiE/edit?usp=sharing)

## Demo Videos:
- [User UI](https://drive.google.com/file/d/1Jjgy3L74j5xO3A8D8bJD6ZU-s93VX9h0/view?usp=sharing)
- [Admin UI](https://drive.google.com/file/d/1Pe07m4BAloL8ZombodQLosFMc4PKL-O_/view?usp=sharing)










### DjangoBackend

#### Table of Contents

- [Setup Instructions backend](#setup-instructions-backend)
- [Setup Instructions frontend](#setup-instructions-frontend)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
---

### Setup Instructions BackEnd

#### Prerequisites

1. **Python** (>= 3.8)
2. **Git**
3. **Virtualenv** (recommended)
4. **Database** (e.g., PostgreSQL, MySQL, SQLite)

#### Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd djbackend/busbooker
   ```

2. **Set up the Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   ```bash
   cp .env.example .env
   ```

5. **Set Up Database**

   Run migrations to initialize the database.

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser**

   To access the Django admin, create a superuser account:

   ```bash
   python manage.py createsuperuser
   ```

### Running the Project

To start the Django development server:

```bash
python manage.py runserver
```

The project will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Here's a `README.md` file formatted for GitHub, tailored for a React app.

---

### React App

### Table of Contents

- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [Building for Production](#building-for-production)
- [Testing](#testing)
- [License](#license)

---
### Setup Instructions Frontend

#### Prerequisites

1. **Node.js** (>= 14.x recommended)
2. **npm** (comes with Node.js)

#### Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install Dependencies**

   Using npm:

   ```bash
   npm install
   ```
3. **Configure Environment Variables**

   Create a `.env` file in the root directory, using `.env.example` as a template. Fill in the required values.

   ```bash
   cp .env.example .env
   ```

### Running the Project

To start the React development server:

Using npm:

```bash
npm start
```

The project will be available at [http://localhost:3000](http://localhost:3000).

### Environment Variables

The `.env` file should contain any necessary environment variables. Example variables include:

- `REACT_APP_API_URL`
- `REACT_APP_AUTH_KEY`

### Building for Production

To create

### Environment Variables

The `.env` file should contain environment-specific configurations. Example variables include:

- `SECRET_KEY`
- `DATABASE_URL`
- `DEBUG`
- `ALLOWED_HOSTS`

