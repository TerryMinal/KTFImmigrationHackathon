from flask import Flask, redirect, url_for, session, request, render_template
from utils import bridge, authen

app = Flask(__name__)
app.secret_key = "lol"


@app.route("/")
def root():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route("/login/")
def login():
    message = "" 
    if 'message' in request.args:
        message = request.args.get('message')
    return render_template("login.html", message = message)

@app.route("/register/")
def register():
    message = ""
    if 'message' in request.args:
        message = request.args.get('message')
    return render_template("register.html", message = message)


@app.route("/logout/")
def logout():
    session.pop("username")
    return redirect(url_for("root"))


@app.route("/authenticate/", methods = ['POST', 'GET'])
def authenticate():
    data = authen.dbHandler()
    userNames = data['usernames']
    passWords = data['passwords']
    checkBoxList = request.form.getlist("interests")
    print request.form
    print checkBoxList
    if request.form['account'] == 'Login':
        val = authen.authenticate(request.form, userNames, passWords )
        if val == True :
            session['username'] = request.form['username']
            return redirect(url_for('root'))
        else:
            return redirect(url_for('login', message = val))
    elif request.form['account'] == 'Register':
        val = authen.register(checkBoxList, request.form, userNames, passWords)
        if val == True :
            return redirect(url_for('login', message = "Registration Successful", ))
        else:
            return redirect(url_for('register', message = val))
    else:
        return redirect(url_for( 'root' ) )
    
@app.route("/home/")
def home():
    return render_template("home.html")

#@app.route("/blogs")
#def blogs():
#    return render_template(blog

if __name__ == "__main__":
    app.debug = True
    app.run()

