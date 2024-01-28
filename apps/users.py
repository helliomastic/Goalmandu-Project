from flask import render_template,session,request,redirect
from flask_login import login_required,current_user
from . import app,db,User

@app.route('/admin/panel',methods=["GET"])
@login_required
def panel():
    if current_user.type != "Admin":
        return redirect("/")

    return render_template('adminPanel.html',session=session)


@app.route('/admin/viewUsers',methods=["GET","POST"])
@login_required
def viewUsers():
    if current_user.type != "Admin":
        return redirect("/")

    if request.method == "GET":
        users = User.query.all()
        return render_template('viewUsers.html',session=session, users=users)

    # get data
    if "user" not in request.form:
        return redirect("/admin/viewUsers")
    
    user = User.query.get(request.form['user'])
    # Delete User
    if user:
        db.session.delete(user)
        db.session.commit()
    
    return redirect("/admin/viewUsers")


@app.route('/admin/createUser',methods=["GET","POST"])
@login_required
def createUser():
    if current_user.type != "Admin":
        return redirect("/")
    
    if request.method == "GET":
        return render_template('createUser.html',session=session)

    # get data
    data = request.form.deepcopy()
    rq=["name","phone","password"]
    if any(i not in data or not data[i] for i in rq):
        error = f"Require:{','.join(rq)}"
        return render_template('auth/register.html',data=data,error=error)
    
    # create user
    newuser = User(
        name = data['name'],
        phone = data['phone'],
        password = data['password']
    )

    db.session.add(newuser)
    db.session.commit()

    return redirect("/admin/viewUsers")


@app.route('/admin/editUser',methods=["GET","POST"])
@login_required
def editUser():
    if current_user.type != "Admin":
        return redirect("/")
    
    if request.method == "GET":
        if "user" not in request.args:
            return redirect('/admin/viewUsers')
        
        user = User.query.get(request.args.get("user"))
        return render_template('edituser.html',session=session,user=user)

    # get data
    data = request.form.deepcopy()
    rq=["name","phone"]
    if any(i not in data or not data[i] for i in rq):
        return redirect('/admin/viewUsers')
    
    # edit user
    user = User.query.get(data['user'])
    if user:
        user.name = data['name']
        user.phone = data['phone']
        db.session.commit()

    return redirect('/admin/viewUsers')