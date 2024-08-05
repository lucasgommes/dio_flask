from flask import Flask, url_for, request


app = Flask(__name__)


@app.route("/hello/<user>/<int:age>")
def hello_world(user, age):
    if user:
        return {
            "Name": "Lukas",
            "Age": 24
        }
    

@app.route("/welcome")
def welcome():
    return {
        "message": "Hello, World!"
    }


@app.route("/about", methods=["POST", "GET"])
def about():
    if request.method == 'GET':
        return 'This is a GET'
    else:
        return 'This is a POST'


with app.test_request_context():
    print(url_for("welcome"))
    print(url_for("about", next="/"))
    print(url_for("hello_world", user="Lukas", age=24))