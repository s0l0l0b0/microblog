from flask  import render_template
from app import app

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