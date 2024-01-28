from flask import render_template,session,request,redirect
from . import app

@app.route('/')
@app.route('/home',methods=["GET"])
def index():
    return render_template('homepage.html',session=session)