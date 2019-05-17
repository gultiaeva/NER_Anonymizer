#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask
from flask import request
from flask import url_for
from flask import make_response
from flask import render_template
from flask import jsonify
from flask import redirect
from flask_wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required
from processing.postprocessing import Predictor
from joblib import load
# from processing.natashenka import recognize_all


with open('processing/binaries/LGBMClassifier.pkl', 'rb') as f:
        classifier = pickle.load(f)

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = "SOADISAHOIDLHWNEOIASLDNXOJASKBDOALSXANSLKXAIDNO"


class TextForm1(Form):
    enter = TextAreaField('Enter your text', validators=[Required()],
                          render_kw={"rows": 18, "cols": 150})
    submit = SubmitField('Analyze')


class TextForm2(Form):
    enter = TextAreaField('Here will be your anonimized text',
                          validators=[Required()],
                          render_kw={"rows": 18, "cols": 150})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/anonimize_text', methods=['GET', 'POST'])
def home():
    enter1 = None
    enter2 = None
    form1 = TextForm1()
    form2 = TextForm2()
    # if form1.validate_on_submit():
    if request.method == "POST":
        pred = Predictor(classifier, form1.enter.data)
        form2.enter.data = pred.form_answer()   # формируем ответ in :string
        # return redirect(url_for('anonimize'))
    return render_template("index.html", form=[form1, form2],
                           enter=[enter1, enter2])


# @app.route('/anonimized')
def anonimize(s):
    return "The text '{}' will be anonimized".format(s)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9995, debug=True)
