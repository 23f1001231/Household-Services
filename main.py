from flask import Flask

app = Flask("__main__")

@app.route("/")
def home():
    return "Hello"

app.run()
