from flask import render_template, request, redirect, url_for, session, flash
from sqlalchemy import table
from sqlalchemy.ext.automap import automap_base
from app import app, db
import json
from jinja2.filters import FILTERS, environmentfilter
import base64


# b64encode for jinja2
@environmentfilter
def str_to_b64str(environment, value, attribute=None):
    return base64.b64encode(value.encode("ascii")).decode('ascii')

# fixing dictionary from masterfile


@environmentfilter
def last_char_dic(enviorment, value, attribute=None):
    return value[:-1] + "}"


FILTERS['b64encode'] = str_to_b64str
FILTERS['last_char_dic'] = last_char_dic

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


@app.route('/team_score')
def queryhaving():

    tableData = db.session.execute("""  SELECT echipe.echipa_nume, SUM(probleme.puncte) AS scor
                                        FROM concursuri_ctf, probleme, incercari, echipe
                                        WHERE echipe.echipa_nume=incercari.echipa_nume AND probleme.flag=incercari.incercare_flag AND incercari.incercare_timp BETWEEN concursuri_ctf.timp_inceput AND concursuri_ctf.timp_terminat
                                        GROUP BY echipe.echipa_nume
                                        HAVING scor > 0
                                        ORDER BY scor desc;""").fetchall()

    columnNames = ["Echipa", "Scor"]
    print(tableData)
    return render_template('queryresults.html', tableName="Scorul Echipelor", columnNames=columnNames, tableData=tableData)


@app.route('/user_country')
def queryselect():

    tableData = db.session.execute("SELECT utilizatori.user_nume, tari.tara_nume                                        \
                                   FROM utilizatori, echipe, tari                                                       \
                                   WHERE utilizatori.echipa_nume=echipe.echipa_nume AND echipe.tara_tag=tari.tara_tag   \
                                   ").fetchall()
    columnNames = ["Utilizator", "Tara"]
    return render_template('queryresults.html', tableName="Utilizatorii din fiecare tara", columnNames=columnNames, tableData=tableData)


@ app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        if "tableName" in session:
            try:
                tableName = session.get("tableName")
                requestdic = {key: None if val == "None" else val for key, val in request.form.items()}
                entry = Tables[tableName](**requestdic)

                db.session.add(entry)
                db.session.commit()
                flash("Adaugat cu succes!")
            except Exception as e:
                flash(str(e))

            return redirect(url_for(f'{tableName}'))
        else:
            return redirect(url_for("index"))


@ app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        if "tableName" in session:
            try:
                print(request.form)
                tableName = session.get("tableName")
                table = Tables[tableName]
                requestdic = request.form.to_dict()

                entity = requestdic.pop("hiddenInfo")
                entity = base64.b64decode(entity.encode('ascii')).decode('ascii')
                entity = json.loads(entity)

                requestdic = {key: None if val == "None" else val for key, val in requestdic.items()}

                updatetable = db.session.query(table).filter_by(**entity).first()
                for key, val in requestdic.items():
                    setattr(updatetable, key, val)

                db.session.commit()
                flash("Updatat cu succes!")
            except Exception as e:
                flash(str(e))

            return redirect(url_for(f'{tableName}'))
        else:
            return redirect(url_for("index"))


@ app.route('/delete/<entity>')
def delete(entity):
    if "tableName" in session:
        try:
            entity = base64.b64decode(entity.encode('ascii')).decode('ascii')
            entity = json.loads(entity)
            entity = {key: val for key, val in entity.items() if val != "None"}
            tableName = session.get("tableName")
            table = Tables[tableName]
            db.session.query(table).filter_by(**entity).delete()
            db.session.commit()
            flash("Sters cu succes!")
        except Exception as e:
            flash(str(e))

        return redirect(url_for(f'{tableName}'))
