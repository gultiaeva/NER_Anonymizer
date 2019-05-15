#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask
from flask import request,url_for,make_response,render_template,jsonify, redirect
from flask_wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required



app = flask.Flask(__name__)
app.config['SECRET_KEY']="SOADISAHOIDLHWNEOIASLDNXOJASKBDOALSXANSLKXAIDNO"

class TextForm1(Form):
    enter = TextAreaField('Enter your text',validators=[Required()])
    submit = SubmitField('Analyze')

class TextForm2(Form):
    enter = TextAreaField('Here will be yput anonimized text',validators=[Required()])

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/anonimize_text', methods=['GET', 'POST'])
def home():
    enter1= None
    enter2 = None
    form1 = TextForm1()
    form2 = TextForm2()
    #if form1.validate_on_submit():
    if request.method == "POST":
        form2.enter.data=anonimize(form1.enter.data)
        #return redirect(url_for('anonimize'))
    return render_template ("index.html",form=[form1,form2],enter= [enter1,enter2])

#@app.route('/anonimized')
def anonimize(s):
    return "The text '{}' will be anonimized".format(s)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=9995,debug=True)

