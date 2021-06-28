from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
Base = declarative_base()
app = Flask(__name__)


class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True)
    first_name = Column("first_name", String, unique=True)
    last_name = Column("last_name", String, unique=True)


@app.route("/", methods=['POST', 'GET'])
def get_name():
    engine = create_engine("sqlite:///new.db", echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    session = Session()

    try:
        last_entry = list(session.query(User).all())[-1]
        _name, _lastname = last_entry.first_name, last_entry.last_name
    except IndexError:
        _name = _lastname = "unknown name"

    if request.method == "POST":
        _name = request.form['name']
        _lastname = request.form['lastname']
        user = User(id=1, first_name="maurice", last_name="jarck")
        session.add(user)
        session.commit()

    session.close()

    return render_template("index.html", name=_name + " " + _lastname)


app.run(host="localhost", port=8080)
