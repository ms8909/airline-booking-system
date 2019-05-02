#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)
#Configure MySQL
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

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

#Define route for login
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
	query = 'SELECT * FROM customer WHERE email = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home_customer'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login_c.html', error=error)

#Authenticates the register
@app.route('/registerAuth_c', methods=['GET', 'POST'])
def registerAuth_c():
	#grabs information from the forms
    email = request.form['email']
    password = request. form['password']
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
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, password, first_name, last_name, building_number, street, city, state, passport_num, passport_exp_d, passport_exp_m, passport_exp_y, passport_country, dob_d, dob_m, dob_y))
        conn.commit()
        cursor.close()
        return render_template('login_c.html')


@app.route('/')
def home():
    # global search
    return render_template('home.html',data=[{'temp':1}])


@app.route('/home_customer')
def home_customer():
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


        cursor.execute(query, (src_airport, des_airport, departure_d, departure_m, departure_y, ))
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
        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status, num_of_seats FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE departure_airport = %s and arrival_airport = %s and departure_day = %s and departure_month = %s and departure_year %s'
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


    return render_template('view_my_flights_c.html', username=username, flights=[])

    cursor.close()
    return render_template('view_my_flights_c.html', username=username, flights=[])


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
    print('airline_name_dep', airline_name_dep)
    print("json",request.form['flight_num_dep'] )
    print(flight_num_dep)

    round='no'
    try:
        flight_num_arr = request.form['flight_num_arr']
        airline_name_arr = request.form["airline_name_arr"]
        round='yes'
        print(flight_num_arr)
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
        return render_template('purchase_ticket_c.html', flight_dep=dep_data, flight_arr=[], price=price)


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



        return render_template('view_my_flights.html')
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
        return render_template('home.html')


@app.route('/track_my_spending_c', methods=['GET', 'POST'])
def track_my_spending_c():
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)




@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'

#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000)
