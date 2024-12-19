# Project Name
## Right_Hr_Solutions
* This project focuses on creating a comprehensive tool for scraping data from various social media platforms such as Instagram, Twitter, and Facebook using Python and Django. The tool will allow users to gather and analyze social media data efficiently.

### Overview
* The Social Media Scraping Tool is designed to extract data from multiple social media platforms. This document details the module specifically for Twitter scraping, outlining the available APIs and their functionalities.

## Module Name 
### Frontend
* The Twitter Scraper module provides APIs to scrape data from Twitter using various approaches, such as profile names, hashtags, trending topics, and post IDs.


# Setup Instructions

## Installation

### Python Installation Process
Before proceeding, ensure Python is installed on your system. If not, you can download and install Python from [python.org](https://www.python.org/downloads/).

### Setting up a Virtual Environment
To work with Django, it's recommended to create a virtual environment. Follow the steps outlined in the [Python documentation](https://docs.python.org/3/tutorial/venv.html) or use tools like `virtualenv` or `venv`.

### Installing Django
Once the virtual environment is set up, you can install Django within it. Refer to the [Django documentation](https://docs.djangoproject.com/en/stable/intro/install/) for detailed instructions on installing Django.

## Getting Started

### Clone the Project
```bash
git clone https://github.com/exoticaitsolutions/Right_Hr_Solutions.git
```

## Navigate to the Project Directory

```bash
  cd Right_Hr_Solutions
```

# Install Dependencies
### Using requirements.txt
```
pip install -r requirements.txt
```

# Individual Dependencies


***Setuptools***
```
python -m pip install --upgrade pip setuptools
```
***SocialAuth***
```
pip install django-allauth
```

## Environment Variables
 To run this project, you will need to add the following environment variables to your .env file
# Create .env file
in linux
```
touch .env
```
in window 
```
type nul > .env
```
## Setup .env File 
```
EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = EMAIL_HOST
EMAIL_PORT = EMAIL_PORT
EMAIL_USE_SSL = EMAIL_USE_SSL
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL
```

# makemigrations
```
python manage.py makemigrations
```

# migrate
```
python manage.py migrate
```

# Run Project
```bash
python manage.py runserver
```


