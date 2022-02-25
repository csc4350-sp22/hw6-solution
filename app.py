import flask
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

app = flask.Flask(__name__)

# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class TVShow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)


db.create_all()


@app.route("/")
def index():
    shows = TVShow.query.all()
    return flask.render_template(
        "index.html",
        num_shows=len(shows),
        shows=[show.title for show in shows],
    )


@app.route("/save", methods=["POST"])
def save():
    show_name = flask.request.form.get("show")
    show = TVShow(title=show_name)
    db.session.add(show)
    db.session.commit()
    return flask.redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    show_name = flask.request.form.get("show")
    show = TVShow.query.filter_by(title=show_name).first()
    if show is not None:
        db.session.delete(show)
        db.session.commit()
    return flask.redirect("/")


app.run()
