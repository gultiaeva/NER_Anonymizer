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
from processing.postprocessing import form_answer
from joblib import load
import pickle
#from processing.natashenka import recognize_all

encoders = [load('processing/binaries/part_of_speech_encoder.joblib'),
            load('processing/binaries/gender_encoder.joblib'),
            load('processing/binaries/quantity_encoder.joblib'),
            load('processing/binaries/case_encoder.joblib'),
            load("processing/binaries/class_encoder.joblib")]

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
    if request.method == "POST":
        if "Unique_NER" in request.form:
            form2.enter.data = form_answer(form1.enter.data) #формируем ответ in :string
        elif "Natasha" in request.form:
            form2.enter.data = "Do smth too"
    return render_template("index.html", form=[form1, form2],
                           enter=[enter1, enter2])


# @app.route('/anonimized')
def anonimize(s):
    return "The text '{}' will be anonimized".format(s)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9995, debug=True)
