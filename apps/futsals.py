from flask import render_template,session,request,redirect
from flask_login import login_required,current_user
from . import app,db,User,Futsal

@app.route('/admin/viewFutsals',methods=["GET","POST"])
@login_required
def viewFutsals():
    if current_user.type != "Admin":
        return redirect("/")
    
    if request == "GET":
        futsals = Futsal.query.all()
        return render_template('viewFutsals.html',session=session,futsals=futsals)
    
    if 'futsal' not in request.form:
        return redirect('/admin/viewFutsals')
    
    futsal = Futsal.query.get(request.form['futsal'])
    if futsal:
        db.session.delete(futsal)
        db.session.commit()
        
    return redirect('/admin/viewFutsals') 


@app.route('/admin/editFutsal',methods=["GET","POST"])
@login_required
def editFutsal():
    if current_user.type != "Admin":
        return redirect("/")

    if request.method == "GET":
        if 'futsal' not in request.args:
            return redirect('/admin/viewFutsals')
        futsal = Futsal.query.get(request.args.get('futsal'))
        return render_template('editFutsal.html',session=session,futsal=futsal)
    
    data = request.form.deepcopy()
    rq=["futsal","name","location","contacts"]
    if any(i not in data or not data[i] for i in rq):
        return redirect('/admin/viewFutsal')
    
    futsal = Futsal.query.get(data['futsal'])
    if futsal:
        futsal.name = data['name']
        futsal.location = data['location']
        futsal.contacts = data['contacts']
        db.session.commit()

    return redirect('/admin/viewFutsals')