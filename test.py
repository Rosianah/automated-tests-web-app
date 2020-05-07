from flask import Flask, request           # import flask
from flask_cors import CORS

app = Flask(__name__) # create an app instance
CORS(app)


@app.route("/", methods = ['POST'])
def test():
    testmsg = request.json
    print(testmsg)
    return "Ok", 200

if __name__ == "__main__":        # on running python app.py
    app.run(port=5000, debug=True)   