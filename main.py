from flask import Flask, render_template, redirect, url_for, session
from forms import LoginForm, RegistrationForm, SendMessage, AddConversation
import requests
import random
app = Flask('app')

logged = False
code = 0

app.config['SECRET_KEY'] = 'ao40592j2023ij3ospij80394nsh0eps'
@app.route('/', methods=['GET', 'POST'])
def home():
	form = SendMessage()
	User = ""
	conversation = ""
	if "user" in session:
		User = session['user']
	else:
		return redirect(url_for('login'))
	if "conversation" in session:
		conversation = session['conversation']
	if form.validate_on_submit():
		User = session["user"]
		conversation = session["conversation"]
		file = open(str(code)+".txt", "a")
		file.write("\n" + User + ": " + form.content.data)
		file.close()
		return redirect(url_for('home'))
	file = open(User+".txt", "r")
	convers = file.readlines()
	file.close()
	return render_template("index.html", convers=convers, conversation=conversation, form=form)

@app.route('/addConversation', methods=['GET', 'POST'])
def addConversation():
	form = AddConversation()
	if "user" in session:
		trash=10
		del trash
	else:
		return redirect(url_for('login'))
	if form.validate_on_submit():
		User = session['user']
		file = open("accounts.txt", "r")
		accounts = file.readlines()
		file.close()
		exists = False
		for account in accounts:
			print(account)
			if account == str(form.username.data):
				print("YAY!")
				exists = True
		if exists == True:
			session["conversation"] = form.username.data
			conversationID = str(random.randint(1,1000))
			file = open(User + ".txt", "a")
			file.write("\n"+form.username.data)
			file.close()
			file = open(User + "Codes.txt", "a")
			file.write("\n"+conversationID)
			file.close()
			file = open(form.username.data + ".txt", "a")
			file.write("\n"+User)
			file.close()
			file = open(form.username.data + "Codes.txt", "a")
			file.write("\n"+conversationID)
			file.close()
			file = open(conversationID + ".txt", "w")
			file.close()
			return redirect(url_for('home'))
			
	return render_template("addConversation.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		req = requests.get("https://www.jacktheappleyt.repl.co/login_support/"+str(form.email.data)+"/"+str(form.password.data))
		if str(req.text) != "FAIL":
			session['user'] = str(form.email.data)
		return redirect(url_for('home'))
	return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	print('Registration Page:')
	form = RegistrationForm()
	if form.validate_on_submit():
		requests.get("https://www.jacktheappleyt.repl.co/create/"+form.username.data+"/" + form.password.data)
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login_support/<username>/<password>")
def login_support(username, password):
	file = open("accounts.txt", "r")
	usernames = file.readlines()
	file.close()
	del file
	login = 0
	x = 0
	for item in usernames:
		if item.replace("\n", "") == username:
			login = x
			break
		x += 1
	if login != 0:
		file = open("password.txt", "r")
		passwords = file.readlines()
		file.close()
		del file
		if passwords[login].replace("\n", "") == password:
			return "SUCCESS"
		else:
			return "FAIL"
	else:
		return "FAIL"

@app.route("/conversation/<username>")
def conversationSet(username):
	session["conversation"] = username
	return redirect(url_for('home'))
@app.route("/renderconversation/<username>")
def render_conv(username):
	global code
	User = session['user']
	file = open(User+".txt", "r")
	names = file.readlines()
	file.close()
	file = open(User+"Codes.txt", "r")
	codes =  file.readlines()
	file.close()
	count = 0
	for name in names:
		if name == username:
			break
		count += 1
	code = int(codes[count])
	del count
	file = open(str(code)+".txt", "r")
	messages = file.readlines()
	file.close()
	print(code)
	return(render_template("conversation.html", messages=messages))
@app.route("/create/<username>/<password>")
def create(username, password):
	file = open("accounts.txt", "a")
	file.write("\n" + username)
	file.close()
	file = open("password.txt", "a")
	file.write("\n"+password)
	file.close()
	file = open(username+".txt", "w")
	file.write()
	file.close()
	file = open(username+"Codes.txt", "w")
	file.write()
	file.close()
	del file
	return("success")

app.run(host='0.0.0.0', port=8080)