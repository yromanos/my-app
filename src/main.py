from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>My First App</title>
        </head>
        <body>
            <h1>This is my first app written in VS Code and downloaded from GitHub via docker !!</h1>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)