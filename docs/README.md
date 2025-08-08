# Todo App Documentation

## Overview
This is a simple todo application built with Flask.

## Project Structure
```
todo-app/
├── src/                    # Source code
│   ├── static/            # Static files (CSS, JS, images)
│   │   ├── css/          # Stylesheets
│   │   ├── js/           # JavaScript files
│   │   └── images/       # Image assets
│   ├── templates/         # HTML templates
│   ├── models/           # Data models
│   ├── controllers/      # Route handlers
│   ├── utils/            # Utility functions
│   ├── app.py           # Main Flask application
│   └── main.py          # Application entry point
├── config/               # Configuration files
├── docs/                # Documentation
├── tests/               # Test files
├── requirements.txt     # Python dependencies
└── README.md           # Project README
```

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python src/main.py`

## Features
- Add new todos
- Mark todos as complete
- Delete todos
- Persistent storage

## API Endpoints
- `GET /` - Display todo list
- `POST /add` - Add new todo
- `POST /complete/<id>` - Mark todo as complete
- `POST /delete/<id>` - Delete todo 