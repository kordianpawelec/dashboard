from flask import Flask
from scripts.importand_days import Holidays

app = Flask(__name__)

holiday = Holidays()

@app.route('/')
def main():
    return f"<p>data:\n{holiday.get_holidays()}</p>"

if __name__ == '__main__':
    app.run('0.0.0.0')