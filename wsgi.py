#!/usr/bin/env python3
"""
WSGI entry point for the Flask application.
This file is used by Gunicorn to serve the application.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Create the Flask application instance
app = create_app()

# For Gunicorn, the application object should be named 'application'
application = app

if __name__ == '__main__':
    # This allows running the file directly for development
    app.run(host='0.0.0.0', port=8000, debug=False) 