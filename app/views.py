from msilib import Table
from flask import render_template, request
from sqlalchemy.ext.automap import automap_base
from app import app, db

# dumb but easy fix to stop it from complaining about db.query without installing sqlalchemy addons
# might break other things
# pylint: disable=no-member
Base = automap_base()
Base.prepare(db.engine, reflect=True)
Tables = {"tari": Base.classes.tari,
          "echipe": Base.classes.echipe,
          "utilizatori": Base.classes.utilizatori,
          "autori": Base.classes.autori,
          "concursuri_ctf": Base.classes.concursuri_ctf,
          "probleme": Base.classes.probleme,
          "rezolvari": Base.classes.rezolvari,
          "servere": Base.classes.servere,
          "incercari": Base.classes.incercari
          }


@app.context_processor
def navbar_context():
    pages = [table for table in Tables.keys()]
    return {"pages": pages}


@app.route("/")
def Index():
    return render_template("index.html")


@app.route('/tari')
def tari():
    tableName = "tari"
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template(f"{tableName}.html", tableName=tableName.title(), columnNames=columnNames, tableData=tableData)


@ app.route('/echipe')
def echipe():
    tableName = "echipe"
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template(f"{tableName}.html", tableName=tableName.title(), columnNames=columnNames, tableData=tableData)


@ app.route('/utilizatori')
def utilizatori():
    tableName = "utilizatori"
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template(f"{tableName}.html", tableName=tableName.title(), columnNames=columnNames, tableData=tableData)


@ app.route('/autori')
def autori():
    tableName = "autori"
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template(f"{tableName}.html", tableName=tableName.title(), columnNames=columnNames, tableData=tableData)


@ app.route('/concursuri_ctf')
def concursuri_ctf():
    tableName = "concursuri_ctf"
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template(f"{tableName}.html", tableName=tableName.title(), columnNames=columnNames, tableData=tableData)


@ app.route('/probleme')
def probleme():
    tableName = "probleme"
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template(f"{tableName}.html", tableName=tableName.title(), columnNames=columnNames, tableData=tableData)


@ app.route('/rezolvari')
def rezolvari():
    tableName = "rezolvari"
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template(f"{tableName}.html", tableName=tableName.title(), columnNames=columnNames, tableData=tableData)


@ app.route('/servere')
def servere():
    tableName = "servere"
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template(f"{tableName}.html", tableName=tableName.title(), columnNames=columnNames, tableData=tableData)


@ app.route('/incercari')
def incercari():
    tableName = "incercari"
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template(f"{tableName}.html", tableName=tableName.title(), columnNames=columnNames, tableData=tableData)
