from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
# Agregué jsonify lo demás son funciones del último tp



app = Flask(__name__)
"""
@app.route('/users', methods = ['GET'])
def users ():
    
    result = {"id": 1, "name": "Mariano", "email": "mampcpel@gmail.com", "active": True}
        
    data=[]
    for row in result:
              entity['id'] = row['id']
              entity['name'] = row['name']
              entity['email'] = row['email']
              entity['active'] = row['active']
              data.append(entity)

    return jsonify(data),200
"""
"""@app.route('/user/<id>', methods = ['GET'])
def users (id):
    result = {"id": 1, "name": "Mariano", "email": "mampcpel@gmail.com", "active": True}
    for row in result:
         if row('id') == int(id):
              entity['id'] = row['id']
              entity['name'] = row['name']
              entity['email'] = row['email']
              entity['active'] = row['active']
              data.append(entity)

    return jsonify(data),200
"""


if __name__== '__main__':
        app.run("localhost", port=8088, debug=True)