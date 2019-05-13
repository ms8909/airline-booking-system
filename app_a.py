from app import *



@app.route('/login_a')
def login_a():
	return render_template('login_a.html')

#Define route for register
@app.route('/register_a')
def register_a():
	return render_template('register_a.html')

#Authenticates the login
@app.route('/loginAuth_a', methods=['GET', 'POST'])
def loginAuth_a():
	email = request.form['email']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']
	cursor = conn.cursor()
	query = 'SELECT password FROM booking_agent WHERE email = %s'
	cursor.execute(query, (email))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		result= check_password_hash(data['password'],password)
		if result==False:
			error = 'Invalid login or username'
			return render_template('login_a.html', error=error)
		else:
			session['email'] = email
			session['booking_agent_id'] = booking_agent_id
			return redirect(url_for('home_a'))
	else:
		error = 'Invalid login or username'
		return render_template('login_c.html', error=error)

#Authenticates the register
@app.route('/registerAuth_a', methods=['GET', 'POST'])
def registerAuth_a():
	#grabs information from the forms
	email = request.form['email']
	password = request. form['password']
	booking_agent_id= request.form['booking_agent_id']
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM booking_agent WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		error = "This user already exists"
		return render_template('register_a.html', error = error)
	else:
		password = generate_password_hash(password)
		ins = 'INSERT INTO booking_agent(email, password, booking_agent_id) VALUES(%s, %s, %s)'
		cursor.execute(ins, (email, password, booking_agent_id))
		conn.commit()
		cursor.close()
		return render_template('login_a.html')

#

@app.route('/home_a')
def home_a():
    # global search
    email= session['email']
    if email==None:
        error = "Please login first"
        return render_template('login_a.html', error = error)

    return render_template('home_a.html',email=email, data=[{'temp':1}])



@app.route('/search_a', methods=['GET', 'POST'])
def search_a():
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
            return render_template('home_a.html', error='', flights_departure=data, flights_arrival=[])
        else:
    		#returns an error message to the html page
            message = 'No Tickets available'
            return render_template('home_a.html', error=message)
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
            return render_template('home_a.html', error='', flights_departure=data_deparature, flights_arrival=data_arrival)
        else:
            #returns an error message to the html page
            message = 'No Tickets available'
            return render_template('home_a.html', error=message, flighs=[])


@app.route('/purchase_ticket_a', methods=['GET', 'POST'])
def purchase_ticket_a():
    email = session['email']
    if email==None:
        return render_template('login_a.html')


    #get the flight number
    flight_num_dep = request.form['flight_num_dep']
    airline_name_dep = request.form["airline_name_dep"]


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

        return render_template('purchase_ticket_a.html', flight_dep=[dep_data], flight_arr=[arr_data], price=price)

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
        return render_template('purchase_ticket_a.html', flight_dep=[dep_data], flight_arr=[], price=price)


@app.route('/payment_a', methods=['GET', 'POST'])
def payment_a():
    email = session['email']
    booking_agent_id = session['booking_agent_id']
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
    flight_num_arr= session['flight_num_arr']
    airline_name_arr= session['airline_name_arr']
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
        price_a = float(price) * 0.9

        query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
        cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))

        query2 = 'insert into buys(ticket_id, customer_email, booking_agent_id) values (%s, %s, %s)'
        cursor.execute(query2, (ticket_number, customer_email, booking_agent_id))


        query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))


        query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
        cursor.execute(query4, (ticket_number, payment_number))

        conn.commit()
        cursor.close()

        return redirect(url_for('home_a'))

    else:
        cursor = conn.cursor();
        from random import randint
        ticket_number= str(randint(10000, 99999))
        payment_number = str(randint(10000000, 99999999))

        query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
        cursor.execute(query, (flight_num_dep, airline_name_dep))
        price_dep = cursor.fetchone()['base_price']

        price_dep_a = float(price_dep) * 0.9

        query6 = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
        cursor.execute(query6, (flight_num_arr, airline_name_arr))
        price_arr = cursor.fetchone()['base_price']
        price_arr_a = float(price_arr)*0.9

        price = price_dep + price_arr
        price_a = price_dep_a + price_arr_a

        query1 = 'insert into ticket(ticket_id, flight_num, airline_name) values (%s, %s, %s)'
        cursor.execute(query1, (ticket_number, flight_num_dep, airline_name_dep))

        query2 = 'insert into buys(ticket_id, customer_email, booking_agent_id) values (%s, %s, %s)'
        cursor.execute(query2, (ticket_number, customer_email, booking_agent_id))

        query3 = 'insert into payment(payment_num, card_type, card_number, card_name, security_code, expiration_month, expiration_year, sold_price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query3, (payment_number, card_type, card_number, name, security_code, exp_month, exp_year, price))

        query4 = 'insert into paid(ticket_id, payment_num) values (%s, %s)'
        cursor.execute(query4, (ticket_number, payment_number))

        conn.commit()
        return redirect(url_for('home_a'))




@app.route('/view_my_commissions_a', methods=['GET', 'POST'])
def view_my_commissions_a():
	email = session['email']
	booking_agent_id = session['booking_agent_id']
	cursor = conn.cursor()
	try:
		start_date = request.form['start_date']
		end_date = request.form['end_date']
		start_date= start_date+' 00:00:00'
		end_date= end_date+' 00:00:00'

		#total amount of commissions last 30 days
		query0 = 'SELECT sum(sold_price*0.1) as sum FROM buys natural join paid natural join payment where payment_time >= %s and payment_time<=  %s and booking_agent_id = %s'
		cursor.execute(query0, (booking_agent_id))
		total_com = cursor.fetchone()['sum']
		#average commission last 30 days
		query1 = 'SELECT avg(sold_price*0.1) as average FROM buys natural join paid natural join payment where payment_time >= %s and payment_time<=  %s and booking_agent_id = %s'
		cursor.execute(query1, (booking_agent_id))
		avg_com = cursor.fetchone()['average']
		#total number of tickets sold last 30 days
		query2 = 'SELECT count(ticket_id) as count FROM buys natural join paid natural join payment where payment_time >= %s and payment_time<=  %s and booking_agent_id = %s'
		cursor.execute(query2, (booking_agent_id))
		count = cursor.fetchone()['count']

	except:
		#total amount of commissions last 30 days
		query0 = 'SELECT sum(sold_price*0.1) as sum FROM buys natural join paid natural join payment where payment_time >= date_sub(now(), interval 1 month) and booking_agent_id = %s'
		cursor.execute(query0, (booking_agent_id))
		total_com = cursor.fetchone()['sum']
		#average commission last 30 days
		query1 = 'SELECT avg(sold_price*0.1) as average FROM buys natural join paid natural join payment where payment_time >= date_sub(now(), interval 1 month) and booking_agent_id = %s'
		cursor.execute(query1, (booking_agent_id))
		avg_com = cursor.fetchone()['average']
		#total number of tickets sold last 30 days
		query2 = 'SELECT count(ticket_id) as count FROM buys natural join paid natural join payment where payment_time >= date_sub(now(), interval 1 month) and booking_agent_id = %s'
		cursor.execute(query2, (booking_agent_id))
		count = cursor.fetchone()['count']

	cursor.close()

	return render_template('view_my_commissions_a.html', username=email, total_com=total_com, avg_com = avg_com, count=count)


@app.route('/view_top_customers_a', methods=['GET', 'POST'])
def view_top_customers_a():
	email = session['email']
	booking_agent_id = session['booking_agent_id']

	cursor = conn.cursor()

	#view top customers based on number of tickets
	query = 'SELECT customer_email, count(customer_email) as count FROM buys natural join paid natural join payment where payment_time >= date_sub(now(), interval 6 month) and booking_agent_id = %s Group by customer_email order by count desc limit 5'
	cursor.execute(query, (booking_agent_id))
	top5 = cursor.fetchall()
	#top5y = cursor.fetchall()['count']

	top5x=[]
	top5y=[]
	for i  in top5:
		top5x.append(i['customer_email'])
		top5y.append(i['count'])



	#view top customers based on amount of commissions
	query = 'SELECT customer_email, sum(sold_price*0.1) as sum FROM buys natural join paid natural join payment where payment_time >= date_sub(now(), interval 12 month) and booking_agent_id = %s group by customer_email order by sum desc limit 5'
	cursor.execute(query, (booking_agent_id))
	top5comm = cursor.fetchall()

	top5commx=[]
	top5commy=[]
	print(top5comm)

	for k in top5comm:
		top5commx.append(k['customer_email'])
		top5commy.append(float(k['sum']))

	return render_template('view_top_customers_a.html', username=email, top5x=top5x, top5y=top5y, top5commx= top5commx, top5commy= top5commy)


@app.route('/view_my_flights_a', methods=['GET', 'POST'])
def view_my_flights_a():
	email = session['email']
	booking_agent_id = session['booking_agent_id']
	cursor = conn.cursor()
	query = 'SELECT email FROM booking_agent where email = %s'
	cursor.execute(query, (email))
	data = cursor.fetchone()
	if data==None:
		error = "Please login first"
		return render_template('login_a.html', error = error)
	query = 'SELECT flight_num, status, customer_email, airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM buys natural join ticket natural join flight where booking_agent_id = %s'
	cursor.execute(query, (booking_agent_id))
	flights = cursor.fetchall()
	cursor.close()
	return render_template('view_my_flights_a.html', username=email, flights=flights)
