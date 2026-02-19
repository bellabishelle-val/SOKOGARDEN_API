# import flask and its components
from flask import *

#import the pymysql module - it helps create a connection between python flask and mysql database
import pymysql
# create a flask application and give it a name
app = Flask(__name__)

# below is the register/sign up route
@app.route("/api/signup", methods = ["POST"])
def signup():
    if request.method == "POST":
        #EXTRACT the different details entered on the form
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        # by use of the print function lets print all details sent with upcoming request
        # print(username, email, password, phone)

        #establish a connection between flask/python and mysql
        connection = pymysql.connect(host = "localhost", user = "root", password = "", database = "sokogardenonline")

        #create a cursor to execute sql  -> cursor is like a mediator between your Python code and the database
        cursor = connection.cursor()

        #structure an sql to insert details received from the form
        # the %s is a placeholder -> a placeholder stands in places of actual values i.e we shall replace later on
        sql = "INSERT INTO users (username, email, phone, password) VALUES(%s, %s, %s, %s )"

        #create a tuple that will hold all the data gotten from the form
        data = (username, email, phone, password)

        #by use of the cursor execute the sql as u replace the placeholder with actual values
        cursor.execute(sql, data)

        # commit the changes to the database
        connection.commit()


        return jsonify({"message": "User Registered Successfully"})



#Below is the login/sign route
@app.route("/api/signin", methods= ["POST"])
def signin():
    if request.method == "POST":
         #extract the two details entered on the form
        email = request.form["email"]
        password = request.form["password"]

        #print out the details entered
        # print(email,password)

        #create/ establish connection to database
        connection = pymysql.connect(host="localhost",user="root", password="", database= "sokogardenonline")

        #create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        #structure the sql query that will check whether the email and password entered are correct
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"

        #put the data received from the form into a tuple
        data = (email, password)

        #by use of cursor execute sql
        cursor.execute(sql, data)

        #check whether there row returned and store them on variable
        count = cursor.rowcount
        print(count)

        #if there are record return it means the password and email are correct otherwise it means they are wrong
        if count == 0:
            return jsonify({"message" : "Login failed"})
        else:
            # there must be a user so we create a variable that will hold the details of user fetched from database
            user= cursor.fetchone()
            # return details to frontend as well as a message
            return jsonify({"message" : "User Logged In Successfully", "user":user})

#run the application
app.run(debug = True)