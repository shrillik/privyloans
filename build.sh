#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies and build React app
npm install
npm run build

# Initialize database
python -c "from api import app, db; app.app_context().push(); db.create_all()"
