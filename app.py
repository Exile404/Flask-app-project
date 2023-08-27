from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQLdb

app = Flask(__name__)

# Configure the MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DATABASE'] = 'blood_donor'

# Initialize the MySQL database
db = MySQLdb.connect(app.config['MYSQL_HOST'], app.config['MYSQL_USER'],
                         app.config['MYSQL_PASSWORD'], app.config['MYSQL_DATABASE'])

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/signup')
def signup():
  return render_template('signup.html')

# @app.route('/blood_donation')
# def blood_donation():
#   return render_template('blood_donation.html')

# @app.route('/requests')
# def requests():
#   return render_template('requests.html')

# @app.route('/search')
# def search():
#   return render_template('search.html')

# # Handle the login form submission
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']

  # Check if the user exists and the password is correct
    cursor = db.cursor()

    select_query = "SELECT * FROM users WHERE email=%s AND password=%s"
    data = (email, password)
    cursor.execute(select_query, data)
    user = cursor.fetchone()

    
    print(user)
    query = "SELECT * FROM db_blood"  # Modify the query according to your table structure
    cursor.execute(query)
    data_from_db = cursor.fetchall()
    print(data_from_db)
    cursor.close()
    db.close()
    if user is not None:
        return render_template('base.html', data=data_from_db)
    else:
        return render_template('login.html')

# # Handle the signup form submission
@app.route('/signup', methods=['POST'])
def signup_post():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cursor = db.cursor()

    insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    data = (name, email, password)
    cursor.execute(insert_query, data)

    db.commit()
    cursor.close()
    db.close()

    return 'User registered successfully!'

@app.route('/add_donor')
def add_donor():
    return render_template('add_donor.html')

def logout():
    # Perform logout actions (e.g., clear session, etc.)
    return render_template('index.html') 
@app.route('/save_donor', methods=['POST'])
def save_donor():
    name = request.form['name']
    blood_group = request.form['blood_group']
    contact = request.form['contact']

    cursor = db.cursor()
    insert_query = "INSERT INTO db_blood (name, blood_group, contact) VALUES (%s, %s, %s)"
    data = (name, blood_group, contact)
    
    try:
        cursor.execute(insert_query, data)
        db.commit()
        cursor.close()
        return redirect('/')  # Redirect to the donor list page
    except Exception as e:
        print("An error occurred:", e)
        return render_template('error.html')



if __name__ == '__main__':
  app.run(debug=True)
