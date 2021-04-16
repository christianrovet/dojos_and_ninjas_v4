from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)

@app.route('/dojo')
def dojo():
    mysql = connectToMySQL('dojos_and_ninjas')
    dojos = mysql.query_db('SELECT * FROM dojos;')
    return render_template('dojo.html', dojos = dojos)

@app.route('/create_dojo', methods=['POST'])
def create_dojo():
    mysql = connectToMySQL('dojos_and_ninjas')
    query = "INSERT INTO dojos (name, created_at,updated_at) VALUES (%(name)s, NOW(), NOW());"
    data = {
        "name": request.form['name']
    }
    mysql.query_db(query,data)
    return redirect('/dojo')

@app.route('/ninjas')
def ninjas():
    mysql = connectToMySQL('dojos_and_ninjas')
    dojos = mysql.query_db('SELECT * FROM dojos')
    return render_template('ninja.html', dojos = dojos)

@app.route('/create_ninja', methods=["POST"])
def create_ninja():
    # print(request.form[])
    mysql = connectToMySQL('dojos_and_ninjas')
    query = "INSERT INTO ninjas (first_name, last_name, age, created_at,updated_at, dojo_id) VALUES(%(first_name)s, %(last_name)s, %(age)s, NOW(), NOW(), %(dojo_id)s);"
    data = {
        "first_name": request.form['firstname'],
        "last_name": request.form['lastname'],
        "age": request.form['age'],
        "dojo_id": request.form['dojo_id']
    }
    mysql.query_db(query,data)
    return redirect('/ninjas')

@app.route('/show/<int:dojo_id>')
def show(dojo_id):
    mysql = connectToMySQL('dojos_and_ninjas')
    query = 'SELECT * FROM dojos LEFT JOIN ninjas ON dojo_id = dojos.id WHERE dojos.id = %(id)s ;'
    data = {
        'id': dojo_id
    }
    ninjas_dojos = mysql.query_db(query,data)
    print(ninjas_dojos)
    return render_template('dojo_show.html', ninjas_dojos=ninjas_dojos)


if __name__ == "__main__":
    app.run(debug=True)