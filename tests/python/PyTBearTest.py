from bears.python.PyTBear import PyTBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

test_safe = """
def safe():
    pass
"""


test_XSS = """
from flask import Flask, request, make_response
app = Flask(__name__)

@app.route('/XSS_param', methods =['GET'])
def XSS1():
    param = request.args.get('param', 'not set')

    html = open('templates/xss.html').read()
    resp = make_response(html.replace('{{ param }}', param))
    return resp

if __name__ == '__main__':
    app.run(debug= True)
"""


test_inter_command_injection = """
import subprocess
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    with open('menu.txt','r') as f:
        menu = f.read()

    return render_template('command_injection.html', menu=menu)

def shell_the_arg(arg):
    subprocess.call(arg, shell=True)

@app.route('/menu', methods=['POST'])
def menu():
    param = request.form['suggestion']

    shell_the_arg('echo ' + param + ' >> ' + 'menu.txt')

    with open('menu.txt','r') as f:
        menu = f.read()

    return render_template('command_injection.html', menu=menu)

@app.route('/clean')
def clean():
    subprocess.call('echo Menu: > menu.txt', shell=True)

    with open('menu.txt','r') as f:
        menu = f.read()

    return render_template('command_injection.html', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)

"""


PyTBearDefaultsTest = verify_local_bear(
    PyTBear,
    valid_files=(test_safe,),
    invalid_files=(test_XSS, test_inter_command_injection,))
