# MapApp

MapApp is a simple Tkinter-based application that allows users to manage and visualize a list of users on a map. Each user has a name, surname, number of posts, location, and coordinates.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Diagram](#diagram)
- [License](#license)

## Features

- Add, edit, and remove users.
- Display user details.
- Visualize user locations on a map.
- Retrieve coordinates from Wikipedia.

## Requirements

- Python 3.6+
- Tkinter
- requests
- BeautifulSoup4
- psycopg2
- tkintermapview
- PostgreSQL

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/MapApp.git
    cd MapApp
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up the PostgreSQL database:

    ```sql
    CREATE DATABASE mapapp;
    \c mapapp
    CREATE TABLE public.users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        surname VARCHAR(50),
        posts INT,
        location VARCHAR(100),
        coords geometry(Point, 4326)
    );
    ```

4. Update the database connection parameters in the script:

    ```python
    db_params = connection.connect(
        database="mapapp",
        user="yourusername",
        password="yourpassword",
        host="localhost",
        port="5432"
    )
    ```

## Usage

Run the application:

```sh
python main.py
```

