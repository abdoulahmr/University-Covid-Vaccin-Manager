from multiprocessing import connection
from unicodedata import category
from flask import(
    Flask,
    render_template,
    request,
    url_for
)
import sqlite3
from werkzeug.utils import redirect

# data base section
# connecting to bata-base
connection = sqlite3.connect('UniCovVacMAn.db', check_same_thread=False)

# creating cursor
cursor = connection.cursor()

# creating tables if they are not created
cursor.execute('''CREATE TABLE IF NOT EXISTS student (id INTEGER, matricule INTEGER, nom TEXT, prnom TEXT, sexe TEXT, dateness TEXT, wilaya TEXT, comune TEXT, facul TEXT, depa TEXT, anne TEXT, vaccin TEXT);''')
cursor.execute('''CREATE TABLE IF NOT EXISTS techer (id INTEGER, nom TEXT, prnom TEXT, sexe TEXT, dateness TEXT, wilaya TEXT, comune TEXT, vaccin TEXT);''')
cursor.execute('''CREATE TABLE IF NOT EXISTS worker (id INTEGER, nom TEXT, prnom TEXT, sexe TEXT, dateness TEXT, wilaya TEXT, comune TEXT, vaccin TEXT);''')
cursor.execute('''CREATE TABLE IF NOT EXISTS acconts (id INTEGER, email TEXT, password TEXT);''')
cursor.execute('''CREATE TABLE IF NOT EXISTS id (last_id INTEGER)''')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

global privlage
privlage = "guest"

def check_vac(id,type):
    id_info = cursor.execute('SELECT * FROM {type} where id = {id}'.format(type=type,id=id))
    if id_info[0][11] == 'Non':
        return 0
    else:
        return 1

def logout():
    privlage = "guest"

def addid():
    cursor.execute('''SELECT * FROM id''')
    last_id = cursor.fetchone()[0]
    cursor.execute('''UPDATE id SET last_id = {new} WHERE last_id = {old}'''.format(new = last_id + 1, old = last_id))
    connection.commit()
    return last_id+1

# home page
@app.route("/")
def home():
    return render_template("first/first.html")

# coronavirus information page
@app.route("/about-covid")
def about_covid():
    return render_template("about/about_covid.html")

# coronavirus vaccin information page
@app.route("/about-anticovid")
def about_anticovid():
    return render_template("about/about_anticovid.html")

@app.route("/Qna")
def qna():
    return render_template("qna/qna.html")

@app.route("/contact_us")
def contact_us():
    return render_template("contact/contact_us.html")

# login page
@app.route("/login",methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form['user']
        password = request.form['password']
        cursor.execute("SELECT * FROM acconts")
        accont_list = cursor.fetchall()
        cont = 0
        if user == "admin" and password == "admin":
            privlage = "admin"
            return redirect(url_for('admin'))
        else:
            while (cont!=len(accont_list)):
                if (user == accont_list[cont][1] and password == accont_list[cont][2]):
                    id = accont_list[cont][0]
                    conf = 1
                    privlage = "user"
                    return redirect('/{id}{conf}'.format(id=id,conf=conf))
                else:
                    pass
                cont =+ 1
        connection.commit()
    return render_template("login/login_page.html")

# user accont page
@app.route("/<int:id><int:conf>")
def user(id,conf):
    if (conf == 1):
        cursor.execute('SELECT * FROM student where id = {id}'.format(id=id))
        info = cursor.fetchall()
        matricule = info[0][1]
        nom  = info[0][2]
        prenom  = info[0][3]
        sexe =  info[0][4]
        dateness  = info[0][5]
        wilaya = info[0][6]
        comune = info[0][7]
        facul = info[0][8]
        depa = info[0][9]
        anne = info[0][10]
        connection.commit()
    else:
        print('error')
    return render_template("user/user-info.html",matricule=matricule,nom=nom,prenom=prenom,sexe=sexe,dateness=dateness,wilaya=wilaya,comune=comune,facul=facul,depa=depa,anne=anne)

## get paper
@app.route("/user/sertification-<int:id>-<int:conf>",methods = ['POST', 'GET'])
def sertification(id,conf):
    if (conf == 1):
        cursor.execute('SELECT * FROM student where id = {id}'.format(id=id))
        info = cursor.fetchall()
        matricule = info[0][1]
        nom  = info[0][2]
        prenom  = info[0][3]
        sexe =  info[0][4]
        dateness  = info[0][5]
        wilaya = info[0][6]
        comune = info[0][7]
        facul = info[0][8]
        depa = info[0][9]
        anne = info[0][10]
    return render_template("user/page.html")

# admin page
# home admin page
@app.route("/admin")
def admin():
    if privlage == "admin":
        print(privlage)
    return render_template("admin/admin.html")

# admin adding worker page
@app.route("/admin/add_worker",methods = ['POST', 'GET'])
def add_worker():
    if request.method == "POST":
        email_worker = request.form['email']
        password_worker = request.form['password']
        nom_worker = request.form['nom']
        prnom_worker = request.form['prnom']
        sexe_worker = request.form['check']
        dateness_worker = request.form['dateness']
        wilaya_worker = request.form['wilaya']
        comune_worker = request.form['comune']
        id = addid()
        connection.execute('''INSERT INTO worker (id,nom, prnom, sexe, dateness,
        wilaya, comune,, vaccin) VALUES('{id}','{nom}','{prnom}','{sexe}','{dateness}','{wilaya}','{comune}','Non')'''.format(id=id,nom = nom_worker,
        prnom = prnom_worker, sexe = sexe_worker, dateness = dateness_worker, wilaya = wilaya_worker, comune = comune_worker))
        connection.execute('''INSERT INTO acconts (id,email, password) VALUES('{id}','{email}','{password}')'''.format(id=id,email=email_worker,password=password_worker))
        connection.commit()
    return render_template("add/add_worker.html")

# admin adding techer page
@app.route("/admin/add_techer",methods = ['POST', 'GET'])
def add_techer():
    if request.method == "POST":
        email_techer = request.form['email']
        password_techer = request.form['password']
        nom_techer = request.form['nom']
        prnom_techer = request.form['prnom']
        sexe_techer = request.form['check']
        dateness_techer = request.form['dateness']
        wilaya_techer = request.form['wilaya']
        comune_techer = request.form['comune']
        id = addid()
        connection.execute('''INSERT INTO techer (id,nom, prnom, sexe, dateness,
        wilaya, comune, vaccin) VALUES('{id}','{nom}','{prnom}','{sexe}','{dateness}','{wilaya}','{comune}','Non')'''.format(id=id,nom = nom_techer,
        prnom = prnom_techer, sexe = sexe_techer, dateness = dateness_techer, wilaya = wilaya_techer, comune = comune_techer))
        connection.execute('''INSERT INTO acconts (id,email, password) VALUES('{id}','{email}','{password}')'''.format(id=id,email=email_techer,password=password_techer))
        connection.commit()
    return render_template("add/add_techer.html")

# admin adding student page
@app.route("/admin/add_student",methods = ['POST', 'GET'])
def add_student():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        matricule = request.form['matricule']
        nom = request.form['nom']
        prnom = request.form['prnom']
        sexe = request.form['check']
        dateness = request.form['dateness']
        wilaya = request.form['wilaya']
        comune = request.form['comune']
        facul = request.form['facul']
        depa = request.form['depa']
        anne = request.form['anne']
        id = addid()
        connection.execute('''INSERT INTO student (id,matricule, nom, prnom, sexe, dateness,
        wilaya, comune, facul, depa, anne, vaccin) VALUES('{id}','{matricule}','{nom}','{prnom}',
        '{sexe}','{dateness}','{wilaya}','{comune}','{facul}','{depa}','{anne}','Non')'''.format(id=id,matricule = matricule,
        nom = nom, prnom = prnom, sexe = sexe, dateness = dateness,
        wilaya = wilaya, comune = comune, facul = facul, depa = depa, anne = anne))
        connection.execute('''INSERT INTO acconts (id,email, password) VALUES('{id}','{email}','{password}')'''.format(id=id,email=email,password=password))
        connection.commit()
    return render_template("add/add_student.html")

if __name__ == '__main__':
    app.run(debug = True, port=5001)