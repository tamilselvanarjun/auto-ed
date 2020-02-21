from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

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
    return render_template('graph.html')

global flabels
flabels = ['', 'x', 'x,y', 'x,y,z', 'x,y,z,u', 'x,y,z,u,v'] 

global dispval
dispval = ''

global function_expression, function_output, func_content
func_content = ["a", "b", "c"]
function_expression = ["", "", ""]
function_output = [None]*3

global editing
editing = 0

def one():
    global func_content
    func_content[editing]+='1'
    #print(func_content)
    #calculate()
    #return 82#render_template('calculator.html', disp = dispval, calcfuncs=one)

calcfuncs = {}
calcfuncs['1']=one
