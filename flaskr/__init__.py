import os
from functools import lru_cache
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

@lru_cache(maxsize=None)
def collatz_length(n):
    if n == 1:
        return 1
    if n % 2 == 0:
        return 1 + collatz_length(n // 2)
    else:
        return 1 + collatz_length(3 * n + 1)

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

    cache_length = {}

    @app.route("/", methods=["GET"])
    def homepage():
        return render_template("homepage.html")

    @app.route("/sequence", methods=["GET", "POST"])
    def collatz():
        result = None
        sequence_length = None
        if request.method == "POST":
            number = int(request.form["number"])
            if number < 1:
                result = "Please enter a positive integer."
            else:
                result = collatz_sequence(number)
                sequence_length = len(result)
        return render_template("index.html", result=result, sequence_length=sequence_length)
    
    @app.route("/range", methods = ["GET", "POST"])
    def collatz_range():
        max_number = None
        max_length = None
        min_number = None
        min_length = None
        error = None
        if request.method == "POST":
            try:
                start = int(request.form["start"])
                end = int(request.form["end"])
                if start < 1 or end < 1:
                    error = "Both numbers must be positive integers."
                elif start > end:
                    error = "The start number must be less than or equal to the end number."
                else:
                    max_length = 0
                    min_length = float("inf")
                    for number in range(start, end + 1):
                        length = collatz_length(number)
                        if length > max_length:
                            max_length = length
                            max_number = number
                        if length < min_length:
                            min_length = length
                            min_number = number
            except ValueError:
                error = "Invalid input. Please enter positive integers."
        return render_template("range.html",
            max_number=max_number,
            max_length=max_length,
            min_number=min_number,
            min_length=min_length,
            error=error,)
    
    return app