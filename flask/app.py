from flask import Flask, render_template, request, jsonify,url_for,redirect,flash
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key'

#sql資料庫的環境設置
def get_data():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-CGJ6AVJ;'
        'DATABASE=專題;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.老師資料")
    data = cursor.fetchall()
    conn.close()
    return data

#html界面各個
@app.route("/")
def first():
    return redirect(url_for('web'))

@app.route("/web")
def web():
    return render_template("web.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/home")
def home():
    return render_template("Shome.html")

@app.route("/Sinput", methods=["GET", "POST"])
def Sinput():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-CGJ6AVJ;'
                'DATABASE=專題;'
                'Trusted_Connection=yes;'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dbo.Students WHERE Student_id = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return redirect(url_for('Shome'))
            else:
                flash('帳號或密碼錯誤', 'error')
        except Exception as e:
            print(f"Error: {e}")  # 打印错误信息到控制台
            flash('賬號或密碼錯誤，請重新再試', 'error')
    
    return render_template("Sinput.html")

@app.route("/Tinput", methods=["GET", "POST"])
def Tinput():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-CGJ6AVJ;'
                'DATABASE=專題;'
                'Trusted_Connection=yes;'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dbo.老師資料 WHERE Teacher_id = ? AND Password = ?", (username, password))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return redirect(url_for('Thome'))
            else:
                flash('帳號或密碼錯誤', 'error')
        except Exception as e:
            print(f"Error: {e}")  # 打印错误信息到控制台
            flash('賬號或密碼錯誤，請重新再試', 'error')
    
    return render_template("Tinput.html")

@app.route("/Thome")
def Thome():
    return render_template("Thome.html")

@app.route("/Shome")
def Shome():
    return render_template("Shome.html")

@app.route('/index')
def index():
    data = get_data()
    return render_template('index.html', data=data)

@app.route("/wait")
def wait():
    return render_template("wait.html")

if __name__ == "__main__":
    app.run()