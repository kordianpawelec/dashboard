from flask import Flask
from scripts.importand_days import Holidays
import json

app = Flask(__name__)

holidays = Holidays()

@app.route('/')
def main():
    html = "<h1>Holidays</h1><table border='1'><tr><th>Name</th><th>Dates</th></tr>"
    
    for names, dates_list in holidays.get_data().items():
        
        dates = ''
        
        for date in dates_list:
            dates += f'{date['date']} {date['country']} '

        html += f"<tr><td>{names}</td><td>{dates}</td></tr>"
    
    html += "</table>"
    return html

@app.route('/upcomming')
def upcoming():
    html = "<h1>Upcoming Holidays (Next 7 Days)</h1><table border='1'><tr><th>Name</th><th>Date</th><th>Country</th><th>Days Until</th></tr>"
    
    for holiday in holidays.check_close_days():
        html += f"<tr><td>{holiday['name']}</td><td>{holiday['date']}</td><td>{holiday['country']}</td><td>{holiday['days_until']}</td></tr>"
    
    html += "</table>"
    return html

if __name__ == '__main__':
    app.run('0.0.0.0')