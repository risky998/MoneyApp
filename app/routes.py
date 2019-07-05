
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {"name" : "Rishabh Sarup"}
    render_template('index.html', title = "Home", user=user)
