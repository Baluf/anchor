import os

from flask import Flask, render_template

from routes.route import sheet_blueprint

app = Flask(__name__)
app.register_blueprint(sheet_blueprint, prefix='/sheet')


@app.route('/')
def index():
    logo_file = os.path.join('static', 'logo.png')
    return render_template('templates/index.html', logo=logo_file)


if __name__ == '__main__':
    app.run(debug=True, )