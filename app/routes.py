from app import app

# Decorators: modifies the fucntion that follows it.
# A common pattern with decorators is to use them to register functions as callbacks for certain events.
# In this case, the @app.route decorator creates an association between the URL given as an argument and the function.
@app.route('/')
@app.route('/index')

def index():
    return "Hello, World!, anything else?"