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
		return redirect(url_for('home'))
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
        return render_template('index.html')


@app.route('/')
def home():
    # global search
    return render_template('home.html', data=[{'temp':1}])


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
        query = 'SELECT * FROM flight WHERE departure_airport = %s and arrival_airport = %s and departure_day = %s and departure_month = %s and departure_year = %s'
        cursor.execute(query, (src_airport, des_airport, departure_d, departure_m, departure_y))
    	#stores the results in a variable
        data = cursor.fetchone()
    	#use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        if(data):
            return render_template('home.html', error='', flighs=data)
        else:
    		#returns an error message to the html page
            message = 'No Tickets available'
            return render_template('home.html', error=message)
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
            return render_template('home.html', error='', flighs=data)
        else:
            #returns an error message to the html page
            message = 'No Tickets available'
            return render_template('home.html', error=message, flighs=[])




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
    flight_num = request.form['flight_num']

    #save the flight number in the session
    session['flight_num'] = flight_num

    # get information of the flight and send to the payment page to ask for credit card information
    cursor = conn.cursor();

    return render_template('purchase_ticket_c.html', fligth=[])

@app.route('/payment_c', methods=['GET', 'POST'])
def payment_c():
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)

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