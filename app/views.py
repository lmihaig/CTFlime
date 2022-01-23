from flask import render_template, request, redirect, url_for, session, flash
from sqlalchemy import table
from sqlalchemy.ext.automap import automap_base
from app import app, db
import json
from jinja2.filters import FILTERS, environmentfilter
import base64


@environmentfilter
def str_to_b64str(environment, value, attribute=None):
    """ b64encode for jinja2 """
    return base64.b64encode(value.encode("ascii")).decode('ascii')


@environmentfilter
def last_char_dic(enviorment, value, attribute=None):
    """ fixing dictionary from masterfile by removing trailing ',' and appending '}' """
    return value[:-1] + "}"


FILTERS['b64encode'] = str_to_b64str
FILTERS['last_char_dic'] = last_char_dic

# quick fix to stop it from complaining about db.query without installing sqlalchemy addons
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
    """ gives access to all the table names globally """
    tabele = [table for table in Tables.keys()]
    return {'tabele': tabele}


@ app.route('/')
def Index():
    """ default route """
    return render_template('index.html')


@ app.route('/tari')
def tari():
    """ route for tari table """
    tableName = 'tari'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/echipe')
def echipe():
    """ route for echipe table """
    tableName = 'echipe'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/utilizatori')
def utilizatori():
    """ route for utilizatori table """
    tableName = 'utilizatori'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/autori')
def autori():
    """ route for autori table """
    tableName = 'autori'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/concursuri_ctf')
def concursuri_ctf():
    """ route for concursuri_ctf table """
    tableName = 'concursuri_ctf'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/probleme')
def probleme():
    """ route for probleme table """
    tableName = 'probleme'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/rezolvari')
def rezolvari():
    """ route for rezolvari table """
    tableName = 'rezolvari'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/servere')
def servere():
    """ route for servere table """
    tableName = 'servere'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@ app.route('/incercari')
def incercari():
    """ route for incercari table """
    tableName = 'incercari'
    session["tableName"] = tableName
    table = Tables[tableName]
    columnNames = table.__table__.columns.keys()
    tableData = db.session.query(table).all()
    return render_template('masterfile.html', tableName=tableName, columnNames=columnNames, tableData=tableData)


@app.route('/team_score')
def queryhaving():
    """ a query using a GROUP BY and HAVING clause that returns all the teams and their total score, for a problem to be included in a 
    team's score the team needs to have submitted its solve during the contest and the flag must match the challenge's flag """

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
    """ a simple query with only a WHERE clause that returns all the users that have chosent o represent a country and their specific country """
    tableData = db.session.execute("SELECT utilizatori.user_nume, tari.tara_nume                                        \
                                   FROM utilizatori, echipe, tari                                                       \
                                   WHERE utilizatori.echipa_nume=echipe.echipa_nume AND echipe.tara_tag=tari.tara_tag   \
                                   ").fetchall()
    columnNames = ["Utilizator", "Tara"]
    return render_template('queryresults.html', tableName="Utilizatorii din fiecare tara", columnNames=columnNames, tableData=tableData)


@app.route('/rezolvari_corecte')
def viewcomplex():
    """ a complex view that shows all the eligible solves for all teams and the problem that the solve was for """
    db.session.execute("""
                        CREATE OR REPLACE VIEW probleme_rezolvate (echipa_nume, problema_id, problema_nume, puncte, incercare_timp)
                        AS SELECT echipe.echipa_nume, probleme.problema_id, probleme.problema_nume, probleme.puncte, incercari.incercare_timp
                        FROM echipe, probleme, concursuri_ctf, incercari
                        WHERE echipe.echipa_nume=incercari.echipa_nume AND probleme.flag=incercari.incercare_flag AND incercari.incercare_timp BETWEEN concursuri_ctf.timp_inceput AND concursuri_ctf.timp_terminat;
                        """)
    tableData = db.session.execute("SELECT * FROM probleme_rezolvate").fetchall()
    columnNames = tableData[0].keys()
    return render_template('queryresults.html', tableName="Problemele rezolvate corect", columnNames=columnNames, tableData=tableData)


@app.route('/upcoming')
def viewsimple():
    """ a simple view that shows all the contests that have yet to start or are not yet finished """
    db.session.execute("""
                        CREATE OR REPLACE VIEW concursuri_neterminate (concurs_id, concurs_nume, concurs_editie, timp_inceput, timp_terminat)
                        AS SELECT concurs_id, concurs_nume, concurs_editie, timp_inceput, timp_terminat
                        FROM concursuri_ctf
                        WHERE timp_terminat > CURRENT_TIMESTAMP;
                        """)
    tableData = db.session.execute("SELECT * FROM concursuri_neterminate").fetchall()
    columnNames = tableData[0].keys()
    return render_template('masterfile.html', tableName="Concursuri neterminate", columnNames=columnNames, tableData=tableData)


@app.route('/add', methods=['POST'])
def add():
    """ modular add route that works for all tables """
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
    """ modular update route that works for all tables """
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
    """ modular delete route that works for all tables """
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
