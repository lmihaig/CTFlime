from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Create a file named secrets.txt that has only your password on one line
with open("secrets.txt", "r") as secretfile:
    password = secretfile.readline()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://root:{password}@localhost/ctflime"
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
