from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify

from . models import User, Posts, db
from . forms import AddPostForm, SignUpForm, SignInForm, AboutUserForm

import uuid
import string
import random

from blog import oidc, app


class CreateShadowUserException(Exception):
	pass

def shadow_register(*args, **kwargs):
	username = str(uuid.uuid4())
	try:
		reg = User("", "", username,
		           ''.join(random.choices(string.digits+string.ascii_letters + string.punctuation, k=50)),
		           kwargs.get("email"))

		db.session.add(reg)
		db.session.commit()
		return username
	except:
		raise CreateShadowUserException

@app.route('/oidclogin')
@oidc.require_login
def oidclogin():
	# return 'Welcome {}!! Livinig in {}'.format(oidc.user_getfield('email'), oidc.user_getfield('address'))
	if oidc.user_loggedin:
		email = oidc.user_getfield('email')
		address = oidc.user_getfield('address')
		user = User.query.filter_by(email=email).first()
		if user is not None:
			session['current_user'] = user.username
			session['user_available'] = True
			return redirect(url_for('about_user'))
		else:
			username = shadow_register(email=email, address=address)
			if username:
				session['current_user'] = username
				session['user_available'] = True
			else:
				return "Could not create user in local DB"

		return redirect(url_for('index'))

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/posts')
def show_posts():
	if session['user_available']:
		posts = Posts.query.all()
		user = User.query.all()
		return render_template('posts.html', posts=posts, user=user)
	flash('User is not Authenticated')
	return redirect(url_for('index'))


@app.route('/add', methods=['GET', 'POST'])
def add_post():
	if session['user_available']:
		blogpost = AddPostForm(request.form)
		us = User.query.filter_by(username=session['current_user']).first()
		if request.method == 'POST':
			bp = Posts(blogpost.title.data, blogpost.description.data, us.uid)
			db.session.add(bp)
			db.session.commit()
			return redirect(url_for('show_posts'))
		return render_template('add.html', blogpost=blogpost)
	flash('User is not Authenticated')
	return redirect(url_for('index'))


@app.route('/delete/<pid>/<post_owner>', methods=('GET', 'POST'))
def delete_post(pid, post_owner):
	if session['current_user'] == post_owner:
		me = Posts.query.get(pid)
		db.session.delete(me)
		db.session.commit()
		return redirect(url_for('show_posts'))
	flash('You are not a valid user to Delete this Post')
	return redirect(url_for('show_posts'))


@app.route('/update/<pid>/<post_owner>', methods=('GET', 'POST'))
def update_post(pid, post_owner):
	if session['current_user'] == post_owner:
		me = Posts.query.get(pid)
		blogpost = AddPostForm(obj=me)
		if request.method == 'POST':
			bpost = Posts.query.get(pid)
			bpost.title = blogpost.title.data
			bpost.description = blogpost.description.data
			db.session.commit()
			return redirect(url_for('show_posts'))
		return render_template('update.html', blogpost=blogpost)
	flash('You are not a valid user to Edit this Post')
	return redirect(url_for('show_posts'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	signupform = SignUpForm(request.form)
	if request.method == 'POST':
		reg = User(signupform.firstname.data, signupform.lastname.data, \
		           signupform.username.data, signupform.password.data, \
		           signupform.email.data)
		db.session.add(reg)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('signup.html', signupform=signupform)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	signinform = SignInForm()
	if request.method == 'POST':
		em = signinform.email.data
		log = User.query.filter_by(email=em).first()
		if log.password == signinform.password.data:
			current_user = log.username
			session['current_user'] = current_user
			session['user_available'] = True
			return redirect(url_for('show_posts'))
	return render_template('signin.html', signinform=signinform)


@app.route('/about_user')
def about_user():
	aboutuserform = AboutUserForm()
	if session['user_available']:
		user = User.query.filter_by(username=session['current_user']).first()
		return render_template('about_user.html', user=user, aboutuserform=aboutuserform)
	flash('You are not a Authenticated User')
	return redirect(url_for('index'))


@app.route('/logout')
def logout():
	session.clear()
	session['user_available'] = False
	oidc.logout()
	return redirect(url_for('index'))


@app.route('/blog/api/v0.1/posts', methods=['GET'])
def get_tasks():
	posts = Posts.query.all()
	"""for i in api_posts:
		title= i.title
		description = i.description
		data_dict= {'title': title, 'description': description}"""
	"""for i in posts:
		t[i] = posts.title
	print(t)"""
	title = posts.title
	print(title)
	description = posts.description
	return jsonify(title=title, description=description)


if __name__ == '__main__':
	app.run()
