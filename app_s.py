from app import *



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
	#executes query

	query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register_s.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff(username, password, first_name, last_name, airline_name) VALUES(%s, %s, %s,%s,%s)'
		cursor.execute(ins, (username, password, first_name, last_name, airline_name))
		conn.commit()
		cursor.close()
		return render_template('login_s.html')

#

@app.route('/home_s')
def home_s():
    # global search
    email= session['username']
    if email==None:
        error = "Please login first"
        return render_template('login_s.html', error = error)

    return render_template('view_my_flights_s.html',email=email, data=[{'temp':1}])


@app.route('/view_my_flights_s', methods=['GET', 'POST'])
def view_my_flights_s():
    username = session['username']
    cursor = conn.cursor()

    query = 'SELECT airline_name FROM airline_staff where username = %s'

    cursor.execute(query, (username))
    airline_name = cursor.fetchone()
    cursor.close()

    query = 'SELECT flight_num, status, airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight where airline_name = %s'

    cursor.execute(query, (airline_name))
    data = cursor.fetchall()
    cursor.close()

    return render_template('view_my_flights_s.html', username=username, flights=data)


@app.route('/search_s', methods=['GET', 'POST'])
def search_s():
    # global search
    src_sirport = request.form['src_sirport']
    des_sirport = request.form['des_sirport']
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
        #query = 'SELECT * FROM flight WHERE departure_sirport = %s and arrival_sirport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        query = 'SELECT flight_num, flight.airline_name, departure_sirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_sirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status, num_of_seats FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE departure_sirport = %s and arrival_sirport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        #select (num_of_seats - (select count(flight_num) from buys natural join ticket natural join flight natural join airplane where flight_num = %s)) as available_seats
        #from airplane, flight where airplane.id = flight.airplane_id and airplane.airline_name = flight.airline_name and flight.flight_num = %s


        cursor.execute(query, (src_sirport, des_sirport, departure_d, departure_m, departure_y))
    	#stores the results in a variable
        data = cursor.fetchall()
    	#use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        print(data)
        if(data):
            return render_template('home_s.html', error='', flights_departure=data, flights_srrival=[])
        else:
    		#returns an error message to the html page
            message = 'No Tickets available'
            return render_template('home_s.html', error=message)
    else:
        #executes query
        query = 'SELECT flight_num, flight.airline_name, departure_sirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_sirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status, num_of_seats FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE departure_sirport = %s and arrival_sirport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        #select (num_of_seats - (select count(flight_num) from buys natural join ticket natural join flight natural join airplane where flight_num = %s)) as available_seats
        #from airplane, flight where airplane.id = flight.airplane_id and airplane.airline_name = flight.airline_name and flight.flight_num = %s


        cursor.execute(query, (src_sirport, des_sirport, departure_d, departure_m, departure_y ))
    	#stores the results in a variable
        data_deparature = cursor.fetchall()
        #use fetchall() if you are expecting more than 1 data row

        # arrival
        query = 'SELECT flight_num, flight.airline_name, departure_sirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_sirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status, num_of_seats FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE departure_sirport = %s and arrival_sirport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        #select (num_of_seats - (select count(flight_num) from buys natural join ticket natural join flight natural join airplane where flight_num = %s)) as available_seats
        #from airplane, flight where airplane.id = flight.airplane_id and airplane.airline_name = flight.airline_name and flight.flight_num = %s


        cursor.execute(query, (des_sirport, src_sirport, arrival_d, arrival_m, arrival_y ))
    	#stores the results in a variable
        data_srrival = cursor.fetchall()

        cursor.close()
        error = None
        if(data_deparature):
            return render_template('home_s.html', error='', flights_departure=data_deparature, flights_srrival=data_srrival)
        else:
            #returns an error message to the html page
            message = 'No Tickets available'
            return render_template('home_s.html', error=message, flighs=[])


@app.route('/purchase_ticket_s', methods=['GET', 'POST'])
def purchase_ticket_s():
    email = session['email']
    if email==None:
        return render_template('login_s.html')


    #get the flight number
    flight_num_dep = request.form['flight_num_dep']
    airline_name_dep = request.form["airline_name_dep"]


    round='no'
    try:
        flight_num_srr = request.form['flight_num_srr']
        airline_name_srr = request.form["airline_name_srr"]
        round='yes'
        #print(flight_num_srr)
    except:
        round='no'

    cursor = conn.cursor()
    if round=='yes':
        flight_num_srr = request.form['flight_num_srr']

        query = 'SELECT flight_num, flight.airline_name, departure_sirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_sirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
        cursor.execute(query, (flight_num_dep, airline_name_dep))

        #use fetchall() if you are expecting more than 1 data row
        dep_data = cursor.fetchone()

        query = 'SELECT flight_num, flight.airline_name, departure_sirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_sirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
        cursor.execute(query, (flight_num_srr, airline_name_srr))
        #stores the results in a variable
        arr_data = cursor.fetchone()
        cursor.close()

        #save the flight number in the session
        session['flight_num_dep'] = flight_num_dep
        session['airline_name_dep'] = airline_name_dep
        session['round_trip'] = round
        session['flight_num_srr'] = flight_num_srr
        session['airline_name_srr'] = airline_name_srr
        # get information of the flight and send to the payment page to ask for credit card information
        cursor = conn.cursor();
        # print(dep_data)
        price=arr_data['base_price'] + dep_data['base_price']
        #session['price'] = price

        return render_template('purchase_ticket_s.html', flight_dep=[dep_data], flight_srr=[arr_data], price=price)

    else:
        query = 'SELECT flight_num, flight.airline_name, departure_sirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_sirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
        cursor.execute(query, (flight_num_dep, airline_name_dep))
        #stores the results in a variable

        #use fetchall() if you are expecting more than 1 data row
        dep_data = cursor.fetchone()
        cursor.close()

        #save the flight number in the session
        session['flight_num_dep'] = flight_num_dep
        session['airline_name_dep'] = airline_name_dep
        session['round_trip'] = round
        session['flight_num_srr'] = 'None'
        session['airline_name_srr'] = 'None'

        # get information of the flight and send to the payment page to ask for credit card information
        cursor = conn.cursor();
        price=dep_data['base_price']
        #session['price'] = price
        return render_template('purchase_ticket_c.html', flight_dep=[dep_data], flight_srr=[], price=price)


@app.route('/payment_s', methods=['GET', 'POST'])
def payment_s():
    email = session['email']
    booking_sgent_id = session['booking_sgent_id']
    if email==None:
        print('Please login first to pay')
        return render_template('login.html')

    #get credit card information from the form
    name = request.form['card_name']
    card_number = request.form['card_number']
    card_type = request.form['card_type']
    security_code = request.form['security_code']
    exp_month = request.form['exp_month']
    exp_year = request.form['exp_year']

    customer_email = request.form['email']
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


    #get details of the flight saved in the session
    flight_num_dep= session['flight_num_dep']
    airline_name_dep= session['airline_name_dep']
    round= session['round_trip']
    flight_num_srr= session['flight_num_srr']
    airline_name_srr= session['airline_name_srr']
    #price=session['price']
    cursor = conn.cursor();
    #card information
    query0 = 'select email from customer where email = %s'
    cursor.execute(query0, (customer_email))
    data = cursor.fetchone()

    if data == None:
        ins = 'INSERT INTO customer(email, first_name, last_name, building_number, street, city, state, passport_number, passport_ex_day, passport_ex_month, passport_ex_year, passport_country, dob_day, dob_month, dob_year) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (customer_email, first_name, last_name, building_number, street, city, state, passport_num, passport_exp_d, passport_exp_m, passport_exp_y, passport_country, dob_d, dob_m, dob_y))
        conn.commit()

    # use information to process the payment and purchase the flight
    if round=='no':


        from random import randint
        ticket_number= str(randint(10000, 99999))
        payment_number = str(randint(10000000, 99999999))


        query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
        cursor.execute(query, (flight_num_dep, airline_name_dep))
        price = cursor.fetchone()['base_price']
        price_s = float(price) * 0.9

        query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
        cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))

        query2 = 'insert into buys(ticket_id, customer_email, booking_sgent_id) values (%s, %s, %s)'
        cursor.execute(query2, (ticket_number, customer_email, booking_sgent_id))


        query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))


        query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
        cursor.execute(query4, (ticket_number, payment_number))

        conn.commit()
        cursor.close()

        return redirect(url_for('home_s'))

    else:
        cursor = conn.cursor();
        from random import randint
        ticket_number= str(randint(10000, 99999))
        payment_number = str(randint(10000000, 99999999))

        query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
        cursor.execute(query, (flight_num_dep, airline_name_dep))
        price_dep = cursor.fetchone()['base_price']

        price_dep_s = float(price_dep) * 0.9

        query6 = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
        cursor.execute(query6, (flight_num_srr, airline_name_srr))
        price_srr = cursor.fetchone()['base_price']
        price_srr_s = float(price_srr)*0.9

        price = price_dep + price_srr
        price_s = price_dep_s + price_srr_s

        query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
        cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))

        query2 = 'insert into buys(ticket_id, customer_email, booking_sgent_id) values (%s, %s, %s)'
        cursor.execute(query2, (ticket_number, customer_email, booking_sgent_id))

        query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))

        query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
        cursor.execute(query4, (ticket_number, payment_number))

        conn.commit()
        return redirect(url_for('home_s'))




@app.route('/view_my_commissions_s', methods=['GET', 'POST'])
def view_my_commissions_s():
    email = session['email']
    cursor = conn.cursor()

    query = 'SELECT flight_num, status, airline_name, departure_sirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_sirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM buys natural join ticket natural join flight where customer_email = %s'

    cursor.execute(query, (email))
    data = cursor.fetchall()
    cursor.close()

    return render_template('view_my_commissions_s.html', username=email, flights=data)


@app.route('/view_top_customers_s', methods=['GET', 'POST'])
def view_top_customers_s():
    email = session['email']

    cursor = conn.cursor()

    query = 'SELECT flight_num, status, airline_name, departure_sirport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_sirport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM buys natural join ticket natural join flight where customer_email = %s'

    cursor.execute(query, (email))
    data = cursor.fetchall()
    cursor.close()

    return render_template('view_top_customers_s.html', username=email, flights=data)
