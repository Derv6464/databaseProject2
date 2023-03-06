import datetime
from flask import Flask, request, render_template
import oracledb
# Replace with your actual Oracle database credentials
user = 'SYSTEM'
password = 'root'
port = 1521
service_name = 'XEPDB1'
conn_string = "localhost:{port}/{service_name}".format(
    port=port, service_name=service_name)
app = Flask(__name__)
data = []
id = []

# get Job_Ids from Employee Table
connection = oracledb.connect(
    user=user, password=password, dsn=conn_string)
cur = connection.cursor()
job_id = cur.execute('select ID from ASSETS.JOB_TITLE')
for row in job_id:
    id.append(row[0])
cur.close()
connection.close()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/employee_view', methods=['GET', 'POST'])
def get_data():
    employ = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('Select Employees.employee_id, Employees.name, login.email, job_title.title, employees.DOB, department.dpt_name From assets.employees inner join assets.Login On Employees.login_id=Login.ID inner join assets.Job_title On Employees.job_id=Job_title.ID inner join assets.Department On Employees.department_id=department.dpt_ID')
    for row in cur:
        employ.append({"Employee_ID": row[0], "Name": row[1], "Email":row[2], "Job":row[3], "dob":row[4], "dpt":row[5]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    # Pass the data to the template to display in the HTML table
    return render_template('index.html', data=employ)


@app.route('/about_View')
def about():
    return render_template('about.html')


@app.route('/Insert_View')
def insert():
    return render_template('Insertion.html', job_id=id)

@app.route('/approve_req/<int:id>', methods=["GET","POST"])
def approve_req(id):
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    exe = "UPDATE assets.requests SET requests.is_approved = 1 WHERE requests.request_id = "+str(id)
    cur.execute(exe)
    con.commit()
    return render_template('after_submit.html')


@app.route('/reject_req/<int:id>', methods=["GET","POST"])
def reject_req(id):
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    exe = "UPDATE assets.requests SET requests.is_approved = 0 WHERE requests.request_id = "+str(id)
    cur.execute(exe)
    con.commit()
    return render_template('after_submit.html')
@app.route('/Insertion_data', methods=["GET", "POST"])
def getData():
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    num = request.form["phone"]
    job = request.form["job_id"]
    date = request.form["date"]
    print(request.form)
    Name = fname + " " + lname
    return render_template('data.html', name=Name, Email=email, Number=num, JOB=job, Date=date)

@app.route('/Insert_jobs', methods=["GET", "POST"])
def getjobsData():
    id = request.form["id"]
    title = request.form["title"]
    min = request.form["min"]
    max = request.form["max"]
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    #print("INSERT INTO HR.JOBS(JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY) VALUES (:0, :1, :2,:3)", (id, title,  int(min), int(max)))
    
    cur.execute("INSERT INTO HR.JOBS(JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY) VALUES (:0, :1, :2,:3)", 
                (id, title,  int(min), int(max)))
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')


@app.route('/Add_Assets', methods=["GET", "POST"])
def getAssetData():
    name = request.form["name"]
    model = request.form["model"]
    brand = request.form["brand"]
    company = request.form["company"]
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    # print("INSERT INTO HR.JOBS(JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY) VALUES (:0, :1, :2,:3)", (id, title,  int(min), int(max)))

    cur.execute("INSERT INTO ASSETS.ASSETS(NAME, MODEL, BRAND, COMPANY_ID, IS_AVAILABLE, IS_RETIRED) VALUES (:0, :1, :2,:3, :4, :5)",
                (name, model, brand, int(company), 0, 0))
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')

@app.route('/empty_View')
def empty():
    return render_template('empty.html')

@app.route('/add_Asset_View')
def addAssetView():
    return render_template('addAssets.html')

@app.route('/assests_View')
def assests():
    assestAva = []
    assetRet = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('Select Assets.asset_id, assets.name, assets.model, assets.brand, company.company_name, assets.is_available, assets.is_retired FROM assets.assets inner join assets.company on assets.company_id = company.company_id')
    for row in cur:
        if int(row[6]) == 1:
            assetRet.append({"id": row[0], "name": row[1], "Model":row[2], "Brand":row[3], "Company":row[4]})
        else:
            ava = True
            if int(row[5]) != 1:
               ava = False
            assestAva.append({"id": row[0], "name": row[1], "Model":row[2], "Brand":row[3], "Company":row[4],"Avaviable":ava })
    # Close the cursor and connection
    cur.close()
    connection.close()
    return render_template('assests.html',data=[assestAva,assetRet])

@app.route('/requests_View')
def requets():
    requestCl = []
    requestOp = []

    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('Select requests.request_id, requests.is_open, requests.is_approved, assets.name, employees.name FROM assets.requests inner join assets.assets on requests.asset_id = assets.asset_id inner join assets.employees on requests.employee_id = employees.employee_id')
    for row in cur:

        if int(row[1]) != 1:
            app = True
            if int(row[2]) != 1:
                app = False
            requestCl.append({"id": row[0], "is approved":app, "item":row[3], "employee":row[4]})
        else:
            app = True
            if int(row[2]) != 1:
                app = False
            requestOp.append({"id": row[0], "is approved":app, "item":row[3], "employee":row[4]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    return render_template('requests.html',data=[requestCl,requestOp])

@app.route('/history_View')
def history():
    hist = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select ASSET_HISTORY_ID,BEGIN_DATE,END_DATE,REQUEST_ID from ASSETS.HISTORY')
    for row in cur:
        hist.append({"id": row[0], "begin date": row[1], "end date":row[2], "request":row[3] })
    # Close the cursor and connection
    cur.close()
    connection.close()
    return render_template('history.html',data=hist)

@app.route('/insert_jobs_View')
def jobs_view():
    return render_template('Insert_jobs.html')



@app.route("/submit_form", methods=["GET", "POST"])
def submit_form():
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    Id = request.form["id"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    num = request.form["phone"]
    salary = request.form["salary"]
    comm = request.form["Commission"]
    job = request.form["job_id"]
    date = request.form["date"]
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    # Insert the data into the database
    cur.execute("INSERT INTO HR.Employees (EMPLOYEE_ID,FIRST_NAME, LAST_NAME, EMAIL,PHONE_NUMBER,HIRE_DATE,JOB_ID,SALARY,COMMISSION_PCT,MANAGER_ID,DEPARTMENT_ID) VALUES (:0, :1, :2,:3,:4,:5,:6,:7,:8,:9,:10)", (int(
        Id), fname, lname, email, num, date_obj, job, int(salary), float(comm), None, None))
    return render_template('after_submit.html')


if __name__ == '__main__':
    app.run()
