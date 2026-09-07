# Personal Expense Tracker

**Live Demo: ** Open the deployed Streamlit application
The live version runs with sample expense data for demonstration. The repository also contains the MySQL/SQL implementation used for database-backed analysis.

A simple personal expense analysis application built using **Python, Streamlit, MySQL, SQL, Pandas, and Plotly**.

I created this project to practice working with transaction data, storing data in a relational database, querying it using SQL, and presenting the results through an interactive Streamlit dashboard.

## What the Project Does

The project generates sample expense transactions and stores the data in a MySQL database.

The Streamlit application reads the expense data and allows the user to explore spending patterns using filters, summary metrics, charts, and predefined SQL queries.

## Features

* View expense transactions through a Streamlit application
* Filter expenses based on available categories and payment modes
* View summary metrics for the expense data
* Analyze spending using interactive Plotly charts
* Store and retrieve transaction data using MySQL
* Run predefined SQL queries for expense analysis
* Generate sample expense data using Python and Faker

## Technologies Used

* **Python** – application logic and data processing
* **Pandas** – data manipulation and analysis
* **Streamlit** – dashboard and user interface
* **MySQL** – storing expense transaction data
* **SQL** – querying and aggregating expense data
* **PyMySQL** – connecting Python with MySQL
* **Plotly** – interactive charts
* **Faker** – generating sample transaction data
* **python-dotenv** – managing database credentials through environment variables

## Project Files

```text
personal-expense-tracker/
│
├── app.py
├── database.py
├── data_generator.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

**app.py**
Contains the Streamlit dashboard, filters, metrics, visualizations, and SQL analysis section.

**database.py**
Handles the connection between the Python application and the MySQL database.

**data_generator.py**
Generates sample expense transaction data used in the project.

## Running the Project

### 1. Install the required packages

```bash
pip install -r requirements.txt
```

### 2. Configure MySQL

Create a MySQL database named:

```text
expense_new
```

### 3. Create a `.env` file

Create a `.env` file inside the project folder and enter your local MySQL credentials:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=expense_new
```

The `.env` file is included in `.gitignore`, so database credentials are not uploaded to GitHub.

### 4. Run the application

```bash
streamlit run app.py
```

## SQL Analysis

The application also contains predefined SQL queries to analyze the expense data.

Examples include:

* Average expense by category
* Highest-value transactions
* Category-wise expense analysis
* Payment-related expense analysis

This part of the project helped me practice connecting **Python applications with MySQL** and using SQL queries for data analysis.

## What I Learned

Through this project, I practiced:

* Connecting Python to a MySQL database
* Writing SQL queries for data analysis
* Working with Pandas DataFrames
* Building an interactive application using Streamlit
* Creating interactive visualizations using Plotly
* Organizing a small Python data project into multiple files
* Separating database credentials from source code using environment variables

## Author

**Dhashvinth Bashkar**

Data Science Portfolio Project



