from flask import render_template,session,request,redirect
from flask_login import login_required,current_user,login_user,logout_user
from . import app,db,User

@app.route('/register/',methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template('auth/register.html')
    
    # Get data
    data = request.form
    newuser = User()
    newuser.name =  data.get("name")
    newuser.password = data.get("password")
    newuser.phone = data.get("phone")
    newuser.is_admin = True
    
    # Insert
    db.session.add(newuser)
    db.session.commit()

    return redirect('/login')


@app.route('/login/',methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('auth/login.html')
    
    # Get data
    data = request.form

    # Validate
    user = User.query.filter_by(phone=data['phone']).first()
    if not user or user.password != data['password']:
        return render_template('auth/login.html',data=data,error="Account Doesnt Exist Or Incorrect Password")

    # login
    login_user(user,remember=True)
    if request.args.get("next"):
        return redirect(request.args.get("next"))

    return redirect('/')


@app.route('/logout/',methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect('/login')

