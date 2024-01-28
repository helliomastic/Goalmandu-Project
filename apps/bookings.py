from flask import render_template,session,request,redirect
from flask_login import login_required,current_user
from . import app,db,User,Futsal,Bookings,tools


@app.route('/admin/viewBookings',methods=["GET","POST"])
@login_required
def viewBookingsA():
    if current_user.type != "Admin":
        return redirect("/")
    
    if request.method == "GET":
        bookings = Bookings.query.all()
        return render_template('viewBookings.html',session=session,bookings=bookings)
     
    if 'booking' not in request.form:
        return redirect('/admin/viewBookings')
    
    booking = Bookings.query.get(request.form['booking'])
    if booking:
        db.session.delete(booking)
        db.session.commit()

    return redirect('/admin/viewBookings')


@app.route('/admin/editBookings',methods=["GET","POST"])
@login_required
def editBookings():
    if current_user.type != "Admin":
        return redirect("/")

    if request.method == "GET":
        if 'booking' not in request.args:
            return redirect('/admin/viewBookings')
        
        booking = Bookings.query.get(request.args.get('booking'))
        return render_template('editBooking.html',session=session,booking=booking)
    
    data = request.form.deepcopy()
    rq=["booking","date","time","duration","cost","status"]
    if any(i not in data or not data[i] for i in rq):
        return redirect('/admin/viewBookings')
    
    booking = Bookings.query.get(data['booking'])
    if booking:
        booking.date = data['date']
        booking.time = data['time']
        booking.duration = data['duration']
        booking.cost = data['cost']
        booking.status = data['status']
        db.session.commit()

    return redirect('/admin/viewBookings')


@app.route('/admin/refund',methods=["POST"])
@login_required
def refund():
    if current_user.type != "Admin":
        return redirect("/")
    
    # refund
    if 'booking' not in request.form:
        return redirect('/admin/viewBookings')
    
    booking = Bookings.query.get(request.form['booking'])
    if booking:
        tools.refund(booking)   ############################################ implement this Prajwal
        booking.status="Refunded"
        db.session.commit()
    
    return redirect('/admin/viewBookings')



@app.route('/admin/cancel',methods=["POST"])
@login_required
def cancel():
    if current_user.type != "Admin":
        return redirect("/")
    
    # cancel
    if 'booking' not in request.form:
        return redirect('/admin/viewBookings')
    
    booking = Bookings.query.get(request.form['booking'])
    if booking:
        booking.status="canceled"
        db.session.commit()

    return redirect('/admin/viewBookings')

