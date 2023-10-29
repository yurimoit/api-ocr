from flask import Flask

app=Flask(__name__)

@app.route("/")
def helloWorld():
    return f"<p>Hello, world!<p>"

if __name__ == "__main__":
   app.run(debug=True, port=5000)