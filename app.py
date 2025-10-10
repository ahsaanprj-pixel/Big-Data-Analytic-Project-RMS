# Week 1: Basic Flask application setup
from flask import Flask, render_template

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Basic database import (will be expanded in Wk 2)
# from database import Database

@app.route('/')
def index():
    # Basic route - will be expanded in later weeks
    return render_template('index.html', restaurant_name="Restaurant Management System")

# Placeholder routes for future development
@app.route('/config')
def config():
    return "Configuration page - coming in Wk 3"

@app.route('/create_order')
def create_order():
    return "Create Order page - coming in Wk 4"

@app.route('/kitchen')
def kitchen():
    return "Kitchen page - coming in Wk 5"

@app.route('/print_receipt')
def print_receipt():
    return "Print Receipt page - coming in Wk 6"

if __name__ == '__main__':
    app.run(debug=True)