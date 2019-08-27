from flask import Flask, render_template,request,flash, redirect, session, abort
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.secret_key='avada kedavra'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'examCommittee'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

config = {
  'user': 'root',
  'password': '49559411',
  'host': '127.0.0.1',
  'database': 'examCommittee',
  'raise_on_warnings': True,
}
mysql.init_app(app)

#cnx = mysql.connector.connect(**config)
conn = mysql.connect()
cursor = conn.cursor()

@app.route('/')
def hello_world():
    return render_template('login.html')


@app.route('/forgot-password.html')
def forgotPass():
    return render_template('forgot-password.html')

@app.route('/signin.html')
def login():
    return render_template('login.html')

@app.route('/index.html',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        examInfo = request.form.to_dict()
        print(examInfo)
        a = examInfo["exid"]
        b = examInfo["typed"]
        c = examInfo["exam"]
        d = examInfo["course"]
        e = examInfo["committee"]
        f = examInfo["examdate"]
        g = examInfo["timer1"]
        h = examInfo["timer2"]
        print(a,b,c,d,e,f,g,h)
        data_exam = {
            'ExamID': examInfo["exid"],
            'Typed': examInfo["typed"],
            'ExamName': examInfo["exam"],
            'CourseID':examInfo["course"],
            'CommitteeID': examInfo["committee"],
            'Dater': examInfo["examdate"],
            'StartTime': examInfo["timer1"],
            'EndTime': examInfo["timer2"],
        }
        #add_exam = ("INSERT INTO exam"
         #           "(ExamID,Typed,ExamName,CourseID,CommitteeID,Dater,StartTime,EndTime) "
          #          "VALUES (%(ExamID)s, %(Typed)s, %(ExamName)s, %(CourseID)s, %(CommitteeID)s, %(Dater)s, %(StartTime)s %(EndTime)s)")

        #cursorEx.execute(add_exam, data_exam)
        #cnx.commit()
        #cursorEx.close()
        #cnx.close()#will go lower if more features are added.
        cursor.callproc('add_exam',(a,b,c,d,e,f,g,h))
        data = cursor.fetchall()
        #session['user']=data[0][0]
        conn.commit()
        flash('Exam is created successfully')
           # return render_template('index.html')
        return render_template('index.html')


@app.route('/Authenticate',methods = ['POST', 'GET'])
def Authenticate():
    #username = request.args.get('UserName')
    #username = request.form['username']
    #password = request.form['password']

    result = {'a':'20'}
    if request.method == 'POST':
        result = request.form.to_dict()

    print(result)
    for x in result:
        if x=="username":
            print("username: "+result[x])
        else:
            print("password: " + result[x])

    #print(result)


    sqlString = "SELECT * from teacher where Username='" + result["username"] + "' and Password='" + result["password"] + "'"
    cursor.execute(sqlString)
    data = cursor.fetchone()
    #data2 = cursor.fetchall()
    if data is None:
        return "Username or Password is wrong"
    else:
        return render_template('index.html')
@app.route('/create_exam.html',methods=['GET','POST'])
def createExam():
    course_id = "SELECT CourseID FROM courses"
    cursor.execute(course_id)
    courseData=cursor.fetchall()
    committee_id = "SELECT CommitteeID FROM committee"
    cursor.execute(committee_id)
    committeeData=cursor.fetchall()
    return render_template('create_exam.html',courseData=courseData,committeeData=committeeData)



if __name__ == '__main__':
    app.run()
