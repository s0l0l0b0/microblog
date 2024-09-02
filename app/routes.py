from flask  import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

# Decorators: modifies the fucntion that follows it.
# A common pattern with decorators is to use them to register functions as callbacks for certain events.
# In this case, the @app.route decorator creates an association between the URL given as an argument and the function.
@app.route('/')


@app.route('/index')
def index():
    user = {'username': 'father'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)


# This function mapped to the /login URL that creates a form
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
