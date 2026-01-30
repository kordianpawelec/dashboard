from flask import Flask
from scripts.importand_days import Holidays
import json

app = Flask(__name__)

holidays = Holidays()

@app.route('/')
def main():
    html = "<h1>Irish Holidays</h1><table border='1'><tr><th>Name</th><th>Date</th><th>Type</th></tr>"
    
    for holiday in holidays.get_holidays():
        html += f"<tr><td>{holiday.get('name')}</td><td>{holiday.get('description')}</td><td>{holiday.get('date').get('iso')}</td><td>{holiday.get('type')}</td></tr>"
    return html

if __name__ == '__main__':
    app.run('0.0.0.0')