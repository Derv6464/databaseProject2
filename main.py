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

@app.route('/')
def home():
    return render_template('about.html')


@app.route('/employee_view', methods=['GET', 'POST'])
def get_data():
    employPend = []
    employApp = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute(
        'Select Employees.employee_id, Employees.name, login.email, job_title.title, employees.DOB, department.dpt_name, employees.is_pending, employees.is_approved From assets.employees inner join assets.Login On Employees.login_id=Login.ID inner join assets.Job_title On Employees.job_id=Job_title.ID inner join assets.Department On Employees.department_id=department.dpt_ID')
    # Close the cursor and connection
    for row in cur:
        if int(row[6]) != 1:
            app = True
            if int(row[7]) != 1:
                app = False
            employApp.append({"Employee_ID": row[0], "Name": row[1], "Email": row[2], "Job": row[3], "dob": row[4], "dpt": row[5], "approved":app})
        else:
            app = True
            if int(row[7]) != 1:
                app = False
            employPend.append({"Employee_ID": row[0], "Name": row[1], "Email": row[2], "Job": row[3], "dob": row[4], "dpt": row[5], "approved":app})
    cur.close()
    connection.close()
    # Pass the data to the template to display in the HTML table
    return render_template('index.html', data=[employApp,employPend])

@app.route('/about_View')
def about():
    return render_template('about.html')

@app.route('/approve_req/<int:id>', methods=["GET", "POST"])
def approve_req(id):
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    exe = "UPDATE assets.requests SET requests.is_approved = 1 WHERE requests.request_id = " + str(id)
    cur.execute(exe)
    con.commit()
    return render_template('after_submit.html')

@app.route('/close_req/<int:id>', methods=["GET", "POST"])
def close_req(id):
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    exe = "UPDATE assets.requests SET requests.is_open = 0 WHERE requests.request_id = " + str(id)
    cur.execute(exe)
    con.commit()
    return render_template('after_submit.html')

@app.route('/reject_req/<int:id>', methods=["GET", "POST"])
def reject_req(id):
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    exe = "UPDATE assets.requests SET requests.is_approved = 0 WHERE requests.request_id = " + str(id)
    cur.execute(exe)
    con.commit()
    return render_template('after_submit.html')

@app.route('/close_ass/<int:id>', methods=["GET","POST"])
def close_ass(id):
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    exe = "UPDATE assets.assets SET ASSETS.IS_AVAILABLE = 0 WHERE Assets.asset_id = "+str(id)
    cur.execute(exe)
    con.commit()
    return render_template('after_submit.html')

@app.route('/avail_ass/<int:id>', methods=["GET","POST"])
def avail_ass(id):
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    exe = "UPDATE assets.assets SET ASSETS.IS_AVAILABLE = 1 WHERE Assets.asset_id = "+str(id)
    cur.execute(exe)
    con.commit()
    return render_template('after_submit.html')

@app.route('/retire_ass/<int:id>', methods=["GET","POST"])
def retire_ass(id):
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    exe = "UPDATE assets.assets SET ASSETS.IS_RETIRED = 1 WHERE Assets.asset_id = "+str(id)
    cur.execute(exe)
    con.commit()
    return render_template('after_submit.html')

@app.route('/unapp_employ/<int:id>', methods=["GET","POST"])
def unapp_employ(id):
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    exe = "UPDATE assets.employees SET employees.IS_APPROVED = 0 WHERE employees.employee_id = "+str(id)
    cur.execute(exe)
    con.commit()
    return render_template('after_submit.html')

@app.route('/app_employ/<int:id>', methods=["GET","POST"])
def app_employ(id):
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    exe = "UPDATE assets.employees SET employees.IS_APPROVED = 1 WHERE employees.employee_id = "+str(id)
    cur.execute(exe)
    con.commit()
    return render_template('after_submit.html')

@app.route('/pend_employ/<int:id>', methods=["GET","POST"])
def pend_employ(id):
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    exe = "UPDATE assets.employees SET employees.IS_APPROVED = 1 WHERE employees.employee_id = "+str(id)
    cur.execute(exe)
    con.commit()
    return render_template('after_submit.html')

@app.route('/Add_Assets', methods=["GET", "POST"])
def getAssetData():
    name = request.form["name"]
    model = request.form["model"]
    brand = request.form["brand"]
    company = request.form["compId"]

    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    # print("INSERT INTO HR.JOBS(JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY) VALUES (:0, :1, :2,:3)", (id, title,  int(min), int(max)))

    cur.execute(
        "INSERT INTO ASSETS.ASSETS(NAME, MODEL, BRAND, COMPANY_ID, IS_AVAILABLE, IS_RETIRED) VALUES (:0, :1, :2,:3, :4, :5)",
        (name, model, brand, int(company), 0, 0))
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')

@app.route('/Add_Employ', methods=["GET", "POST"])
def getEmploy():
    name = request.form["name"]
    logIn = request.form["login"]
    dob = request.form["dob"]
    job = request.form["job"]
    dept = request.form["dept"]
    dob_obj = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()

    cur.execute(
        "INSERT INTO ASSETS.EMPLOYEES(NAME, LOGIN_ID, DOB, JOB_ID, DEPARTMENT_ID, IS_APPROVED, IS_PENDING) VALUES (:0, :1, :2,:3, :4, :5, :6)",
        (name, int(logIn), dob_obj, int(job), int(dept), 0, 1))
    con.commit()
    cur.close()
    return render_template('after_submit.html')

@app.route('/add_employ_View', methods=["GET", "POST"])
def addEmployView():
    job = []
    dept = []
    login = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select ID, TITLE from ASSETS.JOB_TITLE')
    for row in cur:
        job.append({"id": row[0], "name": row[1]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select DPT_ID, DPT_NAME from ASSETS.DEPARTMENT')
    for row in cur:
        dept.append({"id": row[0], "name": row[1]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select ID, EMAIL from ASSETS.LOGIN')
    for row in cur:
        login.append({"id": row[0], "name": row[1]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    return render_template('addEmployee.html', data=[job,dept,login])

@app.route('/Add_Request', methods=["GET", "POST"])
def getRequestData():
    asset = request.form["assId"]
    employee = request.form["empId"]
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    # print("INSERT INTO HR.JOBS(JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY) VALUES (:0, :1, :2,:3)", (id, title,  int(min), int(max)))

    cur.execute("INSERT INTO ASSETS.REQUESTS(IS_OPEN, IS_APPROVED, ASSET_ID, EMPLOYEE_ID) VALUES (:0, :1, :2,:3)",
                (1, 0, int(asset), int(employee)))
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')

@app.route('/Add_Login', methods=["GET", "POST"])
def getLoginData():
    email = request.form["email"]
    passwordIn = request.form["password"]
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    # print("INSERT INTO HR.JOBS(JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY) VALUES (:0, :1, :2,:3)", (id, title,  int(min), int(max)))

    cur.execute("INSERT INTO ASSETS.LOGIN(EMAIL, PASSWORD) VALUES (:0, :1)",
                (email, passwordIn))
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')

@app.route('/add_Asset_View', methods=["GET", "POST"])
def addAssetView():
    assets = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select COMPANY_ID, COMPANY_NAME from ASSETS.COMPANY')
    for row in cur:
        assets.append({"id": row[0], "name": row[1]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    return render_template('addAssets.html', data=assets)

@app.route('/add_Login_View', methods=["GET", "POST"])
def addLoginView():
    login = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select EMAIL, PASSWORD from ASSETS.LOGIN')
    for row in cur:
        login.append({"email": row[0], "password": row[1]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    return render_template('addLogin.html', data=login)

@app.route('/add_Request_View', methods=["GET", "POST"])
def addRequestView():
    assetRequests = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select ASSET_ID, NAME from ASSETS.ASSETS')
    for row in cur:
        assetRequests.append({"id": row[0], "name": row[1]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    empRequests = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select EMPLOYEE_ID, NAME from ASSETS.EMPLOYEES')
    for row in cur:
        empRequests.append({"id": row[0], "name": row[1]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    return render_template('addRequest.html', data=[assetRequests, empRequests])

@app.route('/assests_View')
def assests():
    assestAva = []
    assetRet = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute(
        'Select Assets.asset_id, assets.name, assets.model, assets.brand, company.company_name, assets.is_available, assets.is_retired FROM assets.assets inner join assets.company on assets.company_id = company.company_id')
    for row in cur:
        if int(row[6]) == 1:
            assetRet.append({"id": row[0], "name": row[1], "Model": row[2], "Brand": row[3], "Company": row[4]})
        else:
            ava = True
            if int(row[5]) != 1:
                ava = False
            assestAva.append(
                {"id": row[0], "name": row[1], "Model": row[2], "Brand": row[3], "Company": row[4], "Avaviable": ava})
    # Close the cursor and connection
    cur.close()
    connection.close()
    return render_template('assests.html', data=[assestAva, assetRet])

@app.route('/requests_View')
def requets():
    requestCl = []
    requestOp = []
#pls work
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute(
        'Select requests.request_id, requests.is_open, requests.is_approved, assets.name, employees.name FROM assets.requests inner join assets.assets on requests.asset_id = assets.asset_id inner join assets.employees on requests.employee_id = employees.employee_id')
    for row in cur:
        if int(row[1]) != 1:
            app = True
            if int(row[2]) != 1:
                app = False
            requestCl.append({"id": row[0], "is approved": app, "item": row[3], "employee": row[4]})
        else:
            app = True
            if int(row[2]) != 1:
                app = False
            requestOp.append({"id": row[0], "is approved": app, "item": row[3], "employee": row[4]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    return render_template('requests.html', data=[requestCl, requestOp])

@app.route('/history_View')
def history():
    hist = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select ASSET_HISTORY_ID,BEGIN_DATE,END_DATE,REQUEST_ID from ASSETS.HISTORY')
    for row in cur:
        hist.append({"id": row[0], "begin date": row[1], "end date": row[2], "request": row[3]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    return render_template('history.html', data=hist)

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
    cur.execute(
        "INSERT INTO HR.Employees (EMPLOYEE_ID,FIRST_NAME, LAST_NAME, EMAIL,PHONE_NUMBER,HIRE_DATE,JOB_ID,SALARY,COMMISSION_PCT,MANAGER_ID,DEPARTMENT_ID) VALUES (:0, :1, :2,:3,:4,:5,:6,:7,:8,:9,:10)",
        (int(
            Id), fname, lname, email, num, date_obj, job, int(salary), float(comm), None, None))
    return render_template('after_submit.html')

if __name__ == '__main__':
    app.run()
