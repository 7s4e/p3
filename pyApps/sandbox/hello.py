from flask import Flask, url_for, request, render_template
from markupsafe import escape

app = Flask(__name__)

# url_for('static', filename='style.css')

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_world():
    return "<p>Hello World!</p>"

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "do_the_login()"
    else:
        return "show_the_login_form()"
    
# @app.get('/login')
# def login_get():
#     return show_the_login_form()

# @app.post('/login')
# def login_post():
#     return do_the_login()
    
@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'


'''
Case 1: a module:
/application.py
/templates
    /hello.html

Case 2: a package:
/application
    /__init__.py
    /templates
        /hello.html
'''