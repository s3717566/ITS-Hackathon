from flask import Flask, render_template, request
import pyodbc
import datetime
app = Flask(__name__)

server = 'raddish.database.windows.net'
database = 'SAS'
username = 's3719678'
password = 'raddish12!'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                        server+';DATABASE='+database+';UID='+username+';PWD=' + password)

def get_cursor():
        cursor = cnxn.cursor()
        return cursor


@app.route('/')
def student():
        
        now = datetime.datetime.now()
        year = str(now.year)
        month = str(now.month)
        day = str(now.day)
        minute = str(now.minute)

        if      now.hour <= 12:
                hour = str(now.hour)
                period = "am"
        else:
                hour = str(now.hour - 12)
                period = "pm"

        date = day + "/" + month + "/" + year +" " + hour + ":" + minute + " " + period

        return render_template("student.html", date=date)

@app.route('/home', methods=['POST','GET'])
def home():
    return render_template("home.html")

@app.route('/result', methods=['POST', 'GET'])
def result():
        if request.method == 'POST':
                result = request.form
                return render_template("result.html", result=result)

@app.route('/communities')
def communities():
    return render_template("communities.html")

@app.route('/friends')
def friends():
    return render_template("friends.html")

@app.route('/login', methods=['POST','GET'])
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/testcommunity')
def testcommunity():
    return render_template("testcommunity.html")

@app.route('/community', methods=['POST', 'GET'])
def community():

    result = request.form
    var = request.form['Name']
    var2 = request.form['Desc']

    cursor = get_cursor().execute(f"INSERT INTO COMMUNITIES VALUES ('{var}','{var2}')")
    cnxn.commit()

    communities = get_cursor().execute("SELECT * FROM COMMUNITIES")
    comArray = []
    counter = 0;

    for c in communities:
        comArray.append(c)
        counter+=1
    return render_template("community.html", comArray=comArray,counter=counter)

if __name__ == 'main':
        app.run(debug=True)
