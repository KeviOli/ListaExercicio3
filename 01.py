from flask import Flask, request

app = Flask(__name__)

@app.route('/adicao')
def add():
    num1 = float(request.args.get('num1'))
    num2 = float(request.args.get('num2'))
    result = num1 + num2
    return str(result)

@app.route('/subtracao')
def subtract():
    num1 = float(request.args.get('num1'))
    num2 = float(request.args.get('num2'))
    result = num1 - num2
    return str(result)

@app.route('/multiplicacao')
def multiply():
    num1 = float(request.args.get('num1'))
    num2 = float(request.args.get('num2'))
    result = num1 * num2
    return str(result)

@app.route('/divisao')
def divide():
    num1 = float(request.args.get('num1'))
    num2 = float(request.args.get('num2'))
    if num2 == 0:
        return "Error: não tem como dividir por zero"
    result = num1 / num2
    return str(result)

if __name__ == '__main__':
    app.run(debug=True)
