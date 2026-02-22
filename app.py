# import flask and its components
from flask import *
import os
#import the pymysql module - it helps create a connection between python flask and mysql database
import pymysql
# create a flask application and give it a name
app = Flask(__name__)

# configure the location to where your product images will be saved on your application
app.config["UPLOAD_FOLDER"] = "static/images"

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



# below is route for adding products
@app.route("/api/add_product", methods = ["POST"])
def Addproducts():
    if request.method == "POST":
        # extract data entered on the form
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        # for the product photo we shall fetch it from the files as shown below
        product_photo = request.files["product_photo"]

        #extract the file name of product photo
        filename = product_photo.filename
        # print("this is the file name :, filename")

        # by use of the os module (operating system) we can extract the file path where the images is currently saved
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # save the product photo image into the new location
        product_photo.save(photo_path)

        #print them out to test whether you are receiving the details sent with the request.
        # print(product_name, product_description, product_cost, product_photo)

        #establish a connection to the database
        connection = pymysql.connect(host="localhost", user="root", password= "", database = "sokogardenonline")

        # create a cursor
        cursor = connection.cursor()

        # structure the sql query to insert the product details to the database
        sql = "INSERT INTO product_details(product_name, product_description, product_cost, product_photo) VALUES (%s, %s, %s, %s)"

        # create a tuple that will hold data from the form which are currently held onto the different variable declared.
        data = (product_name, product_description, product_cost, filename)

        # use cursor to execute the sql as you replace the placeholders with actual data
        cursor.execute(sql, data)

        # commit changes to database
        connection.commit()


        return jsonify ({"message" : "Product Added Successfully"})
    

#run the application
app.run(debug = True)