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
    username = request.form['username']
    password = request.form['password']
    cursor = conn.cursor()
    query = 'SELECT password FROM customer WHERE email = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    error = None
    if(data):
        result= check_password_hash(data['password'],password)
        if result==False:
            error = 'Invalid login or username'
            return render_template('login_c.html', error=error)
        else:
            session['username'] = username
            return redirect(url_for('home_c'))
    else:
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
        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE departure_airport = %s and arrival_airport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
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
            for d in data:
                querycount = 'SELECT count(ticket_id) as c from ticket where flight_num= %s and airline_name= %s'
                cursor.execute(querycount, (d['flight_num'], d['airline_name']))
                count = cursor.fetchone()
                print(count)
                queryprice = 'SELECT base_price from flight where flight_num= %s and airline_name= %s'
                cursor.execute(queryprice, (d['flight_num'], d['airline_name']))
                price = cursor.fetchone()
                print(price)

                queryseats = 'SELECT num_of_seats from flight, airplane where airplane_id=id and flight_num= %s and flight.airline_name= %s'
                cursor.execute(queryprice, (d['flight_num'], d['airline_name']))
                seats = cursor.fetchone()
                print(seats)

                if count['c']/seats['num_of_seats'] >= .7:
                    d['price']= price['base_price']*1.20
                else:
                    d['price']= price['base_price']

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
        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE departure_airport = %s and arrival_airport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
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
            for d in data:
                querycount = 'SELECT count(ticket_id) as c from ticket where flight_num= %s and airline_name= %s'
                cursor.execute(querycount, (d['flight_num'], d['airline_name']))
                count = cursor.fetchone()
                print(count)
                queryprice = 'SELECT base_price from flight where flight_num= %s and airline_name= %s'
                cursor.execute(queryprice, (d['flight_num'], d['airline_name']))
                price = cursor.fetchone()
                print(price)

                queryseats = 'SELECT num_of_seats from flight, airplane where airplane_id=id and flight_num= %s and flight.airline_name= %s'
                cursor.execute(queryprice, (d['flight_num'], d['airline_name']))
                seats = cursor.fetchone()
                print(seats)

                if count['c']/seats['num_of_seats'] >= .7:
                    d['price']= price['base_price']*1.20
                else:
                    d['price']= price['base_price']

            return render_template('home_c.html', error='', flights_departure=data, flights_arrival=[])
        else:
            #returns an error message to the html page
            message = 'No Tickets available'
            return render_template('home_c.html', error=message)
    else:
        #executes query
        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE departure_airport = %s and arrival_airport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        #select (num_of_seats - (select count(flight_num) from buys natural join ticket natural join flight natural join airplane where flight_num = %s)) as available_seats
        #from airplane, flight where airplane.id = flight.airplane_id and airplane.airline_name = flight.airline_name and flight.flight_num = %s


        cursor.execute(query, (src_airport, des_airport, departure_d, departure_m, departure_y ))
        #stores the results in a variable
        data_deparature = cursor.fetchall()
        #use fetchall() if you are expecting more than 1 data row
        for d in data_deparature:
            querycount = 'SELECT count(ticket_id) as c from ticket where flight_num= %s and airline_name= %s'
            cursor.execute(querycount, (d['flight_num'], d['airline_name']))
            count = cursor.fetchone()
            print(count)
            queryprice = 'SELECT base_price from flight where flight_num= %s and airline_name= %s'
            cursor.execute(queryprice, (d['flight_num'], d['airline_name']))
            price = cursor.fetchone()
            print(price)

            queryseats = 'SELECT num_of_seats from flight, airplane where airplane_id=id and flight_num= %s and flight.airline_name= %s'
            cursor.execute(queryseats, (d['flight_num'], d['airline_name']))
            seats = cursor.fetchone()
            print(seats)

            if count['c']/seats['num_of_seats'] >= .7:
                d['price']= price['base_price']*1.20
            else:
                d['price']= price['base_price']


        # arrival
        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE departure_airport = %s and arrival_airport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        #select (num_of_seats - (select count(flight_num) from buys natural join ticket natural join flight natural join airplane where flight_num = %s)) as available_seats
        #from airplane, flight where airplane.id = flight.airplane_id and airplane.airline_name = flight.airline_name and flight.flight_num = %s


        cursor.execute(query, (des_airport, src_airport, arrival_d, arrival_m, arrival_y ))
        #stores the results in a variable
        data_arrival = cursor.fetchall()
        for d2 in data_arrival:
            querycount = 'SELECT count(ticket_id) as c from ticket where flight_num= %s and airline_name= %s'
            cursor.execute(querycount, (d2['flight_num'], d2['airline_name']))
            count = cursor.fetchone()
            print(count)
            queryprice = 'SELECT base_price from flight where flight_num= %s and airline_name= %s'
            cursor.execute(queryprice, (d2['flight_num'], d2['airline_name']))
            price = cursor.fetchone()
            print(price)

            queryseats = 'SELECT num_of_seats from flight, airplane where airplane_id=id and flight_num= %s and flight.airline_name= %s'
            cursor.execute(queryseats, (d2['flight_num'], d2['airline_name']))
            seats = cursor.fetchone()
            print(seats)

            if count['c']/seats['num_of_seats'] >= .7:
                print("1")
                d2['price']= price['base_price']*1.20
            else:
                print("2")
                d2['price']= price['base_price']

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
        querycount = 'SELECT count(ticket_id) as c from ticket where flight_num= %s and airline_name= %s'
        cursor.execute(querycount, (dep_data['flight_num'], dep_data['airline_name']))
        count = cursor.fetchone()
        print(count)
        queryprice = 'SELECT base_price from flight where flight_num= %s and airline_name= %s'
        cursor.execute(queryprice, (dep_data['flight_num'], dep_data['airline_name']))
        price = cursor.fetchone()
        print(price)

        queryseats = 'SELECT num_of_seats from flight, airplane where airplane_id=id and flight_num= %s and flight.airline_name= %s'
        cursor.execute(queryseats, (dep_data['flight_num'], dep_data['airline_name']))
        seats = cursor.fetchone()
        print(seats)

        if count['c']/seats['num_of_seats'] >= .7:
            print("1")
            dep_data['base_price']= price['base_price']*1.20
        else:
            print("2")
            dep_data['base_price']= price['base_price']

        query = 'SELECT flight_num, flight.airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight join airplane on (airplane.id = flight.airplane_id) and (flight.airline_name = airplane.airline_name) WHERE flight_num = %s and flight.airline_name = %s'
        cursor.execute(query, (flight_num_arr, airline_name_arr))
        #stores the results in a variable
        arr_data = cursor.fetchone()

        querycount = 'SELECT count(ticket_id) as c from ticket where flight_num= %s and airline_name= %s'
        cursor.execute(querycount, (arr_data['flight_num'], arr_data['airline_name']))
        count = cursor.fetchone()
        print(count)
        queryprice = 'SELECT base_price from flight where flight_num= %s and airline_name= %s'
        cursor.execute(queryprice, (arr_data['flight_num'], arr_data['airline_name']))
        price = cursor.fetchone()
        print(price)

        queryseats = 'SELECT num_of_seats from flight, airplane where airplane_id=id and flight_num= %s and flight.airline_name= %s'
        cursor.execute(queryseats, (arr_data['flight_num'], arr_data['airline_name']))
        seats = cursor.fetchone()
        print(seats)

        if count['c']/seats['num_of_seats'] >= .7:
            print("1")
            arr_data['base_price']= price['base_price']*1.20
        else:
            print("2")
            arr_data['base_price']= price['base_price']
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
        querycount = 'SELECT count(ticket_id) as c from ticket where flight_num= %s and airline_name= %s'
        cursor.execute(querycount, (dep_data['flight_num'], dep_data['airline_name']))
        count = cursor.fetchone()
        print(count)
        queryprice = 'SELECT base_price from flight where flight_num= %s and airline_name= %s'
        cursor.execute(queryprice, (dep_data['flight_num'], dep_data['airline_name']))
        price = cursor.fetchone()
        print(price)

        queryseats = 'SELECT num_of_seats from flight, airplane where airplane_id=id and flight_num= %s and flight.airline_name= %s'
        cursor.execute(queryseats, (dep_data['flight_num'], dep_data['airline_name']))
        seats = cursor.fetchone()
        print(seats)

        if count['c']/seats['num_of_seats'] >= .7:
            print("1")
            dep_data['base_price']= price['base_price']*1.20
        else:
            print("2")
            dep_data['base_price']= price['base_price']

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

        # query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
        # cursor.execute(query, (flight_num_dep, airline_name_dep))
        # price = cursor.fetchone()['base_price']

        querycount = 'SELECT count(ticket_id) as c from ticket where flight_num= %s and airline_name= %s'
        cursor.execute(querycount, (flight_num_dep, airline_name_dep))
        count = cursor.fetchone()
        print(count)
        queryprice = 'SELECT base_price from flight where flight_num= %s and airline_name= %s'
        cursor.execute(queryprice, (flight_num_dep, airline_name_dep))
        price = cursor.fetchone()
        print(price)

        queryseats = 'SELECT num_of_seats from flight, airplane where airplane_id=id and flight_num= %s and flight.airline_name= %s'
        cursor.execute(queryseats, (flight_num_dep, airline_name_dep))
        seats = cursor.fetchone()
        print(seats)

        if count['c']/seats['num_of_seats'] >= .7:
            print("1")
            price= price['base_price']*1.20
        else:
            print("2")
            price= price['base_price']



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

        # query = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
        # cursor.execute(query, (flight_num_dep, airline_name_dep))
        # price_dep = cursor.fetchone()['base_price']
        querycount = 'SELECT count(ticket_id) as c from ticket where flight_num= %s and airline_name= %s'
        cursor.execute(querycount, (flight_num_dep, airline_name_dep))
        count = cursor.fetchone()
        print(count)
        queryprice = 'SELECT base_price from flight where flight_num= %s and airline_name= %s'
        cursor.execute(queryprice, (flight_num_dep, airline_name_dep))
        price = cursor.fetchone()
        print(price)

        queryseats = 'SELECT num_of_seats from flight, airplane where airplane_id=id and flight_num= %s and flight.airline_name= %s'
        cursor.execute(queryseats, (flight_num_dep, airline_name_dep))
        seats = cursor.fetchone()
        print(seats)

        if count['c']/seats['num_of_seats'] >= .7:
            print("1")
            price_dep= price['base_price']*1.20
        else:
            print("2")
            price_dep= price['base_price']


        # query6 = 'SELECT base_price FROM flight WHERE flight_num = %s and airline_name = %s'
        # cursor.execute(query6, (flight_num_arr, airline_name_arr))
        # price_arr = cursor.fetchone()['base_price']

        querycount = 'SELECT count(ticket_id) as c from ticket where flight_num= %s and airline_name= %s'
        cursor.execute(querycount, (flight_num_arr, airline_name_arr))
        count = cursor.fetchone()
        print(count)
        queryprice = 'SELECT base_price from flight where flight_num= %s and airline_name= %s'
        cursor.execute(queryprice, (flight_num_arr, airline_name_arr))
        price = cursor.fetchone()
        print(price)

        queryseats = 'SELECT num_of_seats from flight, airplane where airplane_id=id and flight_num= %s and flight.airline_name= %s'
        cursor.execute(queryseats, (flight_num_arr, airline_name_arr))
        seats = cursor.fetchone()
        print(seats)

        if count['c']/seats['num_of_seats'] >= .7:
            print("1")
            price_arr= price['base_price']*1.20
        else:
            print("2")
            price_arr= price['base_price']

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
    username = session['username']
    cursor = conn.cursor();

    try:
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        start_date= start_date+' 00:00:00'
        end_date= end_date+' 00:00:00'


        query1 = "SELECT sum(sold_price) as sum, CONCAT( YEAR( payment_time ) , '-', MONTH( payment_time ) ) AS thedate from buys natural join paid natural join payment where customer_email = %s and payment_time >= %s and payment_time<=  %s group by CONCAT( YEAR( payment_time ) , '-', MONTH( payment_time ) )"
        cursor.execute(query1, (username, start_date, end_date))
        data = cursor.fetchall()
    except:

        query1 = "SELECT sum(sold_price) as sum, CONCAT( YEAR( payment_time ) , '-', MONTH( payment_time ) ) AS thedate from buys natural join paid natural join payment where customer_email = %s and payment_time >= date_sub(now(), interval 6 month) group by CONCAT( YEAR( payment_time ) , '-', MONTH( payment_time ) )"
        cursor.execute(query1, (username))
        data = cursor.fetchall()

    query = 'SELECT sum(sold_price) as price from buys natural join paid natural join payment where customer_email = %s and payment_time >= date_sub(now(), interval 12 month)'
    cursor.execute(query, (username))
    data1 = cursor.fetchone()['price']
    print("Total price:", data1)

    l=[]    #labels
    p=[]    #price
    for k in data:
        l.append(k['thedate'])
        p.append(float(k['sum']))

    print("labels:", l)
    print("price:", p)

    #these are just to test the code
    labels = ['January','February','March','April','May','June','July','August']
    price = [10,9,8,7,6,4,7,8]

    cursor.close()
    return render_template('track_my_spending_c.html', username=username, price=data1, values=p, labels=l)




@app.route('/logout')
def logout():
    session.clear()
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
    query = 'SELECT password FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    cursor.close()
    error = None
    if(data):
        result= check_password_hash(data['password'],password)
        if result==False:
            error = 'Invalid login or username'
            return render_template('login_s.html', error=error)
        else:
            session['username'] = username
            return redirect(url_for('home_s'))
    else:
        error = 'Invalid login or username'
        return render_template('login_s.html', error=error)


#Authenticates the register
@app.route('/registerAuth_s', methods=['GET', 'POST'])
def registerAuth_s():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    airline_name = request.form['airline_name']
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
        password = generate_password_hash(password)
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

    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    session['airline_name'] = data

    return render_template('view_my_flights_s.html',username=username, data=[{'temp':1}])


@app.route('/view_my_flights_s', methods=['GET', 'POST'])
def view_my_flights_s():
    username = session['username']
    airline_name = session['airline_name']
    cursor = conn.cursor()

    query = 'SELECT username, airline_name FROM airline_staff where username = %s'

    cursor.execute(query, (username))
    data = cursor.fetchone()

    if data==None:
        error = "Please login first"
        return render_template('login_s.html', error = error)

    try:
        src = request.form['src_airport']
        des = request.form['des_airport']
        range1= True
    except:
        range1= False

    try:
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        # start_date= start_date+' 00:00:00'
        # end_date= end_date+' 00:00:00'
        range2= True
    except:
        range2= False

    if range1== False  and range2==False:
        query = 'SELECT flight_num, status, airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight where airline_name = %s'
        cursor.execute(query, (data['airline_name']))
    elif range1== True  and range2==False:
        query = 'SELECT flight_num, status, airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight where airline_name = %s and departure_airport= %s and arrival_airport= %s'
        cursor.execute(query, (data['airline_name'],src, des ))
    elif range1== False  and range2==True:
        query = 'SELECT flight_num, status, airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight where airline_name = %s and departure_year >= %s and  departure_year <= %s'
        cursor.execute(query, (data['airline_name'], start_date, end_date))
    else:
        query = 'SELECT flight_num, status, airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, base_price FROM flight where airline_name = %s and departure_airport= %s and arrival_airport= %s and departure_year >= %s and  departure_year <= %s'
        cursor.execute(query, (data['airline_name'],src, des, start_date, end_date))

    flights = cursor.fetchall()

    # get all the customers
    cursor.close()
    return render_template('view_my_flights_s.html', username=username, flights=flights)


@app.route('/view_customer_s', methods=['GET', 'POST'])
def view_customer_s():
    username = session['username']
    if username==None:
        return render_template('login_s.html')
    flight_num = request.form['flight_num']
    airline_name = request.form['airline_name']

    # run query based on flight number and airline name and send back the results
    cursor = conn.cursor()

    query = 'SELECT email, first_name, last_name, passport_number, dob_year from customer, buys, ticket where customer.email= buys.customer_email and buys.ticket_id= ticket.ticket_id and ticket.flight_num= %s  and ticket.airline_name= %s'

    cursor.execute(query, (flight_num,airline_name ))
    data = cursor.fetchall()

    return render_template('view_customers_s.html', customers=data)

@app.route('/change_flight_status_form', methods=['GET', 'POST'])
def change_flight_status_form():
    username = session['username']
    airline_name = session['airline_name']
    if username==None:
        return render_template('login_s.html')
    return render_template('change_flight_status.html', flights=[])


@app.route('/change_flight_status', methods=['GET', 'POST'])
def change_flight_status():
    username = session['username']
    airline_name = session['airline_name']

    if username==None:
        return render_template('login_s.html')

    #get the flight number
    flight_num = request.form['flight_num']
    new_status = request.form['new_status']
    cursor = conn.cursor()
    query = 'UPDATE flight SET status = %s WHERE flight_num = %s and airline_name = %s'
    cursor.execute(query, (new_status, flight_num, airline_name['airline_name']))
    conn.commit()

    cursor.close()

    return redirect(url_for('view_my_flights_s'))



@app.route('/create_new_flight_form', methods=['GET', 'POST'])
def create_new_flight_form():
    username = session['username']
    airline_name = session['airline_name']
    if username==None:
        return render_template('login_s.html')
    return render_template('create_new_flight.html', flights=[])



@app.route('/create_new_flight', methods=['GET', 'POST'])
def create_new_flight():
    username = session['username']
    airline_name = session['airline_name']

    #print("Airline name: ", airline_name['airline_name'])
    #print("Username: ", username)

    if username==None:
        return render_template('login_s.html')

    #create a new flight
    flight_num = request.form["flight_num"]
    airplane_id = request.form["airplane_id"]
    base_price = request.form["base_price"]
    departure_hour = request.form["departure_hour"]
    departure_min = request.form["departure_min"]
    departure_day = request.form["departure_day"]
    departure_month = request.form["departure_month"]
    departure_year = request.form["departure_year"]
    departure_airport = request.form["departure_airport"]
    arrival_hour = request.form["arrival_hour"]
    arrival_min = request.form["arrival_min"]
    arrival_day = request.form["arrival_day"]
    arrival_month = request.form["arrival_month"]
    arrival_year = request.form["arrival_year"]
    arrival_airport = request.form["arrival_airport"]
    status = request.form["status"]


    cursor = conn.cursor()

    query = 'INSERT INTO flight(flight_num, airline_name, airplane_id, base_price, departure_hour, departure_min, departure_day, departure_month, departure_year, departure_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, arrival_airport, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(query, (flight_num, airline_name['airline_name'], airplane_id, base_price, departure_hour, departure_min, departure_day, departure_month, departure_year, departure_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, arrival_airport, status))
    conn.commit()

    # query = 'SELECT * FROM flight where airline_name = %s'
    # cursor.execute(query, (airline_name))
    # flights = cursor.fetchall()
    cursor.close()

    # return render_template('create_new_flight.html', flights=[])
    return redirect(url_for('view_my_flights_s'))


@app.route('/add_airplane_form', methods=['GET', 'POST'])
def add_airplane_form():
    username = session['username']
    airline_name = session['airline_name']
    if username==None:
        return render_template('login_s.html')
    return render_template('add_airplane.html', flights=[])



@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
    username = session['username']
    airline_name = session['airline_name']

    if username==None:
        print('Please login first add airplane')
        return render_template('login_s.html')

    #get credit card information from the form
    airplane_id = request.form['airplane_id']
    num_of_seats = request.form['num_of_seats']

    cursor = conn.cursor()
    query = 'INSERT INTO airplane(id, airline_name, num_of_seats) VALUES (%s, %s, %s)'
    cursor.execute(query, (airplane_id, airline_name['airline_name'], num_of_seats))
    conn.commit()

    query = 'SELECT id, num_of_seats FROM airplane WHERE airline_name = %s'
    cursor.execute(query, (airline_name['airline_name']))
    flights = cursor.fetchall()
    cursor.close()
    return render_template('add_airplane.html', flights=flights)


@app.route('/add_airport_form', methods=['GET', 'POST'])
def add_airport_form():
    username = session['username']
    airline_name = session['airline_name']
    if username==None:
        return render_template('login_s.html')
    return render_template('add_airport.html', flights=[])



@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
    username = session['username']
    airline_name = session['airline_name']
    if username==None:
        print('Please login first to pay')
        return render_template('login_s.html')

    airport_id = request.form['airport_id']
    name = request.form['name']
    city = request.form['city']

    cursor = conn.cursor()
    query = 'INSERT INTO airport(id, name, city) VALUES (%s, %s, %s)'
    cursor.execute(query, (airport_id, name, city))
    conn.commit()

    query = 'SELECT * FROM airport'
    cursor.execute(query)
    flights = cursor.fetchall()
    cursor.close()

    return render_template('add_airport.html', flights=flights)


@app.route('/view_all_booking_agents', methods=['GET', 'POST'])
def view_all_booking_agents():
    username = session['username']
    airline_name = session['airline_name']
    if username==None:
        print('Please login first to pay')
        return render_template('login_s.html')

    cursor = conn.cursor()
    #top 5 booking agents based on num tickets sold for the last month
    query = 'SELECT buys.booking_agent_id FROM booking_agent, payment natural join paid natural join buys where payment_time >= date_sub(now(), interval 1 month) and buys.booking_agent_id = booking_agent.booking_agent_id group by buys.booking_agent_id order by count(ticket_id) desc limit 5'
    cursor.execute(query, ())
    top_agents_month = cursor.fetchall()
    print("top_agents_month", top_agents_month)
    #top 5 booking agents based on num tickets for the last year
    query = 'SELECT buys.booking_agent_id FROM booking_agent, payment natural join paid natural join buys where payment_time >= date_sub(now(), interval 12 month) and buys.booking_agent_id = booking_agent.booking_agent_id group by buys.booking_agent_id order by count(ticket_id) desc limit 5'
    cursor.execute(query, ())
    top_agents_year = cursor.fetchall()


    #top 5 booking agents based on commissions received for the last year
    query = 'SELECT buys.booking_agent_id FROM booking_agent, payment natural join paid natural join buys where payment_time >= date_sub(now(), interval 12 month) and buys.booking_agent_id = booking_agent.booking_agent_id group by buys.booking_agent_id order by sum(sold_price*0.1) desc limit 5'
    cursor.execute(query, ())
    top_agents_comm = cursor.fetchall()

    return render_template('view_all_booking_agents.html', top_agents_month=top_agents_month, top_agents_year=top_agents_year, top_agents_comm=top_agents_comm)


@app.route('/view_freq_customers', methods=['GET', 'POST'])
def view_freq_customers():
    username = session['username']
    airline_name = session['airline_name']
    if username==None:
        print('Please login first to pay')
        return render_template('login_s.html')

    cursor = conn.cursor()

    query = 'SELECT customer_email FROM ticket natural join buys natural join paid natural join payment where payment_time >= date_sub(now(), interval 12 month) and airline_name = %s GROUP BY customer_email ORDER BY COUNT(ticket_id) DESC limit 1'
    cursor.execute(query, (airline_name['airline_name']))
    customer = cursor.fetchone()

    query1 = 'SELECT flight_num, airline_name, departure_airport, departure_hour, departure_min, departure_day, departure_month, departure_year, arrival_airport, arrival_hour, arrival_min, arrival_day, arrival_month, arrival_year, status, base_price FROM buys natural join ticket natural join flight where customer_email = %s and airline_name = %s'
    cursor.execute(query1, (customer['customer_email'], airline_name['airline_name']))
    flights = cursor.fetchall()

    return render_template('view_freq_customers.html', customer=customer, flights = flights)


@app.route('/view_reports_form', methods=['GET', 'POST'])
def view_reports_form():
    username = session['username']
    airline_name = session['airline_name']
    if username==None:
        return render_template('login_s.html')
    return render_template('view_reports.html', flights=[])

@app.route('/view_reports', methods=['GET', 'POST'])
def view_reports():
    username = session['username']
    airline_name = session['airline_name']
    if username==None:
        return render_template('login_s.html')

    start_date = request.form['start_date']
    end_date = request.form['end_date']

    start_date= start_date+' 00:00:00'
    end_date= end_date+' 00:00:00'

    cursor = conn.cursor();

    query = "SELECT count(ticket_id) as count, CONCAT( YEAR( payment_time ) , '-', MONTH( payment_time ) ) AS thedate FROM ticket natural join paid natural join payment where payment_time between %s and %s and airline_name = %s group by CONCAT( YEAR( payment_time ) , '-', MONTH( payment_time ) )"
    cursor.execute(query, (start_date,end_date, airline_name['airline_name']))
    data = cursor.fetchall()

    l=[]    #labels
    p=[]    #price
    for k in data:
        l.append(k['thedate'])
        p.append(float(k['count']))

    count = 0
    for i in range(len(p)):
        count += int(p[i])

    print("labels:", l)
    print("price:", p)

    cursor.close()
    return render_template('view_reports.html', values=p, labels = l, count = count)


@app.route('/comparision_of_revenue', methods=['GET', 'POST'])
def comparision_of_revenue():
    username = session['username']
    airline_name = session['airline_name']
    if username==None:
        return render_template('login_s.html')

    cursor = conn.cursor()
    query1 = 'SELECT sum(sold_price) as sum FROM ticket natural join buys natural join paid natural join payment WHERE airline_name = %s and booking_agent_id is null and payment_time >= date_sub(now(), interval 1 month)'
    cursor.execute(query1, (airline_name['airline_name']))
    direct = cursor.fetchone()
    if direct['sum'] == None:
        direct['sum'] = 0
    print('direct:', direct)

    query2 = 'SELECT sum(sold_price) as sum FROM ticket natural join buys natural join paid natural join payment WHERE airline_name = %s and booking_agent_id is not null and payment_time >= date_sub(now(), interval 1 month)'
    cursor.execute(query2, (airline_name['airline_name']))
    indirect = cursor.fetchone()
    print('indirect:', indirect)


    cursor = conn.cursor()
    query3 = 'SELECT sum(sold_price) as sum FROM ticket natural join buys natural join paid natural join payment WHERE airline_name = %s and booking_agent_id is null and payment_time >= date_sub(now(), interval 12 month)'
    cursor.execute(query3, (airline_name['airline_name']))
    directy = cursor.fetchone()
    if direct['sum'] == None:
        direct['sum'] = 0
    print('direct:', direct)

    query4 = 'SELECT sum(sold_price) as sum FROM ticket natural join buys natural join paid natural join payment WHERE airline_name = %s and booking_agent_id is not null and payment_time >= date_sub(now(), interval 12 month)'
    cursor.execute(query4, (airline_name['airline_name']))
    indirecty = cursor.fetchone()
    print('indirect:', indirect)

    return render_template('comparison_of_revenue.html', direct=direct, indirect = indirect,directy=directy, indirecty = indirecty )



@app.route('/view_top_destinations', methods=['GET', 'POST'])
def view_top_destinations():
    username = session['username']
    airline_name = session['airline_name']
    if username==None:
        return render_template('login_s.html')

    cursor = conn.cursor()
    #top destinations within the airline_name
    query = 'SELECT city FROM flight natural join ticket natural join buys natural join paid natural join payment, airport where airport.id = flight.arrival_airport and payment_time >= date_sub(now(), interval 3 month) and airline_name = %s group by flight.arrival_airport order by count(flight.arrival_airport) desc limit 3'
    cursor.execute(query, (airline_name['airline_name']))
    cities_month = cursor.fetchall()
    print("cities_month", cities_month)
    #top destinations within the airline_name
    query1 = 'SELECT city FROM flight natural join ticket natural join buys natural join paid natural join payment, airport where airport.id = flight.arrival_airport and payment_time >= date_sub(now(), interval 12 month) and airline_name = %s group by flight.arrival_airport order by count(flight.arrival_airport) desc limit 3'
    cursor.execute(query1, (airline_name['airline_name']))
    cities_year = cursor.fetchall()


    cursor.close()
    return render_template('view_top_destinations.html', cities_month=cities_month, cities_year=cities_year)

#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    # app.run('127.0.0.1', 5000)
    app.run(debug=True)

from app_a import *
