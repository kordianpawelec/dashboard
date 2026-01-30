from flask import Flask
app = Flask(__name__)

@app.route('/')
def main():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == '__main__':
    app.run('0.0.0.0')