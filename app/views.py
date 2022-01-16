from flask import render_template, request, redirect, url_for, session, flash
from sqlalchemy.ext.automap import automap_base
from app import app, db
import json
from jinja2.filters import FILTERS, environmentfilter
import base64


# b64encode for jinja2
@environmentfilter
def str_to_b64str(environment, value, attribute=None):
    return base64.b64encode(value.encode("ascii")).decode('ascii')


FILTERS['b64encode'] = str_to_b64str


# dumb but easy fix to stop it from complaining about db.query without installing sqlalchemy addons
# might break other things
# pylint: disable=no-member
Base = automap_base()
Base.prepare(db.engine, reflect=True)
Tables = {'tari': Base.classes.tari,
          'echipe': Base.classes.echipe,
          'utilizatori': Base.classes.utilizatori,
          'autori': Base.classes.autori,
          'concursuri_ctf': Base.classes.concursuri_ctf,
          'probleme': Base.classes.probleme,
          'rezolvari': Base.classes.rezolvari,
          'servere': Base.classes.servere,
          'incercari': Base.classes.incercari
          }


@ app.context_processor
def navbar_context():
    pages = [table for table in Tables.keys()]
    return {'pages': pages}


@ app.route('/')
def Index():
    return render_template('index.html')


@ app.route('/tari')
def tari():
    tableName = 'tari'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/echipe')
def echipe():
    tableName = 'echipe'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/utilizatori')
def utilizatori():
    tableName = 'utilizatori'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/autori')
def autori():
    tableName = 'autori'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/concursuri_ctf')
def concursuri_ctf():
    tableName = 'concursuri_ctf'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/probleme')
def probleme():
    tableName = 'probleme'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/rezolvari')
def rezolvari():
    tableName = 'rezolvari'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/servere')
def servere():
    tableName = 'servere'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/incercari')
def incercari():
    tableName = 'incercari'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        if "tableName" in session:
            try:
                tableName = session.get("tableName")
                table = Tables[tableName]
                requestdic = {key: None if val == "None" else val for key, val in request.form.items()}
                entry = table(**requestdic)

                db.session.add(entry)
                db.session.commit()
                flash("Adaugat cu succes!")
            except Exception as e:
                flash(str(e))

            return redirect(url_for(f'{tableName}'))
        else:
            return redirect(url_for("index"))


@ app.route('/update')
def update():
    return 1


@ app.route('/delete/<entity>')
def delete(entity):
    if "tableName" in session:
        try:
            entity = base64.b64decode(entity.encode('ascii')).decode('ascii')
            entity = json.loads(f"{entity[:-1]}}}")
            entity = {key: val for key, val in entity.items() if val != "None"}
            tableName = session.get("tableName")
            deletetable = f"db.session.query(Tables['{tableName}']).filter_by(**{entity}).delete()"
            eval(deletetable)
            db.session.commit()
            flash("Sters cu succes!")
        except Exception as e:
            flash(str(e))

        return redirect(url_for(f'{tableName}'))
