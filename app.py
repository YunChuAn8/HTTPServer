from flask import Flask,render_template,request, jsonify
import time
import math
import random

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/sqrt', methods=['POST'])
def sqrt():
    data = request.get_json()
    number = data.get('number', 0)

    delay = random.uniform(0.1, 0.19)
    time.sleep(delay)
    result = math.sqrt(number)

    return jsonify({'result': result, 'delay': delay}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
