#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect,flash
import pymysql.cursors
import datetime

#Initialize the app from Flask
app = Flask(__name__)

#ahahhahaha jajaja
#Configure MySQL
conn = pymysql.connect(host='192.168.64.3',
                       port=3306,
                       user='root',
                       password='',
                       db='Plane_Official',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define a route to hello function
@app.route('/returnstaff')
def returnstaff():
	return render_template('index.html',message='airline_staff')
#Define a route to hello function
@app.route('/returnagent')
def returnagent():
	return render_template('index.html',message='booking_agent')
#Define a route to hello function
@app.route('/returncustomer')
def returncustomer():
	return render_template('index.html',message='customer')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/searchresult')
def searchresult():
	return render_template('searchresult.html')

@app.route('/customerpurchase')
def customerpurchase():
	return render_template('customerpurchase.html')
#写这个-----------
@app.route('/customerpurchaseAuth',methods=['GET', 'POST'])
def customerpurchaseAuth():
	username = session['username']

	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']

	#cursor used to send queries
	cursor = conn.cursor()
	query = 'Select ticket_id From ticket Where airline_name = %s AND flight_num = %s'
	cursor.execute(query, (airline_name,flight_num))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	if (data):
		#cursor used to send queries
		cursor = conn.cursor()
		query = 'Select * from purchases where ticket_id = %s and customer_email = %s'
		cursor.execute(query, (data['ticket_id'],username))
		data1 = cursor.fetchone()
		query1 = 'Select Count(*) as count from purchases Natural Join ticket where airline_name = %s and flight_num = %s'
		cursor.execute(query1, (airline_name,flight_num))
		qq = cursor.fetchone()
		query0 = 'Select seats from airplane Natural Join flight where airline = %s and airplane_id = %s'
		cursor.execute(query0, (airline_name,'9103'))
		qq0 = cursor.fetchone()
		cursor.close()
		if(data1):
			return render_template('customerpurchase.html',message='unsuccessful')
		elif qq['count'] >= qq0['seats']:
			return render_template('customerpurchase.html',message='unsuccessful')
		else:
			
			cursor = conn.cursor()
			ins = 'INSERT INTO purchases VALUES(%s, %s,NULL,%s)'
			cursor.execute(ins, (data['ticket_id'],username,datetime.date.today()))
			conn.commit()
			cursor.close()
			return render_template('customerpurchase.html',message='successful')
			
	else:
		return render_template('customerpurchase.html',message='unsuccessful')


@app.route('/agentpurchase')
def agentpurchase():
	return render_template('agentpurchase.html')
#写这个-----------
@app.route('/agentpurchaseAuth',methods=['GET', 'POST'])
def agentpurchaseAuth():
	username = session['username']
	cursor = conn.cursor()
	query = 'Select airline_name From booking_agent_work_for Where email = %s'
	cursor.execute(query, username)
	#stores the results in a variable
	check = cursor.fetchall()
	check1=[]
	for i in check:
		check1.append(i['airline_name'])

	#use fetchall() if you are expecting more than 1 data row
	get_id = 'Select booking_agent_id from booking_agent where email = %s'
	cursor.execute(get_id, username)
	his_id = cursor.fetchone()
	cursor.close()

	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']
	customer_email = request.form['customer_email']

	cursor = conn.cursor()
	query = 'Select ticket_id From ticket Where airline_name = %s AND flight_num = %s'
	cursor.execute(query, (airline_name,flight_num))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	if (data):
		#cursor used to send queries
		cursor = conn.cursor()
		query = 'Select * from purchases where ticket_id = %s and customer_email = %s '
		cursor.execute(query, (data['ticket_id'],customer_email))
		data1 = cursor.fetchone()
		query1 = 'Select Count(*) as count from purchases Natural Join ticket where airline_name = %s and flight_num = %s'
		cursor.execute(query1, (airline_name,flight_num))
		qq = cursor.fetchone()
		query0 = 'Select seats from airplane Natural Join flight where airline_name = %s and airplane_id = %s'
		cursor.execute(query0, (airline_name,'9103'))
		qq0 = cursor.fetchone()
		cursor.close()
		print('1',qq0['seats'])
		if(data1):
			return render_template('agentpurchase.html',message='unsuccessful')
		elif qq['count'] >= qq0['seats']:
			return render_template('agentpurchase.html',message='unsuccessful')
		else:
			print(check1)
			if airline_name in check1:
				cursor = conn.cursor()
				ins = 'INSERT INTO purchases VALUES(%s, %s,%s,%s)'
				cursor.execute(ins, (data['ticket_id'],customer_email,his_id['booking_agent_id'],datetime.date.today()))
				conn.commit()
				cursor.close()
				return render_template('agentpurchase.html',message='successful')
		return render_template('agentpurchase.html',message='unsuccessful')
	else:
		return render_template('agentpurchase.html',message='unsuccessful')


@app.route('/flightsearchAuth',methods=['GET', 'POST'])
def flightsearchAuth():
	base = request.form['base']
	text = request.form['text']

	#cursor used to send queries
	cursor = conn.cursor()
	if base == 'departure_airport':
		query = 'Select airline_name,status,flight_num,departure_time,arrival_time From flight Where departure_airport Like %s and status = %s'
		cursor.execute(query,(text,'upcoming'))
	#stores the results in a variable
		data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	if base == 'arrival_airport':
		query = 'Select airline_name,status,flight_num,departure_time,arrival_time From flight Where arrival_airport Like %s and status = %s'
		cursor.execute(query,(text,'upcoming'))
	#stores the results in a variable
		data = cursor.fetchall()
	if base == 'departure_time':
		query = 'Select airline_name,status,flight_num,departure_time,arrival_time From flight Where departure_time Like %s and status = %s'
		cursor.execute(query,(text,'upcoming'))
	#stores the results in a variable
		data = cursor.fetchall()
	if(data):
		return render_template('searchresult.html',message='successful',posts=data)
	else:
		return render_template('searchresult.html', message='unsuccessful')


@app.route('/customersearchAuth',methods=['GET', 'POST'])
def customersearchAuth():
	base = request.form['base']
	text = request.form['text']

	#cursor used to send queries
	cursor = conn.cursor()
	if base == 'departure_airport':
		query = 'Select airline_name,status,flight_num,departure_time,arrival_time From flight Where departure_airport Like %s and status = %s'
		cursor.execute(query,(text,'upcoming'))
	#stores the results in a variable
		data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	if base == 'arrival_airport':
		query = 'Select airline_name,status,flight_num,departure_time,arrival_time From flight Where arrival_airport Like %s and status = %s'
		cursor.execute(query,(text,'upcoming'))
	#stores the results in a variable
		data = cursor.fetchall()
	if base == 'departure_time':
		query = 'Select airline_name,status,flight_num,departure_time,arrival_time From flight Where departure_time Like %s and status = %s'
		cursor.execute(query,(text,'upcoming'))
	#stores the results in a variable
		data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	if(data):
		return render_template('searchresult.html',message='successful',role='customer',posts=data)
	else:
		return render_template('searchresult.html', message='unsuccessful')

@app.route('/agentsearchAuth',methods=['GET', 'POST'])
def agentsearchAuth():
	base = request.form['base']
	text = request.form['text']

	#cursor used to send queries
	cursor = conn.cursor()
	if base == 'departure_airport':
		query = 'Select airline_name,status,flight_num,departure_time,arrival_time From flight Where departure_airport Like %s and status = %s'
		cursor.execute(query,(text,'upcoming'))
	#stores the results in a variable
		data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	if base == 'arrival_airport':
		query = 'Select airline_name,status,flight_num,departure_time,arrival_time From flight Where arrival_airport Like %s and status = %s'
		cursor.execute(query,(text,'upcoming'))
	#stores the results in a variable
		data = cursor.fetchall()
	if base == 'departure_time':
		query = 'Select airline_name,status,flight_num,departure_time,arrival_time From flight Where departure_time Like %s and status = %s'
		cursor.execute(query,(text,'upcoming'))
	#stores the results in a variable
		data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	if(data):
		return render_template('searchresult.html',message='successful',role='agent',posts=data)
	else:
		return render_template('searchresult.html', message='unsuccessful')



#Define route for viewing flights    
@app.route('/viewflights')
def viewflights():
	username = session['username']
	cursor = conn.cursor()
	query = "SELECT airline_name,flight_num,departure_time,departure_airport,arrival_time,arrival_airport,status FROM purchases Natural Join ticket Natural Join flight WHERE customer_email = %s and status = %s order by departure_time Desc"
	cursor.execute(query, (username,'upcoming'))
	data = cursor.fetchall()
	cursor.close()
	if (data):
		return render_template('viewflights.html',message='successful',posts=data)
	else:
		return render_template('viewflights.html',message='unsuccessful')
@app.route('/viewflightsagent')
def viewflightsagent():
	username = session['username']
	cursor = conn.cursor()
	get_id = 'Select booking_agent_id from booking_agent where email = %s'
	cursor.execute(get_id, username)
	book_id = cursor.fetchone()
	query = "SELECT airline_name,flight_num,customer_email,status FROM purchases Natural Join ticket Natural Join flight WHERE booking_agent_id=%s and status = %s order by departure_time Desc"
	cursor.execute(query, (book_id['booking_agent_id'],'upcoming'))
	data = cursor.fetchall() 
	cursor.close()
	if (data):
		return render_template('viewflightsagent.html',message='successful',posts=data)
	else:
		return render_template('viewflightsagent.html',message='unsuccessful')

@app.route('/viewflightsstaff')
def viewflightsstaff():
	username = session['username']
	cursor = conn.cursor()
	query0="Select airline_name from airline_staff where username = %s"
	cursor.execute(query0, username)
	airline_name = cursor.fetchone()
	query = "SELECT airline_name,flight_num,departure_time,departure_airport,arrival_time,arrival_airport,status FROM flight WHERE airline_name = %s  and status = %s and departure_time between CURRENT_TIMESTAMP and date_add(CURRENT_TIMESTAMP,INTERVAL 30 day)"
	cursor.execute(query, (airline_name['airline_name'],'upcoming'))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('viewflightsstaff.html',posts=data1)

@app.route('/viewflightsstaffAuth',methods=['GET', 'POST'])
def viewflightsstaffAuth():
	username = session['username']
	cursor = conn.cursor()
	query0="Select airline_name from airline_staff where username = %s"
	cursor.execute(query0, username)
	airline_name = cursor.fetchone()
	query = "SELECT airline_name,flight_num,departure_time,departure_airport,arrival_time,arrival_airport,status FROM flight WHERE airline_name = %s  and status = %s and departure_time between CURRENT_TIMESTAMP and date_add(CURRENT_TIMESTAMP,INTERVAL 30 day)"
	cursor.execute(query,(airline_name['airline_name'],'upcoming'))
	data1 = cursor.fetchall()

	#grabs information from the forms
	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']

	cursor = conn.cursor()
	query = 'Select customer_email From purchases Natural Join ticket where airline_name = %s and flight_num = %s'
	cursor.execute(query,(airline_name,flight_num))
	data = cursor.fetchall()
	cursor.close()
	if(data):
		return render_template('viewflightsstaff.html', message='successful',posts=data1,post=data)
	else:
		return render_template('viewflightsstaff.html', message='unsuccessful',posts=data1)

@app.route('/viewflightsstaffAuthh',methods=['GET', 'POST'])
def viewflightsstaffAuthh():
	username = session['username']
	cursor = conn.cursor()
	query0="Select airline_name from airline_staff where username = %s"
	cursor.execute(query0, username)
	airline_name = cursor.fetchone()
	query = "SELECT airline_name,flight_num,departure_time,departure_airport,arrival_time,arrival_airport,status FROM flight WHERE airline_name = %s  and status = %s and departure_time between CURRENT_TIMESTAMP and date_add(CURRENT_TIMESTAMP,INTERVAL 30 day)"
	cursor.execute(query,(airline_name['airline_name'],'upcoming'))
	data1 = cursor.fetchall()

	#grabs information from the forms
	firstDate = request.form['firstDate']
	secondDate = request.form['secondDate']

	cursor = conn.cursor()
	query = 'SELECT airline_name,flight_num,departure_time,departure_airport,arrival_time,arrival_airport,status FROM flight WHERE airline_name = %s  and departure_time between %s and %s order by status'
	cursor.execute(query,(airline_name['airline_name'],firstDate,secondDate))
	data = cursor.fetchall()
	cursor.close()
	if(data):
		return render_template('viewflightsstaff.html', message='kiki',posts=data1,dodo=data)
	else:
		return render_template('viewflightsstaff.html', message='unsuccessful',posts=data1)

#Define route for tracking spending
@app.route('/spending')
def spending():
	username = session['username']
	cursor = conn.cursor()
	query1 = 'Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where customer_email = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 180 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 150 day) '
	cursor.execute(query1,username)
	data1 = cursor.fetchone() or {'price':'0'}
	query2 = 'Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where customer_email = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 150 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 120 day) '
	cursor.execute(query2,username)
	data2 = cursor.fetchone() or {'price':'0'}
	query3 = 'Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where customer_email = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 120 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 90 day) '
	cursor.execute(query3,username)
	data3 = cursor.fetchone() or {'price':'0'}
	query4 = 'Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where customer_email = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 90 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 60 day) '
	cursor.execute(query4,username)
	data4 = cursor.fetchone() or {'price':'0'}
	query5 = 'Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where customer_email = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 60 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 30 day) '
	cursor.execute(query5,username)
	data5 = cursor.fetchone() or {'price':'0'}
	query6 = 'Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where customer_email = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 30 day) and CURRENT_TIMESTAMP '
	cursor.execute(query6,username)
	data6 = cursor.fetchone() or {'price':'0'}
	query7 = 'Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where customer_email = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and CURRENT_TIMESTAMP '
	cursor.execute(query7,username)
	data7 = cursor.fetchone() or {'price':'0'}
	print(data1,data2,data3,data4,data5,data6)
	return render_template('spending.html',data1=data1['price'],data2=data2['price'],data3=data3['price'],data4=data4['price'],data5=data5['price'],data6=data6['price'],data7=data7['price'])

#Define route for viewing commission
@app.route('/commission')
def commission():
	username = session['username']
	cursor = conn.cursor()
	get_id = 'Select booking_agent_id from booking_agent where email = %s'
	cursor.execute(get_id, username)
	his_id = cursor.fetchone()
	query1 = 'Select Sum(price) as commission from flight Natural Join ticket Natural Join purchases where booking_agent_id = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 30 day) and CURRENT_TIMESTAMP'
	cursor.execute(query1,his_id['booking_agent_id'])
	data1 = cursor.fetchone() or {'commission':'0'}
	query2 = 'Select Count(*) as count from purchases where booking_agent_id = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 30 day) and CURRENT_TIMESTAMP '
	cursor.execute(query2,his_id['booking_agent_id'])
	data2 = cursor.fetchone() or {'count':'0'}
	query3 = 'Select Avg(price) as average from flight Natural Join ticket Natural Join purchases where booking_agent_id = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 30 day) and CURRENT_TIMESTAMP '
	cursor.execute(query3,his_id['booking_agent_id'])
	data3 = cursor.fetchone() or {'average':'0'}
	print(data1)
	return render_template('commission.html',data1=data1['commission'],data2=data2['count'],data3=data3['average'])

#Define route for viewing commission
@app.route('/commissionAuth',methods=['GET', 'POST'])
def commissionAuth():
	username = session['username']
	cursor = conn.cursor()
	get_id = 'Select booking_agent_id from booking_agent where email = %s'
	cursor.execute(get_id, username)
	his_id = cursor.fetchone()
	query1 = 'Select Sum(price) as commission from flight Natural Join ticket Natural Join purchases where booking_agent_id = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 30 day) and CURRENT_TIMESTAMP'
	cursor.execute(query1,his_id['booking_agent_id'])
	data1 = cursor.fetchone() or {'commission':'0'}
	query2 = 'Select Count(*) as count from purchases where booking_agent_id = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 30 day) and CURRENT_TIMESTAMP '
	cursor.execute(query2,his_id['booking_agent_id'])
	data2 = cursor.fetchone() or {'count':'0'}
	query3 = 'Select Avg(price) as average from flight Natural Join ticket Natural Join purchases where booking_agent_id = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 30 day) and CURRENT_TIMESTAMP '
	cursor.execute(query3,his_id['booking_agent_id'])
	data3 = cursor.fetchone() or {'average':'0'}
	cursor.close()

	firstDate = request.form['firstDate']
	secondDate = request.form['secondDate']

	cursor = conn.cursor()
	search1 = "Select Sum(price) as commission from flight Natural Join ticket Natural Join purchases where booking_agent_id = %s and purchase_date between %s and %s"
	cursor.execute(search1, (his_id['booking_agent_id'],firstDate,secondDate))
	get1 = cursor.fetchone() or {'commission':'0'}
	search2 = 'Select Count(*) as count from purchases where booking_agent_id = %s and purchase_date between %s and %s'
	cursor.execute(search2, (his_id['booking_agent_id'],firstDate,secondDate))
	get2 = cursor.fetchone() or {'count':'0'}

	return render_template('commission.html',message='successful',data1=data1['commission'],data2=data2['count'],data3=data3['average'],get1=get1['commission'],get2=get2['count'])

#Define route for viewing top customers
@app.route('/topcustomer')
def topcustomer():
	username = session['username']
	cursor = conn.cursor()
	get_id = 'Select booking_agent_id from booking_agent where email = %s'
	cursor.execute(get_id, username)
	his_id = cursor.fetchone()
	query1 = 'Select customer_email,Count(customer_email) as count from purchases where booking_agent_id = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 184 day) and CURRENT_TIMESTAMP group by customer_email order by Count(customer_email) Desc limit 5'
	cursor.execute(query1,his_id['booking_agent_id'])
	data1 = cursor.fetchall()
	query2 = 'Select customer_email , Sum(price) as commission from flight Natural Join ticket Natural Join purchases where booking_agent_id = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and CURRENT_TIMESTAMP group by customer_email order by Sum(price) Desc limit 5'
	cursor.execute(query2,his_id['booking_agent_id'])
	data2 = cursor.fetchall()
	cursor.close()
	DD11 = []
	DD12 = []
	DD21 = []
	DD22 = []
	for i in data1:
		DD11.append(i['customer_email'])
		DD12.append(i['count'])
	for i in data2:
		DD21.append(i['customer_email'])
		DD22.append(int(i['commission'])*0.1)
	for i in range(5):
		try:
			if (DD11[i]):
				continue
		except:
			DD11.append('No one')
	for i in range(5):
		try :
			if (DD12[i]):
				print(DD12[i],' ')
		except:
			DD12.append(0)
			print(DD12[i],' ')
	for i in range(5):
		try :
			if (DD21[i]):
				continue
		except:
			DD21.append('No one')
	for i in range(5):
		try :
			if (DD22[i]):
				continue
		except:
			DD22.append(0)
	print(DD12,'/',DD22)
	return render_template('topcustomer.html',data1=DD11[0],data2=DD11[1],data3=DD11[2],data4=DD11[3],data5=DD11[4],dodo1=DD12[0],dodo2=DD12[1],dodo3=DD12[2],dodo4=DD12[3],dodo5=DD12[4],kaka1=DD21[0],kaka2=DD21[1],kaka3=DD21[2],kaka4=DD21[3],kaka5=DD21[4],koko1=DD22[0],koko2=DD22[1],koko3=DD22[2],koko4=DD22[3],koko5=DD22[4])

#Define route for viewing top customers
@app.route('/createflight')
def createflight():
	return render_template('createflight.html')

#Define route for creating flights
@app.route('/createflightAuth',methods=['GET', 'POST'])
def createflightAuth():
	username = session['username']
	cursor = conn.cursor()
	query = "Select permission_type from permission where username = %s"
	cursor.execute(query, (username))
	perm = cursor.fetchone()
	if perm['permission_type']!="Admin":
		return render_template("index.html",message='airline_staff')
	cursor.close()
	#grabs information from the forms
	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']
	departure_airport = request.form['departure_airport']
	departure_time = request.form['departure_time']
	arrival_airport = request.form['arrival_airport']
	arrival_time = request.form['arrival_time']
	price = request.form['price']
	status = request.form['status']
	airplane_id = request.form['airplane_id']

	#cursor used to send queries
	cursor = conn.cursor()
	try:
		ins = 'INSERT INTO flight VALUES(%s, %s,%s,%s,%s,%s,%s,%s,%s)'
		cursor.execute(ins, (airline_name,flight_num,departure_airport,departure_time,arrival_airport,arrival_time,price,status,airplane_id))
		conn.commit()
		cursor.close()
		return render_template('createflight.html',message='successful')
	except:
		return render_template('createflight.html',message='unsuccessful')

#Define route for changing flight status
@app.route('/changestatus')
def changestatus():
	return render_template('changestatus.html')

@app.route('/changestatusAuth',methods=['GET', 'POST'])
def changestatusAuth():
	
	username = session['username']
	cursor = conn.cursor()
	query = "Select permission_type from permission where username = %s"
	cursor.execute(query, (username))
	perm = cursor.fetchone()
	if perm['permission_type']!="Operator":
		return render_template("index.html",message='airline_staff')
	cursor.close()
	
	#grabs information from the forms
	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']
	status = request.form['status']

	#cursor used to send queries
	cursor = conn.cursor()
	query = 'Select * From flight Where airline_name = %s AND flight_num = %s'
	cursor.execute(query, (airline_name,flight_num))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	if(data):
		upd = 'Update flight Set status = %s Where airline_name = %s and flight_num = %s'
		cursor.execute(upd, (status,airline_name,flight_num))
		conn.commit()
		cursor.close()
		return render_template('changestatus.html', message='successful')
	else:
		return render_template('changestatus.html',message='unsuccessful')

#Define route for adding airplane
@app.route('/addairplane')
def addairplane():
	return render_template('addairplane.html')

@app.route('/addairplaneAuth',methods=['GET', 'POST'])
def addairplaneAuth():

	username = session['username']
	cursor = conn.cursor()
	query = "Select permission_type from permission where username = %s"
	cursor.execute(query, (username))
	perm = cursor.fetchone()
	if perm['permission_type']!="Admin":
		return render_template("index.html",message='airline_staff')
	cursor.close()

	#grabs information from the forms
	airline_name = request.form['airline_name']
	airplane_id = request.form['airplane_id']
	seats = request.form['seats']

	#cursor used to send queries
	cursor = conn.cursor()
	query = 'Select * From airplane Where airline_name = %s AND airplane_id = %s'
	cursor.execute(query, (airline_name,airplane_id))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	if(data):
		return render_template('addairplane.html', message='unsuccessful')
	else:
		ins = 'INSERT INTO airplane VALUES(%s, %s,%s)'
		cursor.execute(ins, (airline_name,airplane_id,seats))
		conn.commit()
		cursor.close()
		
		cursor = conn.cursor()
		query = "SELECT airline_name,airplane_id FROM airplane Natural Join airline_staff WHERE username = %s"
		cursor.execute(query, (username))
		data1 = cursor.fetchall()
		cursor.close()
		return render_template('addairplane.html',message='successful',posts=data1)

#Define route for adding airport
@app.route('/addairport')
def addairport():
	return render_template('addairport.html')

@app.route('/addairportAuth',methods=['GET', 'POST'])
def addairportAuth():

	username = session['username']
	cursor = conn.cursor()
	query = "Select permission_type from permission where username = %s"
	cursor.execute(query, (username))
	perm = cursor.fetchone()
	if perm['permission_type']!="Admin":
		return render_template("index.html",message='airline_staff')
	cursor.close()

	#grabs information from the forms
	airport_name = request.form['airport_name']
	airport_city = request.form['airport_city']

	#cursor used to send queries
	cursor = conn.cursor()
	query = 'Select * From airport Where airport_name = %s AND airport_city = %s'
	cursor.execute(query, (airport_name,airport_city))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	if(data):
		return render_template('addairport.html', message='unsuccessful')
	else:
		ins = 'INSERT INTO airport VALUES(%s, %s)'
		cursor.execute(ins, (airport_name,airport_city))
		conn.commit()
		cursor.close()
		return render_template('addairport.html',message='successful')

#Define route for viewing agents
@app.route('/viewagents')
def viewagents():
	cursor = conn.cursor()
	query1 = 'Select email,Count(booking_agent_id) as count from purchases Natural Join booking_agent where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 30 day) and CURRENT_TIMESTAMP group by booking_agent_id order by Count(booking_agent_id) Desc limit 5'
	cursor.execute(query1)
	data1 = cursor.fetchall()
	query2 = 'Select email,Count(booking_agent_id) as count from purchases Natural Join booking_agent where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and CURRENT_TIMESTAMP group by booking_agent_id order by Count(booking_agent_id) Desc limit 5'
	cursor.execute(query2)
	data2 = cursor.fetchall()
	query3 = 'Select email, Sum(price) as commission from flight Natural Join ticket Natural Join purchases Natural Join booking_agent where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and CURRENT_TIMESTAMP group by booking_agent_id order by Sum(price) Desc limit 5'
	cursor.execute(query3)
	data3 = cursor.fetchall()
	return render_template('viewagents.html',posts1=data1,posts2=data2,posts3=data3)

#Define route for viewing customers
@app.route('/viewcustomers')
def viewcustomers():
	cursor = conn.cursor()
	query = "Select customer_email, count(customer_email) as count from purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and CURRENT_TIMESTAMP group by customer_email order by count(customer_email) Desc limit 1"
	cursor.execute(query)
	data = cursor.fetchone()
	print(data)
	return render_template('viewcustomers.html',post=data['customer_email'])


@app.route('/viewcustomersAuth',methods=['GET', 'POST'])
def viewcustomersAuth():
	cursor = conn.cursor()
	query = "Select customer_email, count(customer_email) from purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and CURRENT_TIMESTAMP group by customer_email order by count(customer_email) Desc limit 1 "
	cursor.execute(query)
	data = cursor.fetchone()

	#grabs information from the forms
	email = request.form['email']
	airline_name = request.form['airline_name']
	try:
		#cursor used to send queries
		cursor = conn.cursor()
		query = 'Select customer_email,flight_num From purchases Natural Join ticket Where customer_email = %s and airline_name = %s and purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and CURRENT_TIMESTAMP'
		cursor.execute(query, (email,airline_name))
		#stores the results in a variable
		data1 = cursor.fetchall()
		cursor.close()
		return render_template('viewcustomers.html',post=data['customer_email'],posts=data1,message='successful')
	except:
		return render_template('viewcustomers.html',message='unsuccessful')

#Define route for viewing reports
@app.route('/viewreports')
def viewreports():
	return render_template('viewreports.html')

#Define route for viewing reports
@app.route('/viewlastmonth')
def viewlastmonth():
	return render_template('viewlastmonth.html')
#Define route for viewing reports
@app.route('/viewlastyear')
def viewlastyear():
	return render_template('viewlastyear.html')

#Define route for viewing reports
@app.route('/viewreportsAuth',methods=['GET', 'POST'])
def viewreportsAuth():
	#grabs information from the forms
	time = request.form['time']
	if time == 'month':
		cursor = conn.cursor()
		query = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 30 day) and CURRENT_TIMESTAMP'
		cursor.execute(query)
		data = cursor.fetchone() or {'count':'0'}
		cursor.close()
		print(data)
		return render_template('viewlastmonth.html',data=data['count'])
	else:
		cursor = conn.cursor()
		query1 = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 335 day)'
		cursor.execute(query1)
		data1 = cursor.fetchone() or {'count':'0'}
		query2 = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 334 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 304 day)'
		cursor.execute(query2)
		data2 = cursor.fetchone() or {'count':'0'}
		query3 = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 303 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 273 day)'
		cursor.execute(query3)
		data3 = cursor.fetchone() or {'count':'0'}
		query4 = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 272 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 242 day)'
		cursor.execute(query4)
		data4 = cursor.fetchone() or {'count':'0'}
		query5 = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 241 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 211 day)'
		cursor.execute(query5)
		data5 = cursor.fetchone() or {'count':'0'}
		query6 = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 210 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 180 day)'
		cursor.execute(query6)
		data6 = cursor.fetchone() or {'count':'0'}
		query7 = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 179 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 149 day)'
		cursor.execute(query7)
		data7 = cursor.fetchone() or {'count':'0'}
		query8 = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 148 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 118 day)'
		cursor.execute(query8)
		data8 = cursor.fetchone() or {'count':'0'}
		query9 = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 117 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 87 day)'
		cursor.execute(query9)
		data9 = cursor.fetchone() or {'count':'0'}
		query10 = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 86 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 56 day)'
		cursor.execute(query10)
		data10 = cursor.fetchone() or {'count':'0'}
		query11 = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 55 day) and date_sub(CURRENT_TIMESTAMP, INTERVAL 25 day)'
		cursor.execute(query11)
		data11 = cursor.fetchone() or {'count':'0'}
		query12 = 'Select Count(*) as count From purchases where purchase_date between date_sub(CURRENT_TIMESTAMP, INTERVAL 24 day) and CURRENT_TIMESTAMP'
		cursor.execute(query12)
		data12 = cursor.fetchone() or {'count':'0'}
		cursor.close()
		return render_template('viewlastyear.html',data1=data1['count'],data2=data2['count'],data3=data3['count'],data4=data4['count'],data5=data5['count'],data6=data6['count'],data7=data7['count'],data8=data8['count'],data9=data9['count'],data10=data10['count'],data11=data11['count'],data12=data12['count'])


#Define route for comparing revenue
@app.route('/revenue')
def revenue():
	cursor = conn.cursor()
	query = "Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where purchase_date between  date_sub(CURRENT_TIMESTAMP, INTERVAL 31 day) and CURRENT_TIMESTAMP and booking_agent_id is not Null"
	cursor.execute(query)
	data = cursor.fetchone() or {'price':'0'}
	query = "Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where purchase_date between  date_sub(CURRENT_TIMESTAMP, INTERVAL 31 day) and CURRENT_TIMESTAMP and booking_agent_id is Null"
	cursor.execute(query)
	data1 = cursor.fetchone() or {'price':'0'}
	query = "Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where purchase_date between  date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and CURRENT_TIMESTAMP and booking_agent_id is not Null"
	cursor.execute(query)
	data2 = cursor.fetchone() or {'price':'0'}
	query = "Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where purchase_date between  date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and CURRENT_TIMESTAMP and booking_agent_id is  Null"
	cursor.execute(query)
	data3 = cursor.fetchone() or {'price':'0'}
	cursor.close()
	return render_template('revenue.html',posts=data['price'],post=data1['price'],frogs=data2['price'],frog=data3['price'])
	
@app.route('/revenue1')
def revenue1():
	cursor = conn.cursor()
	query = "Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where purchase_date between  date_sub(CURRENT_TIMESTAMP, INTERVAL 31 day) and CURRENT_TIMESTAMP and booking_agent_id is not Null"
	cursor.execute(query)
	data = cursor.fetchone() or {'price':'0'}
	query = "Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where purchase_date between  date_sub(CURRENT_TIMESTAMP, INTERVAL 31 day) and CURRENT_TIMESTAMP and booking_agent_id is Null"
	cursor.execute(query)
	data1 = cursor.fetchone() or {'price':'0'}
	query = "Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where purchase_date between  date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and CURRENT_TIMESTAMP and booking_agent_id is not Null"
	cursor.execute(query)
	data2 = cursor.fetchone() or {'price':'0'}
	query = "Select Sum(price) as price from flight Natural Join ticket Natural Join purchases where purchase_date between  date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and CURRENT_TIMESTAMP and booking_agent_id is  Null"
	cursor.execute(query)
	data3 = cursor.fetchone() or {'price':'0'}
	cursor.close()
	return render_template('revenue1.html',posts=data['price'],post=data1['price'],frogs=data2['price'],frog=data3['price'])

#Define route for viewing destinations
@app.route('/destination')
def destination():
	cursor = conn.cursor()
	query = "Select arrival_airport,count(arrival_airport) from flight where arrival_time between date_sub(CURRENT_TIMESTAMP, INTERVAL 93 day) and CURRENT_TIMESTAMP group by arrival_airport order by count(arrival_airport) Desc limit 3 "
	cursor.execute(query)
	data = cursor.fetchall()
	cursor.close()

	cursor = conn.cursor()
	query = "Select arrival_airport,count(arrival_airport) from flight where arrival_time between date_sub(CURRENT_TIMESTAMP, INTERVAL 365 day) and CURRENT_TIMESTAMP group by arrival_airport order by count(arrival_airport) Desc limit 3 "
	cursor.execute(query)
	data1 = cursor.fetchall()
	cursor.close()

	return render_template('destination.html',posts=data,post=data1)

#Define route for permission
@app.route('/permission')
def permission():
	return render_template('permission.html')

@app.route('/permissionAuth',methods=['GET', 'POST'])
def permissionAuth():
	
	username = session['username']
	cursor = conn.cursor()
	query = "Select permission_type from permission where username = %s"
	cursor.execute(query, (username))
	perm = cursor.fetchone()
	if perm['permission_type']!="Admin":
		return render_template("index.html",message='airline_staff')
	cursor.close()
	
	#grabs information from the forms
	username = request.form['name']
	permission = request.form['permission']

	#cursor used to send queries
	cursor = conn.cursor()
	query = 'Select * From permission Where username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	if(data):
		return render_template('permission.html',message='unsuccessful')
	else:
		query = 'Select * From airline_staff Where username = %s'
		cursor.execute(query, (username))
		data1 = cursor.fetchone()
		if (data1):
			ins = 'INSERT INTO permission VALUES(%s, %s)'
			cursor.execute(ins, (username,permission))
			conn.commit()
			cursor.close()
			return render_template('permission.html',message='successful')
		else:
			return render_template('permission.html',message='unsuccessful')

#Define route for adding agents
@app.route('/addagents')
def addagents():
	return render_template('addagents.html')

@app.route('/addagentsAuth',methods=['GET', 'POST'])
def addagentsAuth():
	
	username = session['username']
	cursor = conn.cursor()
	query = "Select permission_type from permission where username = %s"
	cursor.execute(query, (username))
	perm = cursor.fetchone()
	if perm['permission_type']!="Admin":
		return render_template("index.html",message='airline_staff')
	cursor.close()

	#grabs information from the forms
	email = request.form['email']
	airline_name = request.form['airline_name']

	#cursor used to send queries
	cursor = conn.cursor()
	query = 'Select * From booking_agent Where email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	if(data):
		query2 = 'Select * From booking_agent_work_for Where email = %s and airline_name = %s'
		cursor.execute(query2, (email,airline_name))
		#stores the results in a variable
		data2 = cursor.fetchone()
		if (data2):
			return render_template('addagents.html', message='unsuccessful')
		else:
			ins = 'INSERT INTO booking_agent_work_for VALUES(%s, %s)'
			cursor.execute(ins, (email,airline_name))
			conn.commit()
			cursor.close()
			return render_template('addagents.html',message='successful')
	else:
		return render_template('addagents.html', message='unsuccessful')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	role = request.form['role']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	if role == "customer":
		query = 'SELECT * FROM customer WHERE email = %s and password = %s'
	elif role == "airline_staff":
		query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
	else:
		query = 'SELECT * FROM booking_agent WHERE email = %s and password = %s'
	cursor.execute(query, ( username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		if role=='customer':
			return render_template('index.html',message='customer')
		elif role == 'booking_agent':
			return render_template('index.html',message='booking_agent')
		else:
			return render_template('index.html',message='airline_staff')
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	role = request.form['role']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	if role == 'customer':
		return render_template ('register_customer.html')
	elif role == 'booking_agent':
		return render_template ('register_booking_agent.html')
	else:
		return render_template ('register_airline_staff.html')
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO %s VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')
	
@app.route('/customerAuth', methods=['GET', 'POST'])
def customerAuth():
	#grabs information from the forms
	username = request.form['username']
	name = request.form['name']
	password = request.form['password']
	building_number = request.form['building_number']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone_number = request.form['phone_number']
	phone_number = int(phone_number)
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country = request.form['passport_country']
	date_of_birth = request.form['date_of_birth']

	#cursor used to send queries
	cursor = conn.cursor()
	query = 'Select * From customer Where email = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists, please retry"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		cursor.execute(ins, (username, name,password,building_number,street,city,state,phone_number,passport_number,passport_expiration,passport_country,date_of_birth))
		conn.commit()
		cursor.close()
		session['username'] = username
		return render_template('index.html',message='customer')

@app.route('/bookingagentAuth', methods=['GET', 'POST'])
def bookingagentAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']

	#cursor used to send queries
	cursor = conn.cursor()
	query = 'Select * From booking_agent Where email = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists, please retry"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO booking_agent VALUES(%s, %s,%s)'
		cursor.execute(ins, (username,password,booking_agent_id))
		conn.commit()
		cursor.close()
		session['username'] = username
		return render_template('index.html',message='booking_agent')
	

@app.route('/airlinestaffAuth', methods=['GET', 'POST'])
def airlinestaffAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	date_of_birth = request.form['date_of_birth']
	airline_name = request.form['airline_name']
	
	#cursor used to send queries
	cursor = conn.cursor()
	query = 'Select * From airline_staff Where username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists, please retry"
		return render_template('register.html', error = error)
	else:
		try:
			ins = 'INSERT INTO airline_staff VALUES(%s, %s,%s,%s,%s,%s)'
			cursor.execute(ins, (username,password,first_name,last_name,date_of_birth,airline_name))
			conn.commit()
			cursor.close()
			session['username'] = username
			return render_template('index.html',message='airline_staff')
		except:
			error = "You did not choose an existing Airline, please try again, and be serious this time LOL."
			return render_template('register.html', error = error)



@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5050, debug = True)
