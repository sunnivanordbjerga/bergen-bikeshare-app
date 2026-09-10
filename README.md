# Bergen BikeShare

[![CI](https://github.com/sunnivanordbjerga/bergen-bikeshare-app/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sunnivanordbjerga/bergen-bikeshare-app/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/sunnivanordbjerga/bergen-bikeshare-app/branch/main/graph/badge.svg?token=MMY4R2WHRA)](https://codecov.io/github/sunnivanordbjerga/bergen-bikeshare-app)
![Python](https://img.shields.io/badge/python-3.13-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


*A bike-sharing management system built with Python, Shiny and SQLite.*

## Overview

Bergen BikeShare is an administrative dashboard for a fictional bike-sharing company operating in Bergen,
Norway.

## Features

* Bike fleet management
* Trip monitoring
* Station monitoring
* Maintenance operations and issue tracking
* Subscription and revenue analytics

---

## Status
Originally developed as a university database assignment, the project is currently being expanded into a portfolio application
featuring a more structured architecture, automated database seeding, testing and a richer administrative experience.

---

## Tech Stack

* Python
* SQLite
* Shiny for Python
* Pandas
* Pytest
* Faker
* Ruff

---

## Installation and running
### Requirements:
* [Python 3.13](https://www.python.org/downloads/) or newer
* [SQLITE3](https://sqlite.org/download.html)

### Clone:
```bash
   git clone https://github.com/sunnivanordbjerga/bergen-bikeshare-app
   cd bergen-bikeshare-app
```
### Install dependencies:
```bash
pip install .
```
### Run
To create/reset and seed the database:

On Windows (PowerShell):
```bash
$env:PYTHONPATH="src"; py src/seed_data/seed.py
```

On macOS / Linux:
```bash
PYTHONPATH=src python3 src/seed_data/seed.py
```

### Test:
```
pytest
```

---

## Database Design

<p style="text-align: center">
    <img src="docs/er_diagram.svg" width="80%" alt="ER diagram">
</p>

---

## Documentation
- [User stories](docs/user_stories.md)
- [Requirements](docs/requirements.md)

---

## Future improvements
MVP:
* Implement a Shiny interface
* Complete tests for core functionality

Stretch goals:
* Implement an interactive station map embed
* Show current weather on the home dashboard
* Implement an interactive bike SVG to visualise repair status

An overview of current development tasks can be found on the [issue board](https://github.com/users/sunnivanordbjerga/projects/2)

---

## Authors
Sunniva Nord Bjerga

---

## License
This project is licensed under a MIT license - see [LICENSE](LICENSE.md)
