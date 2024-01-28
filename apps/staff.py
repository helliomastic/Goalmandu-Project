from flask import render_template,session,request,redirect
from flask_login import login_required,current_user
from . import app,db,User,Futsal,Bookings,tools

@app.route('/registerFutsal',methods=["GET","POST"])
@login_required
def registerFutsal():
    if current_user.type != "Staff":
        return redirect("/")
    
    if request.method == "GET":
        return render_template('registerFutsal.html',session=session)
    
    # Get data
    data = request.form.deepcopy()
    rq=["name","location","contacts"]
    if any(i not in data or not data[i] for i in rq):
        error = f"Require:{','.join(rq)}"
        return render_template('registerFutsal.html',session=session, error=error)

    # Add to db
    futsal = Futsal(
        name=data['name'],
        location=data['location'],
        contacts=data['contacts']
    )
    db.session.add(futsal)
    db.session.commit()

    return redirect("/myFutsal")


@app.route('/myFutsal',methods=["GET"])
def myFutsal():
    if current_user.type != "Staff":
        return redirect("/")
    
    futsal = Futsal.query.filter_by(staff_id=current_user.id)
    
    return render_template('admin/admin.html',session=session, futsal=futsal)


@app.route('/addBooking',methods=["GET","POST"])
@login_required
def addBooking():
    if current_user.type != "Staff":
        return redirect("/")
    
    if request.method == "GET":
        return render_template('addBooking.html',session=session)


    data = request.form.deepcopy()
    rq=["date","time"]
    if any(i not in data or not data[i] for i in rq):
        error = f"Require:{','.join(rq)}"
        return render_template('addBooking.html',session=session, error=error)

    futsal = Futsal.query.filter_by(staff_id=current_user.id)
    can = tools.canBook(current_user.id,futsal.id,data['date'],data['time'])
    if not can:
        return render_template('addBooking.html',session=session, error="Cant book")
    
    # Add to db
    booking = Bookings(
        name=data['name'],
        location=data['location'],
        contacts=data['contacts']
    )

    db.session.add(booking)
    db.session.commit()
    
    return redirect("/viewBookings")


@app.route('/viewBookings',methods=["GET","POST"])
@login_required
def viewBookings():
    if current_user.type != "Staff":
        return redirect("/")
    
    if request.method == "GET":
        return render_template('myFutsal.html',session=session)

    
    if 'booking' not in request.form:
        return redirect('/viewBookings')
    
    booking = Bookings.query.get(request.form['booking'])
        
    # check if can cancel
        
    # cancel
    if booking:
        db.session.delete(booking)
        db.session.commit()

    return redirect('/viewBookings') 
    
