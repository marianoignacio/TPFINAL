from flask import Flask, render_template, request, redirect, flash, url_for, jsonify

import json

app = Flask(__name__)

@app.route('/')
def home ():
    return render_template('index.html')

if __name__== '__main__':
        app.run("localhost", port=8088, debug=True)