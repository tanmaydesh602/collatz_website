import os

from flask import Flask, render_template, request

def collatz_sequence(n):
    sequence = [n]
    while n>1: 
        if n%2==0:
            n//=2
        else:
            n=3*n+1
        sequence.append(n)
    return sequence

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=["GET", "POST"])
    def collatz():
        result = None
        if request.method == "POST":
            print(request.form)
            number = int(request.form["number"])
            if number < 1:
                result = "Please enter a positive integer."
            else:
                result = collatz_sequence(number)
        return render_template("index.html", result=result)
    
    return app