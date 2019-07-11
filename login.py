from flask import Blueprint, redirect, flash, url_for, render_template
from flask_login import login_user, logout_user, current_user, login_required
from app.login.forms import LoginForm, RegistrationForm, SecretForm, ResetPasswordForm
from app.models import User, PasswordHistory, Post
from app import db
from flask_sqlalchemy import request
from werkzeug.urls import url_parse

login = Blueprint('login', __name__, template_folder='templates', static_folder='static',
                     static_url_path='/login/static')

@login.route('/login', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    if form.validate_on_submit():
        # Check if such a user exist
        user = User.query.filter_by(username=form.username.data).first()
        # If the username doesn't exist or the password is wrong. checkPassword is a function defined in my User models class.
        if user is None or not user.checkPassword(form.password.data):
            flash('Invalid username or password!', 'error')
            return redirect(url_for('login.signin'))
        # If all is good, log the user in.
        flash("Logged in! Welcome!")
        # Logs in the user. user in this case refers to the user object created by the SQL query. Remember me is handled via cookies.
        login_user(user, remember=form.rememberMe.data)
		# In the URL exists a get parameter that has the route to be redirected to. 
		# For example, if the user were to access /upload without logging in; next=upload would be in the URL
        next_page = request.args.get('next') 
		# If there is no 'next' get parameter or if its network location part is somehow empty, redirect to index
		# <scheme>://<netloc>/<path>;<params>?<query>#<fragment> is the format for a URL
		# 192.168.1.100/home The IP address is your netloc. This is done to determine if the URL is relative or absolute, for security.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@login.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:   # Redirects user to index if already logged in
		return redirect(url_for('home.index'))
	form = RegistrationForm()

	hashed_ans = ''  # Empty String by Default
	if form.validate_on_submit():
		# Sets up user object
		user = User(username=form.username.data, email=form.email.data, secret_qns=form.secret_qns.data)  # user instance to commit

		# Sets hash of password
		user.setPassword(form.password.data)
		
		# Sets hash of secret answer
		user.setSecretAnswer(form.secret_ans.data)
		
		# Sets up passwordHistory
		passwordHistory = PasswordHistory(user=user)
		db.session.add(user)
		db.session.add(passwordHistory)
		db.session.commit()
		print(f'\n**********Committed {user} to db*************\n')
		# I am using Flask-Toastr and not Flask's built-in Flash feature. Toastr is so much better.
		flash('Congratulations, you are now a registered user!', 'success')
		return redirect(url_for('login.signin'))

	return render_template('register.html', title='Register', form=form)


@login.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home.index'))


@login.route('/secret', methods=['GET', 'POST'])
def secret():
	form = SecretForm()

	# Looks at the URL to see if there is a next page to go to after
	# logging in
	next_page = request.args.get('next')

	# Looks at the URL to get username
	username = request.args.get('user')
	print(username)
	
	# Gets the user object
	user = User.query.filter_by(username=username).first()
	print(user)
	
	if form.validate_on_submit():
		print(form.secret_ans.data)
		if user.checkSecretAnswer(form.secret_ans.data):
			flash('login successful')
			# Function to log the user in
			login_user(user)
			
	 		# If no next page, goes to homepage.
			if not next_page or url_parse(next_page).netloc != '':
				next_page = url_for('home.index')
			return redirect(next_page)
		else:
			flash('Wrong answer.')
			return redirect(url_for('login.signin', next=next_page))
	return render_template('secret.html', form=form, title='Enter your Secret Answer', secret_qns=str(request.args.get('secret_qns')))


# This particular route allows the user to reset password,
# but only if the new password is not the same as the current password
# and the user's four most recent passwords after the current one.
@login.route('/reset-password', methods=['GET', 'POST'])
@login_required
def resetPassword():
	form = ResetPasswordForm()

	# Gets user and passwordHistory object
	user = User.query.filter_by(username=current_user.username).first()
	passwordHistory = PasswordHistory.query.filter_by(user_id=user.id).first()

	if form.validate_on_submit():
		try:
			# Sets the user's current password into passwordHistory.
			# This function also pushes all past passwords down one step
			passwordHistory.setNewPassword(user.password_hash)

			# Sets new password
			user.setPassword(form.new_password.data)
			
			# Adds and commits
			db.session.add(user)
			db.session.add(passwordHistory)
			db.session.commit()
			db.session.close()
		except Exception as e:
			# In case of errors, rollback
			print(f'Something went wrong: {e}')
			db.session.rollback()
	return render_template('reset-password.html', title='Reset Password', form=form)
