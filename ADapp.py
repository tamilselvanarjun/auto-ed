from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

import numpy as np
from ADnum_rev_timed_vis import ADnum
import ADmath_rev as ADmath
import ADgraph_GUI as ADgraph

@app.route('/', methods = ["GET", "POST"])
def startup():
    errors = ""
    if request.method == "POST":
        try:
            ins = int(request.form["inputs"])
            assert ins>0
        except:
            errors += "<p> Please enter a positive integer number of inputs.</p>"
            return render_template('welcome.html', errors=errors)
        
        try:
            outs = int(request.form["outputs"])
            assert outs>0
        except:
            errors += "<p> Please enter a positive integer number of outputs.</p>"
            return render_template('welcome.html', errors=errors)
        if ins>5:
            errors += "<p> More than 5 inputs is not supported in the web app environment.  Please either use the AD?? package or experiment with a fewer number of variables.</p>"
            return render_template('welcome.html', errors=errors)
        if outs>3:
            errors += "<p> More than 3 outputs is not supported in the web app environmnent.  Please either use the AD?? package or experiment with a fewer number of functions.</p>"
            return render_template('welcome.html', errors=errors)
        global master_ins
        master_ins = ins
        global master_outs
        master_outs = outs
        return redirect(url_for('calculate'))
    return render_template('welcome.html', errors=errors)

@app.route('/calculate', methods = ["GET", "POST"])
def calculate():
    if request.method == "POST":
        if request.form["action"] == "Calculate":
            return redirect(url_for('graphwindow'))
        else:
            calcfuncs[request.form["action"]]()
    return render_template('calculator.html', func_content = func_content, calcfuncs=calcfuncs, ins=master_ins, outs=master_outs, flabels = flabels)

@app.route('/graphwindow', methods = ["GET", "POST"])
def graphwindow():
    errors = ""
    if request.method == "POST":
        if request.form["action"] == "Set Input Values":
            try:
                global x
                x = [ADnum(float(request.form["x"]), ins=master_ins, ind=0)]*master_outs
                if master_ins>1:
                    global y
                    y=[ADnum(float(request.form["y"]), ins=master_ins, ind=1)]*master_outs
                if master_ins>2:
                    global z
                    z=[ADnum(float(request.form["z"]), ins=master_ins, ind=2)]*master_outs
                if master_ins>3:
                    global u
                    u=[ADnum(float(request.form["u"]), ins=master_ins, ind=3)]*master_outs
                if master_ins>4:
                    global v
                    v=[ADnum(float(request.form["v"]), ins=master_ins, ind=1)]*master_outs
            except:
                errors += "Please enter numeric values for all of the inputs."
    return render_template('graph.html', ins=master_ins, errors=errors)

global flabels
flabels = ['', 'x', 'x,y', 'x,y,z', 'x,y,z,u', 'x,y,z,u,v'] 

global dispval
dispval = ''

global function_expression, function_output, func_content
func_content = ["", "", ""]
function_expression = ["", "", ""]
function_output = [None]*3

global editing
editing = 0

def edit_f1():
    global editing
    editing = 0

def edit_f2():
    global editing
    editing = 1

def edit_f3():
    global editing
    editing = 2

def add():
    global func_content
    func_content[editing]+='+'
    global function_expression
    function_expression[editing] +='+'

def sub():
    global func_content
    func_content[editing]+='-'
    global function_expression
    function_expression[editing] +='-'

def mul():
    global func_content
    func_content[editing]+='*'
    global function_expression
    function_expression[editing] +='*'

def div():
    global func_content
    func_content[editing]+='/'
    global function_expression
    function_expression[editing] +='/'

def zero():
    global func_content
    func_content[editing]+='0'
    global function_expression
    function_expression[editing] +='0'

def one():
    global func_content
    func_content[editing]+='1'
    global function_expression
    function_expression[editing] +='1'

def two():
    global func_content
    func_content[editing]+='2'
    global function_expression
    function_expression[editing] +='2'

def three():
    global func_content
    func_content[editing]+='3'
    global function_expression
    function_expression[editing] +='3'

def four():
    global func_content
    func_content[editing]+='4'
    global function_expression
    function_expression[editing] +='4'

def five():
    global func_content
    func_content[editing]+='5'
    global function_expression
    function_expression[editing] +='5'

def six():
    global func_content
    func_content[editing]+='6'
    global function_expression
    function_expression[editing] +='6'

def seven():
    global func_content
    func_content[editing]+='7'
    global function_expression
    function_expression[editing] +='7'

def eight():
    global func_content
    func_content[editing]+='8'
    global function_expression
    function_expression[editing] +='8'

def nine():
    global func_content
    func_content[editing]+='9'
    global function_expression
    function_expression[editing] +='9'

def dot():
    global func_content
    func_content[editing]+='.'
    global function_expression
    function_expression[editing] +='.'

def sin():
    global func_content
    func_content[editing]+='sin('
    global function_expression
    function_expression[editing] +='ADmath.sin('

def cos():
    global func_content
    func_content[editing]+='cos('
    global function_expression
    function_expression[editing] +='ADmath.cos('

def cos():
    global func_content
    func_content[editing]+='cos('
    global function_expression
    function_expression[editing] +='ADmath.cos('

def tan():
    global func_content
    func_content[editing]+='tan('
    global function_expression
    function_expression[editing] +='ADmath.tan('

def exp():
    global func_content
    func_content[editing]+='exp('
    global function_expression
    function_expression[editing] +='ADmath.exp('

def log():
    global func_content
    func_content[editing]+='log('
    global function_expression
    function_expression[editing] +='ADmath.log('

def pow_to():
    global func_content
    func_content[editing]+='pow('
    global function_expression
    function_expression[editing] +='**('

def sqrt():
    global func_content
    func_content[editing]+='sqrt('
    global function_expression
    function_expression[editing] +='ADmath.sqrt('

def left_par():
    global func_content
    func_content[editing]+='('
    global function_expression
    function_expression[editing] +='('

def right_par():
    global func_content
    func_content[editing]+=')'
    global function_expression
    function_expression[editing] +=')'
    
def xvar():
    global func_content
    func_content[editing]+='x'
    global function_expression
    function_expression[editing] +='x'

def yvar():
    global func_content
    func_content[editing]+='y'
    global function_expression
    function_expression[editing] +='y'

def zvar():
    global func_content
    func_content[editing]+='z'
    global function_expression
    function_expression[editing] +='z'

def uvar():
    global func_content
    func_content[editing]+='u'
    global function_expression
    function_expression[editing] +='u'

def vvar():
    global func_content
    func_content[editing]+='v'
    global function_expression
    function_expression[editing] +='v'

calcfuncs = {}
calcfuncs['+']=add
calcfuncs['-']=sub
calcfuncs['*']=mul
calcfuncs['/']=div
calcfuncs['0']=zero
calcfuncs['1']=one
calcfuncs['2']=two
calcfuncs['3']=three
calcfuncs['4']=four
calcfuncs['5']=five
calcfuncs['6']=six
calcfuncs['7']=seven
calcfuncs['8']=eight
calcfuncs['9']=nine
calcfuncs['sin']=sin
calcfuncs['cos']=cos
calcfuncs['tan']=tan
calcfuncs['exp']=exp
calcfuncs['log']=log
calcfuncs['pow']=pow_to
calcfuncs['sqrt']=sqrt
calcfuncs['(']=left_par
calcfuncs[')']=right_par
calcfuncs['.']=dot
calcfuncs['x']=xvar
calcfuncs['y']=yvar
calcfuncs['z']=zvar
calcfuncs['u']=uvar
calcfuncs['v']=vvar


calcfuncs['Edit f1'] = edit_f1
calcfuncs['Edit f2'] = edit_f2
calcfuncs['Edit f3'] = edit_f3
