from flask import Flask,render_template,url_for,request,redirect,make_response
from os import listdir

app = Flask(__name__)

list_of_mess = [["","System", "Start chat"]]

@app.route('/chat_send_mess',methods=['POST'])
def chat_send():
	global list_of_mess
	if request.method == 'POST':
		texxt = request.form['text_to_send']
		nick = request.cookies.get("nickname")
		ava = "./avatars/" + request.cookies.get("avatar")
		list_of_mess.insert(0,[ava,nick,texxt])
		return render_template('t.html',vall="test_text",text_to_chat = list_of_mess)
	else:
		return render_template('t.html',vall="test_text",text_to_chat = list_of_mess)


@app.route('/chat_send_mess')
def chat_load():
	global list_of_mess
	return render_template('t.html',vall="test_text",text_to_chat = list_of_mess)

@app.route('/chat_send_mess_load',methods=['GET'])
def chat_load_mess():
	global list_of_mess
	return render_template('ttable.html',text_to_chat = list_of_mess)

@app.route('/prepare',)
def prepare_avatar_and_nickname(errors=""):
	list_of_avatars = listdir("./avatars")
	size_col = 3
	a = [[]]
	j = 0
	for i in range(len(list_of_avatars)):
		if i % size_col == 0 and i != 0:
			j += 1
			a.append([list_of_avatars[i]])
		else:
			a[j].append(list_of_avatars[i])
	return render_template('check_a_l.html',avatars_rows = a,err_no = errors)

@app.route('/')
def start_loggin_user():
	return render_template('start_login.html',err_no = "")

@app.route('/prepare',methods=['POST'])
def check_login_and_avatar():
	if request.form['login'] == "" and request.form['avatar'] == "":
		return prepare_avatar_and_nickname("Avatar and Login are missing")
	elif request.form['avatar'] == "":
		return prepare_avatar_and_nickname("Avtar are missing")
	elif request.form['login'] == "":
		return prepare_avatar_and_nickname("Login are missing")
	else:
		global list_of_mess
		otvet = make_response(render_template('t.html',vall="test_text",text_to_chat = list_of_mess))
    	otvet.set_cookie('nickname', request.form['login'])
    	otvet.set_cookie('avatar', request.form['avatar'])
    	return otvet

@app.route('/', methods=['POST'])
def check_password():
	if request.form['password'] == "drrr":
		return redirect(url_for('prepare_avatar_and_nickname'))
	else:
		return render_template('start_login.html',err_no = "Invalid password")


@app.route('/<path_to>')
def img_load(path_to):
	if path_to.endswith("jpg"):
		return open(path_to,"r").read()
	else:
		print "ELSE"

@app.route('/avatars/<path_to>')
def avatar_load(path_to):
	if path_to.endswith("jpg") or path_to.endswith("png") or path_to.endswith("jpeg"):
		return open("./avatars/" + path_to,"r").read()
	else:
		print "ELSE"

if __name__ == "__main__":
	app.run("www.unitrino.pythonanywhere.com:80")