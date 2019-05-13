#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import matplotlib.pyplot as plt
import numpy as np
import os
from werkzeug.security import generate_password_hash, check_password_hash

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

# app.debug = True

conn = pymysql.connect(host='localhost',
                       user='root',
                       port=8883,
                       password='root',
                       db='airline',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)



@app.route('/login')
def login():
	return render_template('login.html')



@app.route('/login_c')
def login_c():
	return render_template('login_c.html')

#Define route for register
@app.route('/register_c')
def register_c():
	return render_template('register_c.html')

#Authenticates the login
@app.route('/loginAuth_c', methods=['GET', 'POST'])
def loginAuth_c():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT password FROM customer WHERE email = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the user
		#session is a built in
        result= check_password_hash(data['password'], password)
        if result==False:
            error = 'Invalid login or username'
    		return render_template('login_c.html', error=error)
        else:
    		session['username'] = username
    		return redirect(url_for('home_c'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login_c.html', error=error)

#Authenticates the register
@app.route('/registerAuth_c', methods=['GET', 'POST'])
def registerAuth_c():
	#grabs information from the forms
    email = request.form['email']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    building_number = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    passport_num = request.form['passport_num']
    passport_exp_d = request.form['passport_exp_d']
    passport_exp_m = request.form['passport_exp_m']
    passport_exp_y = request.form['passport_exp_y']
    passport_country = request.form['passport_country']
    dob_d = request.form['dob_d']
    dob_m = request.form['dob_m']
    dob_y = request.form['dob_y']

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register_c.html', error = error)
    else:
        # hash the password and then enter in the databases
        password = generate_password_hash(password)
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, password, first_name, last_name, building_number, street, city, state, passport_num, passport_exp_d, passport_exp_m, passport_exp_y, passport_country, dob_d, dob_m, dob_y))
        conn.commit()
        cursor.close()
        return render_template('login_c.html')


@app.route('/')
def home():
    # global search
    return render_template('home.html',data=[{'temp':1}])


@app.route('/home_c')
def home_c():
    # global search
    username= session['username']
    return render_template('home_c.html',username=username, data=[{'temp':1}])

@app.route('/search', methods=['GET', 'POST'])
def search():
    # global search
    src_airport = request.form['src_airport']
    des_airport = request.form['des_airport']
    departure_d = request.form['departure_d']
    departure_m = request.form['departure_m']
    departure_y = request.form['departure_y']
    round_trip = request.form['round_trip']
    arrival_d = request.form['arrival_d']
    arrival_m = request.form['arrival_m']
    arrival_y = request.form['arrival_y']

	#cursor used to send queries
    cursor = conn.cursor()
    if round_trip=='No':

    	#executes query
        #query = 'SELECT * FROM flight WHERE departure_airport = %s and arrival_airport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status, num_of_seats FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE departure_airport = %s and arrival_airport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        #select (num_of_seats - (select count(flight_num) from buys natural join ticket natural join flight natural join airplane where flight_num = %s)) as available_seats
        #from airplane, flight where airplane.id = flight.airplane_id and airplane.airline_name = flight.airline_name and flight.flight_num = %s


        cursor.execute(query, (src_airport, des_airport, departure_d, departure_m, departure_y))
    	#stores the results in a variable
        data = cursor.fetchall()
    	#use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        print(data)
        if(data):
            return render_template('home_c.html', error='', flights=data)
        else:
    		#returns an error message to the html page
            message = 'No Tickets available'
            return render_template('home_c.html', error=message)
    else:
        #executes query
        query = 'SELECT * FROM user WHERE username = %s and password = %s'
        cursor.execute(query, (username, password))
        #stores the results in a variable
        data = cursor.fetchone()
        #use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        if(data):
            return render_template('home_c.html', error='', flighs=data)
        else:
            #returns an error message to the html page
            message = 'No Tickets available'
            return render_template('home_c.html', error=message, flighs=[])

@app.route('/search_c', methods=['GET', 'POST'])
def search_c():
    # global search
    src_airport = request.form['src_airport']
    des_airport = request.form['des_airport']
    departure_d = request.form['departure_d']
    departure_m = request.form['departure_m']
    departure_y = request.form['departure_y']

    round_trip = request.form['round_trip']
    arrival_d = request.form['arrival_d']
    arrival_m = request.form['arrival_m']
    arrival_y = request.form['arrival_y']

	#cursor used to send queries
    cursor = conn.cursor()
    if round_trip=='No':

    	#executes query
        #query = 'SELECT * FROM flight WHERE departure_airport = %s and arrival_airport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status, num_of_seats FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE departure_airport = %s and arrival_airport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        #select (num_of_seats - (select count(flight_num) from buys natural join ticket natural join flight natural join airplane where flight_num = %s)) as available_seats
        #from airplane, flight where airplane.id = flight.airplane_id and airplane.airline_name = flight.airline_name and flight.flight_num = %s


        cursor.execute(query, (src_airport, des_airport, departure_d, departure_m, departure_y))
    	#stores the results in a variable
        data = cursor.fetchall()
    	#use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        print(data)
        if(data):
            return render_template('home_c.html', error='', flights_departure=data, flights_arrival=[])
        else:
    		#returns an error message to the html page
            message = 'No Tickets available'
            return render_template('home_c.html', error=message)
    else:
        #executes query
        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status, num_of_seats FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE departure_airport = %s and arrival_airport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        #select (num_of_seats - (select count(flight_num) from buys natural join ticket natural join flight natural join airplane where flight_num = %s)) as available_seats
        #from airplane, flight where airplane.id = flight.airplane_id and airplane.airline_name = flight.airline_name and flight.flight_num = %s


        cursor.execute(query, (src_airport, des_airport, departure_d, departure_m, departure_y ))
    	#stores the results in a variable
        data_deparature = cursor.fetchall()
        #use fetchall() if you are expecting more than 1 data row

        # arrival
        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status, num_of_seats FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE departure_airport = %s and arrival_airport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        #select (num_of_seats - (select count(flight_num) from buys natural join ticket natural join flight natural join airplane where flight_num = %s)) as available_seats
        #from airplane, flight where airplane.id = flight.airplane_id and airplane.airline_name = flight.airline_name and flight.flight_num = %s


        cursor.execute(query, (des_airport, src_airport, arrival_d, arrival_m, arrival_y ))
    	#stores the results in a variable
        data_arrival = cursor.fetchall()

        cursor.close()
        error = None
        if(data_deparature):
            return render_template('home_c.html', error='', flights_departure=data_deparature, flights_arrival=data_arrival)
        else:
            #returns an error message to the html page
            message = 'No Tickets available'
            return render_template('home_c.html', error=message, flighs=[])



@app.route('/view_my_flights_c', methods=['GET', 'POST'])
def view_my_flights_c():
    username = session['username']
    cursor = conn.cursor()

    query = 'SELECT flight_num, status, airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM buys natural join ticket natural join flight where customer_email = %s'

    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()

    return render_template('view_my_flights_c.html', username=username, flights=data)


@app.route('/search_for_flights_c', methods=['GET', 'POST'])
def search_for_flights_c():
    return redirect(url_for('search'))

@app.route('/purchase_ticket_c', methods=['GET', 'POST'])
def purchase_ticket_c():
    username = session['username']
    if username==None:
        return render_template('login_c.html')


    #get the flight number
    flight_num_dep = request.form['flight_num_dep']
    airline_name_dep = request.form["airline_name_dep"]
    #print('airline_name_dep', airline_name_dep)
    #print("json",request.form['flight_num_dep'] )
    #print(flight_num_dep)

    round='no'
    try:
        flight_num_arr = request.form['flight_num_arr']
        airline_name_arr = request.form["airline_name_arr"]
        round='yes'
        #print(flight_num_arr)
    except:
        round='no'

    cursor = conn.cursor()
    if round=='yes':
        flight_num_arr = request.form['flight_num_arr']

        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
        cursor.execute(query, (flight_num_dep, airline_name_dep))

        #use fetchall() if you are expecting more than 1 data row
        dep_data = cursor.fetchone()

        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
        cursor.execute(query, (flight_num_arr, airline_name_arr))
        #stores the results in a variable
        arr_data = cursor.fetchone()
        cursor.close()

        #save the flight number in the session
        session['flight_num_dep'] = flight_num_dep
        session['airline_name_dep'] = airline_name_dep
        session['round_trip'] = round
        session['flight_num_arr'] = flight_num_arr
        session['airline_name_arr'] = airline_name_arr
        # get information of the flight and send to the payment page to ask for credit card information
        cursor = conn.cursor();
        # print(dep_data)
        price=arr_data['base_price'] + dep_data['base_price']
        #session['price'] = price

        return render_template('purchase_ticket_c.html', flight_dep=[dep_data], flight_arr=[arr_data], price=price)

    else:
        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
        cursor.execute(query, (flight_num_dep, airline_name_dep))
        #stores the results in a variable

        #use fetchall() if you are expecting more than 1 data row
        dep_data = cursor.fetchone()
        cursor.close()

        #save the flight number in the session
        session['flight_num_dep'] = flight_num_dep
        session['airline_name_dep'] = airline_name_dep
        session['round_trip'] = round
        session['flight_num_arr'] = 'None'
        session['airline_name_arr'] = 'None'

        # get information of the flight and send to the payment page to ask for credit card information
        cursor = conn.cursor();
        price=dep_data['base_price']
        #session['price'] = price
        return render_template('purchase_ticket_c.html', flight_dep=[dep_data], flight_arr=[], price=price)


@app.route('/payment_c', methods=['GET', 'POST'])
def payment_c():
    username = session['username']
    if not username:
        print('Please login first to pay')
        return render_template('login.html')

    #get credit card information from the form
    name = request.form['card_name']
    card_number = request.form['card_number']
    card_type = request.form['card_type']
    security_code = request.form['security_code']
    exp_month = request.form['exp_month']
    exp_year = request.form['exp_year']

    #get details of the flight saved in the session
    flight_num_dep= session['flight_num_dep']
    airline_name_dep= session['airline_name_dep']
    round= session['round_trip']
    flight_num_arr= session['flight_num_arr']
    airline_name_arr= session['airline_name_arr']
    #price=session['price']

    #card information

    # use information to process the payment and purchase the flight
    if round=='no':
        cursor = conn.cursor();

        from random import randint
        ticket_number= str(randint(10000, 99999))
        payment_number = str(randint(10000000, 99999999))

        query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
        cursor.execute(query, (flight_num_dep, airline_name_dep))
        price = cursor.fetchone()['base_price']

        query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
        cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))

        query2 = 'insert into buys(ticket_id, customer_email) values (%s, %s)'
        cursor.execute(query2, (ticket_number, username))


        query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))


        query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
        cursor.execute(query4, (ticket_number, payment_number))

        conn.commit()
        cursor.close()

        return redirect(url_for('view_my_flights_c'))

    else:
        cursor = conn.cursor();
        from random import randint
        ticket_number= str(randint(10000, 99999))
        payment_number = str(randint(10000000, 99999999))

        query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
        cursor.execute(query, (flight_num_dep, airline_name_dep))
        price_dep = cursor.fetchone()['base_price']

        query6 = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
        cursor.execute(query6, (flight_num_arr, airline_name_arr))
        price_arr = cursor.fetchone()['base_price']

        price = price_dep + price_arr

        query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
        cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))

        query2 = 'insert into buys(ticket_id, customer_email) values (%s, %s)'
        cursor.execute(query2, (ticket_number, username))

        query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))

        query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
        cursor.execute(query4, (ticket_number, payment_number))

        conn.commit()
        return redirect(url_for('view_my_flights_c'))



@app.route('/track_my_spending_c', methods=['GET', 'POST'])
def track_my_spending_c():

    import datetime
    x = datetime.datetime.now()
    current_year = x.year
    last_year = x.year - 1
    current_month = x.strftime("%B")


    username = session['username']

    # start_month = request.form['start_month']
    # start_year = request.form['start_year']
    # end_month = request.form['end_month']
    # end_year = request.form['end_year']

    cursor = conn.cursor();

    query = 'SELECT sum(sold_price) as price from buys natural join paid natural join payment where customer_email = %s and purchase_year between %s and %s'
    cursor.execute(query, (username, last_year, current_year))
    data1 = cursor.fetchone()['price']
    print("Total price:", data1)


    query1 = 'SELECT sum(sold_price) as sum, purchase_month, purchase_year from buys natural join paid natural join payment where customer_email = %s and purchase_year between %s and %s group by purchase_month, purchase_year'
    cursor.execute(query1, (username, last_year, current_year))
    data = cursor.fetchall()
    #print("Printing:", data)
    #values = data['sum']
    print("data:", data)
    l = [0]*len(data)  #labels as January2019 for example
    p = [0]*len(data)  #total amount spend per monthYear
    amount = [0]*len(data)
    for i in range(len(data)):
        l[i] = (data[i]['purchase_month'] + data[i]['purchase_year'])
        p[i] = data[i]['sum']

    for i in range(len(data)):
        amount[i] = p[i]

    print(amount)

    labels = ["January","February","March","April","May","June","July","August"]
    price = [10,9,8,7,6,4,7,8]

    #fig, ax = plt.subplots()
    plt.bar(l, amount)
    # plt.savefig('static/images/plot0.png')
    # strFile = 'static/images/figure.png'
    plt.savefig('static/images/figure3.png')
    plt.close()

    cursor.close()
    return render_template('track_my_spending_c.html', username=username, price=data1, values=[], labels=[], name = 'My Spendings', url = 'static/images/figure3.png')




@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'



@app.route('/login_s')
def login_s():
	return render_template('login_s.html')

#Define route for register
@app.route('/register_s')
def register_s():
	return render_template('register_s.html')

#Authenticates the login
@app.route('/loginAuth_s', methods=['GET', 'POST'])
def loginAuth_s():
    username = request.form['username']
    password = request.form['password']
    cursor = conn.cursor()
    query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
	#stores the results in a variable
    data = cursor.fetchone()
    cursor.close()
    error = None
    if data==None:
        error = 'Invalid login or username'
        return render_template('login_s.html', error=error)

    session['username'] = username
    return redirect(url_for('home_s'))


#Authenticates the register
@app.route('/registerAuth_s', methods=['GET', 'POST'])
def registerAuth_s():
    username = request.form['username']
    password = request. form['password']
    first_name = request. form['first_name']
    last_name = request. form['last_name']
    airline_name = request. form['airline_name']
    cursor = conn.cursor()
    query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    data = cursor.fetchone()
    error = None
    if data != None:
        error = "This user already exists"
        return render_template('register_s.html', error = error)
    else:
        query = 'SELECT name FROM airline WHERE name = %s'
        cursor.execute(query, (airline_name))
        	#stores the results in a variable
        data = cursor.fetchone()
        if data==None:
            ins = 'INSERT INTO airline(name) VALUES(%s)'
            cursor.execute(ins, (airline_name))
        ins = 'INSERT INTO airline_staff(username, password, first_name, last_name, airline_name) VALUES(%s, %s, %s,%s,%s)'
        cursor.execute(ins, (username, password, first_name, last_name, airline_name))
        conn.commit()
        cursor.close()
        return render_template('login_s.html')


@app.route('/home_s')
def home_s():
    # global search
    username= session['username']
    if username==None:
        error = "Please login first"
        return render_template('login_s.html', error = error)

    return render_template('view_my_flights_s.html',email=email, data=[{'temp':1}])


@app.route('/view_my_flights_staff', methods=['GET', 'POST'])
def view_my_flights_staff():
    username = session['username']
    cursor = conn.cursor()

    query = 'SELECT username, airline_name FROM airline_staff where username = %s'

    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    if data==None:
        error = "Please login first"
        return render_template('login_s.html', error = error)

    query = 'SELECT flight_num, status, airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight where airline_name = %s'

    cursor.execute(query, (data['airline_name']))
    flights = cursor.fetchall()
    cursor.close()

    return render_template('view_my_flights_staff.html', username=username, flights=flights)


@app.route('/change_flight_status', methods=['GET', 'POST'])
def change_flight_status():
    username = session['username']
    if username==None:
        return render_template('login_s.html')


    #get the flight number
    flight_num = request.form['flight_num']
    new_status = request.form['new_status']

    if flight_num==None:

        flight_num_staffrr = request.form['flight_num_staffrr']

        query = 'SELECT flight_num, flight.airline_name, departure_staffirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_staffirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
        cursor.execute(query, (flight_num_dep, airline_name_dep))

        #use fetchall() if you are expecting more than 1 data row
        dep_data = cursor.fetchone()

        query = 'SELECT flight_num, flight.airline_name, departure_staffirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_staffirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
        cursor.execute(query, (flight_num_staffrr, airline_name_staffrr))
        #stores the results in a variable
        arr_data = cursor.fetchone()
        cursor.close()

        #save the flight number in the session
        session['flight_num_dep'] = flight_num_dep
        session['airline_name_dep'] = airline_name_dep
        session['round_trip'] = round
        session['flight_num_staffrr'] = flight_num_staffrr
        session['airline_name_staffrr'] = airline_name_staffrr
        # get information of the flight and send to the payment page to ask for credit card information
        cursor = conn.cursor();
        # print(dep_data)
        price=arr_data['base_price'] + dep_data['base_price']
        #session['price'] = price

        return render_template('purchase_ticket_staff.html', flight_dep=[dep_data], flight_staffrr=[arr_data], price=price)

    else:
        query = 'SELECT flight_num, flight.airline_name, departure_staffirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_staffirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
        cursor.execute(query, (flight_num_dep, airline_name_dep))
        #stores the results in a variable

        #use fetchall() if you are expecting more than 1 data row
        dep_data = cursor.fetchone()
        cursor.close()

        #save the flight number in the session
        session['flight_num_dep'] = flight_num_dep
        session['airline_name_dep'] = airline_name_dep
        session['round_trip'] = round
        session['flight_num_staffrr'] = 'None'
        session['airline_name_staffrr'] = 'None'

        # get information of the flight and send to the payment page to ask for credit card information
        cursor = conn.cursor();
        price=dep_data['base_price']
        #session['price'] = price
        return render_template('purchase_ticket_c.html', flight_dep=[dep_data], flight_staffrr=[], price=price)
#
# @app.route('/create_new_flight', methods=['GET', 'POST'])
# def create_new_flight():
#     email = session['email']
#     if email==None:
#         return render_template('login_staff.html')
#
#
#     #get the flight number
#     flight_num_dep = request.form['flight_num_dep']
#     airline_name_dep = request.form["airline_name_dep"]
#
#
#     round='no'
#     try:
#         flight_num_staffrr = request.form['flight_num_staffrr']
#         airline_name_staffrr = request.form["airline_name_staffrr"]
#         round='yes'
#         #print(flight_num_staffrr)
#     except:
#         round='no'
#
#     cursor = conn.cursor()
#     if round=='yes':
#         flight_num_staffrr = request.form['flight_num_staffrr']
#
#         query = 'SELECT flight_num, flight.airline_name, departure_staffirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_staffirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#
#         #use fetchall() if you are expecting more than 1 data row
#         dep_data = cursor.fetchone()
#
#         query = 'SELECT flight_num, flight.airline_name, departure_staffirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_staffirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
#         cursor.execute(query, (flight_num_staffrr, airline_name_staffrr))
#         #stores the results in a variable
#         arr_data = cursor.fetchone()
#         cursor.close()
#
#         #save the flight number in the session
#         session['flight_num_dep'] = flight_num_dep
#         session['airline_name_dep'] = airline_name_dep
#         session['round_trip'] = round
#         session['flight_num_staffrr'] = flight_num_staffrr
#         session['airline_name_staffrr'] = airline_name_staffrr
#         # get information of the flight and send to the payment page to ask for credit card information
#         cursor = conn.cursor();
#         # print(dep_data)
#         price=arr_data['base_price'] + dep_data['base_price']
#         #session['price'] = price
#
#         return render_template('purchase_ticket_staff.html', flight_dep=[dep_data], flight_staffrr=[arr_data], price=price)
#
#     else:
#         query = 'SELECT flight_num, flight.airline_name, departure_staffirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_staffirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         #stores the results in a variable
#
#         #use fetchall() if you are expecting more than 1 data row
#         dep_data = cursor.fetchone()
#         cursor.close()
#
#         #save the flight number in the session
#         session['flight_num_dep'] = flight_num_dep
#         session['airline_name_dep'] = airline_name_dep
#         session['round_trip'] = round
#         session['flight_num_staffrr'] = 'None'
#         session['airline_name_staffrr'] = 'None'
#
#         # get information of the flight and send to the payment page to ask for credit card information
#         cursor = conn.cursor();
#         price=dep_data['base_price']
#         #session['price'] = price
#         return render_template('purchase_ticket_c.html', flight_dep=[dep_data], flight_staffrr=[], price=price)
#
# @app.route('/add_airplane', methods=['GET', 'POST'])
# def add_airplane():
#     email = session['email']
#     booking_staffgent_id = session['booking_staffgent_id']
#     if email==None:
#         print('Please login first to pay')
#         return render_template('login.html')
#
#     #get credit card information from the form
#     name = request.form['card_name']
#     card_number = request.form['card_number']
#     card_type = request.form['card_type']
#     security_code = request.form['security_code']
#     exp_month = request.form['exp_month']
#     exp_year = request.form['exp_year']
#
#     customer_email = request.form['email']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     building_number = request.form['building_number']
#     street = request.form['street']
#     city = request.form['city']
#     state = request.form['state']
#     passport_num = request.form['passport_num']
#     passport_exp_d = request.form['passport_exp_d']
#     passport_exp_m = request.form['passport_exp_m']
#     passport_exp_y = request.form['passport_exp_y']
#     passport_country = request.form['passport_country']
#     dob_d = request.form['dob_d']
#     dob_m = request.form['dob_m']
#     dob_y = request.form['dob_y']
#
#
#     #get details of the flight saved in the session
#     flight_num_dep= session['flight_num_dep']
#     airline_name_dep= session['airline_name_dep']
#     round= session['round_trip']
#     flight_num_staffrr= session['flight_num_staffrr']
#     airline_name_staffrr= session['airline_name_staffrr']
#     #price=session['price']
#     cursor = conn.cursor();
#     #card information
#     query0 = 'select email from customer where email = %s'
#     cursor.execute(query0, (customer_email))
#     data = cursor.fetchone()
#
#     if data == None:
#         ins = 'INSERT INTO customer(email, first_name, last_name, building_number, street, city, state, passport_number, passport_ex_day, passport_ex_month, passport_ex_year, passport_country, dob_day, dob_month, dob_year) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(ins, (customer_email, first_name, last_name, building_number, street, city, state, passport_num, passport_exp_d, passport_exp_m, passport_exp_y, passport_country, dob_d, dob_m, dob_y))
#         conn.commit()
#
#     # use information to process the payment and purchase the flight
#     if round=='no':
#
#
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price = cursor.fetchone()['base_price']
#         price_staff = float(price) * 0.9
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         cursor.close()
#
#         return redirect(url_for('home_staff'))
#
#     else:
#         cursor = conn.cursor();
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price_dep = cursor.fetchone()['base_price']
#
#         price_dep_staff = float(price_dep) * 0.9
#
#         query6 = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query6, (flight_num_staffrr, airline_name_staffrr))
#         price_staffrr = cursor.fetchone()['base_price']
#         price_staffrr_staff = float(price_staffrr)*0.9
#
#         price = price_dep + price_staffrr
#         price_staff = price_dep_staff + price_staffrr_staff
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         return redirect(url_for('home_staff'))
#
# @app.route('/add_new_airport', methods=['GET', 'POST'])
# def add_new_airport():
#     email = session['email']
#     booking_staffgent_id = session['booking_staffgent_id']
#     if email==None:
#         print('Please login first to pay')
#         return render_template('login.html')
#
#     #get credit card information from the form
#     name = request.form['card_name']
#     card_number = request.form['card_number']
#     card_type = request.form['card_type']
#     security_code = request.form['security_code']
#     exp_month = request.form['exp_month']
#     exp_year = request.form['exp_year']
#
#     customer_email = request.form['email']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     building_number = request.form['building_number']
#     street = request.form['street']
#     city = request.form['city']
#     state = request.form['state']
#     passport_num = request.form['passport_num']
#     passport_exp_d = request.form['passport_exp_d']
#     passport_exp_m = request.form['passport_exp_m']
#     passport_exp_y = request.form['passport_exp_y']
#     passport_country = request.form['passport_country']
#     dob_d = request.form['dob_d']
#     dob_m = request.form['dob_m']
#     dob_y = request.form['dob_y']
#
#
#     #get details of the flight saved in the session
#     flight_num_dep= session['flight_num_dep']
#     airline_name_dep= session['airline_name_dep']
#     round= session['round_trip']
#     flight_num_staffrr= session['flight_num_staffrr']
#     airline_name_staffrr= session['airline_name_staffrr']
#     #price=session['price']
#     cursor = conn.cursor();
#     #card information
#     query0 = 'select email from customer where email = %s'
#     cursor.execute(query0, (customer_email))
#     data = cursor.fetchone()
#
#     if data == None:
#         ins = 'INSERT INTO customer(email, first_name, last_name, building_number, street, city, state, passport_number, passport_ex_day, passport_ex_month, passport_ex_year, passport_country, dob_day, dob_month, dob_year) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(ins, (customer_email, first_name, last_name, building_number, street, city, state, passport_num, passport_exp_d, passport_exp_m, passport_exp_y, passport_country, dob_d, dob_m, dob_y))
#         conn.commit()
#
#     # use information to process the payment and purchase the flight
#     if round=='no':
#
#
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price = cursor.fetchone()['base_price']
#         price_staff = float(price) * 0.9
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         cursor.close()
#
#         return redirect(url_for('home_staff'))
#
#     else:
#         cursor = conn.cursor();
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price_dep = cursor.fetchone()['base_price']
#
#         price_dep_staff = float(price_dep) * 0.9
#
#         query6 = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query6, (flight_num_staffrr, airline_name_staffrr))
#         price_staffrr = cursor.fetchone()['base_price']
#         price_staffrr_staff = float(price_staffrr)*0.9
#
#         price = price_dep + price_staffrr
#         price_staff = price_dep_staff + price_staffrr_staff
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         return redirect(url_for('home_staff'))
#
# @app.route('/view_all_booking_agents', methods=['GET', 'POST'])
# def view_all_booking_agents():
#     email = session['email']
#     booking_staffgent_id = session['booking_staffgent_id']
#     if email==None:
#         print('Please login first to pay')
#         return render_template('login.html')
#
#     #get credit card information from the form
#     name = request.form['card_name']
#     card_number = request.form['card_number']
#     card_type = request.form['card_type']
#     security_code = request.form['security_code']
#     exp_month = request.form['exp_month']
#     exp_year = request.form['exp_year']
#
#     customer_email = request.form['email']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     building_number = request.form['building_number']
#     street = request.form['street']
#     city = request.form['city']
#     state = request.form['state']
#     passport_num = request.form['passport_num']
#     passport_exp_d = request.form['passport_exp_d']
#     passport_exp_m = request.form['passport_exp_m']
#     passport_exp_y = request.form['passport_exp_y']
#     passport_country = request.form['passport_country']
#     dob_d = request.form['dob_d']
#     dob_m = request.form['dob_m']
#     dob_y = request.form['dob_y']
#
#
#     #get details of the flight saved in the session
#     flight_num_dep= session['flight_num_dep']
#     airline_name_dep= session['airline_name_dep']
#     round= session['round_trip']
#     flight_num_staffrr= session['flight_num_staffrr']
#     airline_name_staffrr= session['airline_name_staffrr']
#     #price=session['price']
#     cursor = conn.cursor();
#     #card information
#     query0 = 'select email from customer where email = %s'
#     cursor.execute(query0, (customer_email))
#     data = cursor.fetchone()
#
#     if data == None:
#         ins = 'INSERT INTO customer(email, first_name, last_name, building_number, street, city, state, passport_number, passport_ex_day, passport_ex_month, passport_ex_year, passport_country, dob_day, dob_month, dob_year) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(ins, (customer_email, first_name, last_name, building_number, street, city, state, passport_num, passport_exp_d, passport_exp_m, passport_exp_y, passport_country, dob_d, dob_m, dob_y))
#         conn.commit()
#
#     # use information to process the payment and purchase the flight
#     if round=='no':
#
#
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price = cursor.fetchone()['base_price']
#         price_staff = float(price) * 0.9
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         cursor.close()
#
#         return redirect(url_for('home_staff'))
#
#     else:
#         cursor = conn.cursor();
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price_dep = cursor.fetchone()['base_price']
#
#         price_dep_staff = float(price_dep) * 0.9
#
#         query6 = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query6, (flight_num_staffrr, airline_name_staffrr))
#         price_staffrr = cursor.fetchone()['base_price']
#         price_staffrr_staff = float(price_staffrr)*0.9
#
#         price = price_dep + price_staffrr
#         price_staff = price_dep_staff + price_staffrr_staff
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         return redirect(url_for('home_staff'))
#
# @app.route('/view_freq_customers', methods=['GET', 'POST'])
# def view_freq_customers():
#     email = session['email']
#     booking_staffgent_id = session['booking_staffgent_id']
#     if email==None:
#         print('Please login first to pay')
#         return render_template('login.html')
#
#     #get credit card information from the form
#     name = request.form['card_name']
#     card_number = request.form['card_number']
#     card_type = request.form['card_type']
#     security_code = request.form['security_code']
#     exp_month = request.form['exp_month']
#     exp_year = request.form['exp_year']
#
#     customer_email = request.form['email']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     building_number = request.form['building_number']
#     street = request.form['street']
#     city = request.form['city']
#     state = request.form['state']
#     passport_num = request.form['passport_num']
#     passport_exp_d = request.form['passport_exp_d']
#     passport_exp_m = request.form['passport_exp_m']
#     passport_exp_y = request.form['passport_exp_y']
#     passport_country = request.form['passport_country']
#     dob_d = request.form['dob_d']
#     dob_m = request.form['dob_m']
#     dob_y = request.form['dob_y']
#
#
#     #get details of the flight saved in the session
#     flight_num_dep= session['flight_num_dep']
#     airline_name_dep= session['airline_name_dep']
#     round= session['round_trip']
#     flight_num_staffrr= session['flight_num_s']
#     airline_name_staffrr= session['airline_name_s']
#     #price=session['price']
#     cursor = conn.cursor();
#     #card information
#     query0 = 'select email from customer where email = %s'
#     cursor.execute(query0, (customer_email))
#     data = cursor.fetchone()
#
#     if data == None:
#         ins = 'INSERT INTO customer(email, first_name, last_name, building_number, street, city, state, passport_number, passport_ex_day, passport_ex_month, passport_ex_year, passport_country, dob_day, dob_month, dob_year) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(ins, (customer_email, first_name, last_name, building_number, street, city, state, passport_num, passport_exp_d, passport_exp_m, passport_exp_y, passport_country, dob_d, dob_m, dob_y))
#         conn.commit()
#
#     # use information to process the payment and purchase the flight
#     if round=='no':
#
#
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price = cursor.fetchone()['base_price']
#         price_staff = float(price) * 0.9
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         cursor.close()
#
#         return redirect(url_for('home_staff'))
#
#     else:
#         cursor = conn.cursor();
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price_dep = cursor.fetchone()['base_price']
#
#         price_dep_staff = float(price_dep) * 0.9
#
#         query6 = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query6, (flight_num_staffrr, airline_name_staffrr))
#         price_staffrr = cursor.fetchone()['base_price']
#         price_staffrr_staff = float(price_staffrr)*0.9
#
#         price = price_dep + price_staffrr
#         price_staff = price_dep_staff + price_staffrr_staff
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         return redirect(url_for('home_staff'))
#
# @app.route('/view_reports', methods=['GET', 'POST'])
# def view_reports():
#     email = session['email']
#     booking_staffgent_id = session['booking_staffgent_id']
#     if email==None:
#         print('Please login first to pay')
#         return render_template('login.html')
#
#     #get credit card information from the form
#     name = request.form['card_name']
#     card_number = request.form['card_number']
#     card_type = request.form['card_type']
#     security_code = request.form['security_code']
#     exp_month = request.form['exp_month']
#     exp_year = request.form['exp_year']
#
#     customer_email = request.form['email']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     building_number = request.form['building_number']
#     street = request.form['street']
#     city = request.form['city']
#     state = request.form['state']
#     passport_num = request.form['passport_num']
#     passport_exp_d = request.form['passport_exp_d']
#     passport_exp_m = request.form['passport_exp_m']
#     passport_exp_y = request.form['passport_exp_y']
#     passport_country = request.form['passport_country']
#     dob_d = request.form['dob_d']
#     dob_m = request.form['dob_m']
#     dob_y = request.form['dob_y']
#
#
#     #get details of the flight saved in the session
#     flight_num_dep= session['flight_num_dep']
#     airline_name_dep= session['airline_name_dep']
#     round= session['round_trip']
#     flight_num_staffrr= session['flight_num_staffrr']
#     airline_name_staffrr= session['airline_name_staffrr']
#     #price=session['price']
#     cursor = conn.cursor();
#     #card information
#     query0 = 'select email from customer where email = %s'
#     cursor.execute(query0, (customer_email))
#     data = cursor.fetchone()
#
#     if data == None:
#         ins = 'INSERT INTO customer(email, first_name, last_name, building_number, street, city, state, passport_number, passport_ex_day, passport_ex_month, passport_ex_year, passport_country, dob_day, dob_month, dob_year) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(ins, (customer_email, first_name, last_name, building_number, street, city, state, passport_num, passport_exp_d, passport_exp_m, passport_exp_y, passport_country, dob_d, dob_m, dob_y))
#         conn.commit()
#
#     # use information to process the payment and purchase the flight
#     if round=='no':
#
#
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price = cursor.fetchone()['base_price']
#         price_staff = float(price) * 0.9
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         cursor.close()
#
#         return redirect(url_for('home_staff'))
#
#     else:
#         cursor = conn.cursor();
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price_dep = cursor.fetchone()['base_price']
#
#         price_dep_staff = float(price_dep) * 0.9
#
#         query6 = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query6, (flight_num_staffrr, airline_name_staffrr))
#         price_staffrr = cursor.fetchone()['base_price']
#         price_staffrr_staff = float(price_staffrr)*0.9
#
#         price = price_dep + price_staffrr
#         price_staff = price_dep_staff + price_staffrr_staff
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         return redirect(url_for('home_staff'))
#
# @app.route('/comparision_of_revenue', methods=['GET', 'POST'])
# def comparision_of_revenue():
#     email = session['email']
#     booking_staffgent_id = session['booking_staffgent_id']
#     if email==None:
#         print('Please login first to pay')
#         return render_template('login.html')
#
#     #get credit card information from the form
#     name = request.form['card_name']
#     card_number = request.form['card_number']
#     card_type = request.form['card_type']
#     security_code = request.form['security_code']
#     exp_month = request.form['exp_month']
#     exp_year = request.form['exp_year']
#
#     customer_email = request.form['email']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     building_number = request.form['building_number']
#     street = request.form['street']
#     city = request.form['city']
#     state = request.form['state']
#     passport_num = request.form['passport_num']
#     passport_exp_d = request.form['passport_exp_d']
#     passport_exp_m = request.form['passport_exp_m']
#     passport_exp_y = request.form['passport_exp_y']
#     passport_country = request.form['passport_country']
#     dob_d = request.form['dob_d']
#     dob_m = request.form['dob_m']
#     dob_y = request.form['dob_y']
#
#
#     #get details of the flight saved in the session
#     flight_num_dep= session['flight_num_dep']
#     airline_name_dep= session['airline_name_dep']
#     round= session['round_trip']
#     flight_num_staffrr= session['flight_num_staffrr']
#     airline_name_staffrr= session['airline_name_staffrr']
#     #price=session['price']
#     cursor = conn.cursor();
#     #card information
#     query0 = 'select email from customer where email = %s'
#     cursor.execute(query0, (customer_email))
#     data = cursor.fetchone()
#
#     if data == None:
#         ins = 'INSERT INTO customer(email, first_name, last_name, building_number, street, city, state, passport_number, passport_ex_day, passport_ex_month, passport_ex_year, passport_country, dob_day, dob_month, dob_year) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(ins, (customer_email, first_name, last_name, building_number, street, city, state, passport_num, passport_exp_d, passport_exp_m, passport_exp_y, passport_country, dob_d, dob_m, dob_y))
#         conn.commit()
#
#     # use information to process the payment and purchase the flight
#     if round=='no':
#
#
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price = cursor.fetchone()['base_price']
#         price_staff = float(price) * 0.9
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         cursor.close()
#
#         return redirect(url_for('home_staff'))
#
#     else:
#         cursor = conn.cursor();
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price_dep = cursor.fetchone()['base_price']
#
#         price_dep_staff = float(price_dep) * 0.9
#
#         query6 = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query6, (flight_num_staffrr, airline_name_staffrr))
#         price_staffrr = cursor.fetchone()['base_price']
#         price_staffrr_staff = float(price_staffrr)*0.9
#
#         price = price_dep + price_staffrr
#         price_staff = price_dep_staff + price_staffrr_staff
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         return redirect(url_for('home_staff'))
#
# @app.route('/view_top_destinations', methods=['GET', 'POST'])
# def view_top_destinations():
#     email = session['email']
#     booking_staffgent_id = session['booking_staffgent_id']
#     if email==None:
#         print('Please login first to pay')
#         return render_template('login.html')
#
#     #get credit card information from the form
#     name = request.form['card_name']
#     card_number = request.form['card_number']
#     card_type = request.form['card_type']
#     security_code = request.form['security_code']
#     exp_month = request.form['exp_month']
#     exp_year = request.form['exp_year']
#
#     customer_email = request.form['email']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     building_number = request.form['building_number']
#     street = request.form['street']
#     city = request.form['city']
#     state = request.form['state']
#     passport_num = request.form['passport_num']
#     passport_exp_d = request.form['passport_exp_d']
#     passport_exp_m = request.form['passport_exp_m']
#     passport_exp_y = request.form['passport_exp_y']
#     passport_country = request.form['passport_country']
#     dob_d = request.form['dob_d']
#     dob_m = request.form['dob_m']
#     dob_y = request.form['dob_y']
#
#
#     #get details of the flight saved in the session
#     flight_num_dep= session['flight_num_dep']
#     airline_name_dep= session['airline_name_dep']
#     round= session['round_trip']
#     flight_num_staffrr= session['flight_num_staffrr']
#     airline_name_staffrr= session['airline_name_staffrr']
#     #price=session['price']
#     cursor = conn.cursor();
#     #card information
#     query0 = 'select email from customer where email = %s'
#     cursor.execute(query0, (customer_email))
#     data = cursor.fetchone()
#
#     if data == None:
#         ins = 'INSERT INTO customer(email, first_name, last_name, building_number, street, city, state, passport_number, passport_ex_day, passport_ex_month, passport_ex_year, passport_country, dob_day, dob_month, dob_year) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(ins, (customer_email, first_name, last_name, building_number, street, city, state, passport_num, passport_exp_d, passport_exp_m, passport_exp_y, passport_country, dob_d, dob_m, dob_y))
#         conn.commit()
#
#     # use information to process the payment and purchase the flight
#     if round=='no':
#
#
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price = cursor.fetchone()['base_price']
#         price_staff = float(price) * 0.9
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         cursor.close()
#
#         return redirect(url_for('home_staff'))
#
#     else:
#         cursor = conn.cursor();
#         from random import randint
#         ticket_number= str(randint(10000, 99999))
#         payment_number = str(randint(10000000, 99999999))
#
#         query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query, (flight_num_dep, airline_name_dep))
#         price_dep = cursor.fetchone()['base_price']
#
#         price_dep_staff = float(price_dep) * 0.9
#
#         query6 = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
#         cursor.execute(query6, (flight_num_staffrr, airline_name_staffrr))
#         price_staffrr = cursor.fetchone()['base_price']
#         price_staffrr_staff = float(price_staffrr)*0.9
#
#         price = price_dep + price_staffrr
#         price_staff = price_dep_staff + price_staffrr_staff
#
#         query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
#         cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))
#
#         query2 = 'insert into buys(ticket_id, customer_email, booking_staffgent_id) values (%s, %s, %s)'
#         cursor.execute(query2, (ticket_number, customer_email, booking_staffgent_id))
#
#         query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
#         cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))
#
#         query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
#         cursor.execute(query4, (ticket_number, payment_number))
#
#         conn.commit()
#         return redirect(url_for('home_staff'))

#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    # app.run('127.0.0.1', 5000)
    app.run(debug=True)

from app_a import *
