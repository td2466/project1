#!/usr/bin/env python2.7

# My comments: (Jialiu Wang)
# There are some concepts/names we must understand before using these tools.
# For the most part, we are using three things:
#   HTML for web pages
#   FLASK for handling database
#   JINJA for generating HTML from templates
#
# HTML uses tags to arrange its contents.
# We are using a lot of different tags, including (but not constrained to):
#   <!--   --> for comments
#   <!DOCTYPE> for document declaration
#   <a>   </a> for hyperlinks
#   <br />     for line breaks
#   <dl>       for definition lists
#       <dd>   </dd>        component of definition lists
#       <dt>   </dt>        component of definition lists
#   </dl>      for definition lists
#   <h1>   </h1>    for headings of different sizes
#   <h2>   </h2>    for headings of different sizes
#   <h3>   </h3>    for headings of different sizes
#   <h4>   </h4>    for headings of different sizes
#   <h5>   </h5>    for headings of different sizes
#   <h6>   </h6>    for headings of different sizes
#   <head>   </head>    for head section of an HTML document
#   <html>   </html>    for the whole HTML document
#   <input />  for various kinds of input field
#   <p>   </p> for a (simple) paragraph
#   <title>   </title>      for the title of page (displayed on top of the browser toolbar)
#   <ul>       for unordered lists
#       <li>   </li>        component of unordered lists
#   </ul>      for unordered lists
# For more information and better understanding on HTML,
# I recommend reading http://www.w3school.com.cn/tags/ (in Chinese)
# and http://www.w3schools.com/tags/ (in English).
#
# FLASK is a micro webdevelopment framework for Python.
# It is used as an imported class (Flask class as imported in this
# python code).
# `app = Flask(__name__, template_folder=tmpl_dir)`
# So `app` is an instance of Flask class in our code.
# @app.route() is called a route() decorator. A route() decorator
# is used to bind a function to a URL. Inside the parenthesis
# is (generally) the URL which will trigger the corresponding
# function.
# The function that a route() decorator is bound to (of course)
# has a name. The name is called "endpoint" in Flask. Therefore,
# each route() decorator binds a URL with an endpoint function.
# But as programmers, we love variables and using variables to
# achieve fancy things. The URL used in route() decorator
# has variable (or I should call it "dynamic") parts like
# <variable_name>. Such a dynamic name will also be a parameter
# of the endpoint function the (variable) URL binds to.
# Another important usage of Flask is, the url_for() function.
# In our project, url_for() functions can be called from Jinja
# templates and give us the disired URLs. url_for() function
# takes endpoint (name of function) as input.
# Flask is used to generate dynamic HTML pages based on user
# inputs in our project, guide and redirect user from page
# to page, call Jinja to render HTML pages, communicate with
# the database and handle user
# input as in HTML forms. Therefore it is the core part of this
# project.
# Flask can also handle different HTTP methods, which is also
# used in this project.
# For more information and better, comprehensive understanding
# on Flask, I recommend reading
# http://flask.pocoo.org/docs/0.10/quickstart/
# and more documents on Flask documentation site:
# http://flask.pocoo.org/docs/0.10/
#
# JINJA is a tool for designing text file templates. It is
# able to generate templates for various kinds of text files
# such as HTML, XML, CSV, LaTeX etc.
# It has variables, statements, comments, control structures
# as a programming language. And more importantly, Jinja has
# a very useful feature called templates inheritance.
# It would be extremely easy to use Jinja to write your own
# templates for structured text files, if you have extensive
# experience on programming.
# Jinja mainly use syntax like {{ item }} to represent
# expressions, {% for ... %} to represent statements (control
# structures). With these in mind, it is very easy to understand
# a template written with Jinja.
# Recommended reading
# http://jinja.pocoo.org/docs/dev/templates/

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111db.eastus.cloudapp.azure.com/username
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db.eastus.cloudapp.azure.com/ewu2493"
#
DATABASEURI = "postgresql://rx2138:XRJDFZ@w4111db.eastus.cloudapp.azure.com/rx2138"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
# 
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
#engine.execute("""DROP TABLE IF EXISTS test;""")
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
#
# END SQLITE SETUP CODE
#



@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request 
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request

    The variable g is globally accessible
    """
    try:
        g.conn = engine.connect()
    except:
        print "uh oh, problem connecting to database"
        import traceback; traceback.print_exc()
        g.conn = None

@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/', methods=['GET', 'POST'])
def login():
    """
    request is a special object that Flask provides to access web request information:

    request.method:   "GET" or "POST"
    request.form:     if the browser submitted a form, this contains the data in the form
    request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

    See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
    """

# DEBUG: this is debugging code to see what request looks like
    print request.args

#
# example of a database query
#
    cursor = g.conn.execute("SELECT username FROM Users")
    names = []
    for result in cursor:
        names.append(result['username'])  # can also be accessed using result[0]
    cursor.close()

#
# Flask uses Jinja templates, which is an extension to HTML where you can
# pass data to a template and dynamically generate HTML based on the data
# (you can think of it as simple PHP)
# documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
#
# You can see an example template in templates/index.html
#
# context are the variables that are passed to the template.
# for example, "data" key in the context variable defined below will be 
# accessible as a variable in index.html:
#
#     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
#     <div>{{data}}</div>
#     
#     # creates a <div> tag for each element in data
#     # will print: 
#     #
#     #   <div>grace hopper</div>
#     #   <div>alan turing</div>
#     #   <div>ada lovelace</div>
#     #
#     {% for n in data %}
#     <div>{{n}}</div>
#     {% endfor %}
#
    context = dict(data = names)

    message = None
    if request.method == 'POST':
        cursor = g.conn.execute("SELECT username FROM Users WHERE username='" + request.form['username'] + "'")
        counter = 0
        for row in cursor:
            counter += 1
        cursor.close()
        if counter != 1:
            message = 'Invalid username'
            context['error'] = message
            return render_template('login.html', **context)

        cursor = g.conn.execute("SELECT password FROM Users WHERE username='" + request.form['username'] + "'")
        counter = 0
        passwdFound = ''
        for row in cursor:
            if counter == 0:
                passwdFound = row['password']
            counter += 1
        cursor.close()
        if passwdFound != request.form['password']:
            message = 'Invalid password'
            context['error'] = message
            return render_template('login.html', **context)
        return redirect(url_for('user', username = request.form['username']))

#
# render_template looks in the templates/ folder for files.
# for example, the below file reads template/index.html
#
    return render_template("login.html", **context)

@app.route('/user/<username>')
def user(username):
# DEBUG: this is debugging code to see what request looks like
    print request.args
    cursor = g.conn.execute("SELECT * FROM Users WHERE username='" + username + "'")
    for row in cursor:
        vals = row
    cursor.close()
    context = dict(userData = vals)
    return render_template("user.html", **context)

@app.route('/ebookList')
def ebookList():
    print request.args
    print request.args['username']
    cursor = g.conn.execute("SELECT title,isbn FROM Ebooks")
    booklist = []
    for row in cursor:
        booklist.append(row)
    cursor.close()
    context = dict(ebookList = booklist)
    context['username'] = request.args['username']
    return render_template("ebookList.html", **context)

@app.route('/ebook/<isbn>')
def ebook(isbn):
# DEBUG: this is debugging code to see what request looks like
    print request.args
    cursor = g.conn.execute("SELECT * FROM Ebooks WHERE isbn='" + isbn + "'")
    for row in cursor:
        vals = row
    cursor.close()
    context = dict(ebookInfo = vals)
    context['username'] = request.args['username']
    return render_template("ebook.html", **context)

@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    print request.args
    
    #request.form['itemNumber']
    #request.form['isbn']
    itemnumber = int(request.form['itemNumber'])
    context = dict()
    context['username'] = request.form['username']
    if itemnumber > 0:
        oid_list = []
        cursor = g.conn.execute("SELECT oid FROM Have_Orders")
        for row in cursor:
            oid_list.append(int(row['oid']))
        oid = max(oid_list) + 1
        g.conn.execute("INSERT INTO Have_Orders VALUES (%d, '%s')" % (oid, request.form['username']))
        g.conn.execute("INSERT INTO Add_to VALUES (%d, '%s', %d)" % (itemnumber, request.form['isbn'], oid))
        #g.conn.execute("INSERT INTO Orders_Pay VALUES (%d, %d)" % (oid, number))
        context['isbn'] = request.form['isbn']
        context['itemNumber'] = request.form['itemNumber']
 
    else:
        context['error'] = "Invalid number of books ordered"
        #return redirect(url_for('user', username = request.form['username']))
    cursor = g.conn.execute("SELECT oid, isbn, quantity FROM Add_to")
    order_list = []
    for row in cursor:
        order_list.append(row)
    cursor.close()
    context['orderlist'] = order_list
    cursor = g.conn.execute("SELECT oid FROM Have_Orders WHERE username='" + request.form['username'] + "'")
    user_oid_list = []
    for row in cursor:
        user_oid_list.append(row['oid'])
    cursor.close()
    context['useroidlist'] = user_oid_list
    return render_template("order.html", **context)
    
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    print request.args
    context = dict()
    context['username'] = request.form['username']
    cursor = g.conn.execute("SELECT type, number FROM Own_Cards WHERE username='" + request.form['username'] + "'")
    user_card_list = []
    for row in cursor: 
        user_card_list.append(row)
    cursor.close()
    context['usercardlist'] = user_card_list
    return render_template("payment.html", **context)

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    print request.args
    context = dict()
    context['username'] = request.form['username']
    cursor = g.conn.execute("SELECT timestamp, comment FROM Submit_Comments WHERE username='" + request.form['username'] + "'")
    user_comment = []
    for row in cursor: 
        user_comment.append(row)
    cursor.close()
    context['usercomment'] = user_comment
    return render_template("comment.html", **context)

@app.route('/loginpage')
def loginpage():
    return render_template("login.html")
    
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
#@app.route('/another')
#def another():
  # DEBUG: this is debugging code to see what request looks like
#  print request.args
#  return render_template("anotherfile.html")

  
#@app.route('/login', methods=['GET', 'POST'])
#def login():
    #error = None
    #if request.method == 'POST':
        #if request.form['username'] != app.config['USERNAME']:
            #error = 'Invalid username'
        #elif request.form['password'] != app.config['PASSWORD']:
            #error = 'Invalid password'
        #else:
            #session['logged_in'] = True
            #flash('You were logged in')
            #return redirect(url_for('show_entries'))
    #return render_template('index.html', error=error)
    
#@app.route('/show_entries')
#def show_entries():
  # DEBUG: this is debugging code to see what request looks like
#  print request.args
#  curUser = request.form['username']
#  cursor = g.conn.execute("SELECT * FROM Users WHERE username = curUser")  # how to establish a connection btw this usrn & input
#  info = []
#  for result in cursor:
#    info.append(result['*'])  # can also be accessed using result[0]
#  cursor.close()
#  context = dict(data2 = info)
#  return render_template("show_entries.html")
  
if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=True, threaded=threaded)


  run()
