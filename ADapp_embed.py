from flask import Flask, render_template, redirect, url_for, request, Response
app = Flask(__name__)

import io
import numpy as np
import pandas as pd
from matplotlib.backends.backend_svg import FigureCanvasSVG
from ADnum_rev_timed_vis import ADnum
import ADmath_rev as ADmath
import ADgraph_GUI3 as ADgraph

@app.route('/', methods = ["GET", "POST"])
def startup():
    errors = ""
    global func_content
    global function_expression
    global function_output
    func_content = ["", "", ""]
    function_expression = ["", "", ""]
    function_output = [None]*3
    if request.method == "POST":
        try:
            ins = int(request.form["inputs"])
            assert ins>0
        except:
            errors += "Please enter a positive integer number of inputs."
            return render_template('welcome.html', errors=errors)
        
        try:
            outs = int(request.form["outputs"])
            assert outs>0
        except:
            errors += "Please enter a positive integer number of outputs."
            return render_template('welcome.html', errors=errors)
        if ins>5:
            errors += "More than 5 inputs is not supported in the web app environment.  Please either use the AD?? package or experiment with a fewer number of variables."
            return render_template('welcome.html', errors=errors)
        if outs>3:
            errors += "More than 3 outputs is not supported in the web app environmnent.  Please either use the AD?? package or experiment with a fewer number of functions."
            return render_template('welcome.html', errors=errors)
        global master_ins
        master_ins = ins
        global master_outs
        master_outs = outs
        return redirect(url_for('calculate'))
    return render_template('welcome.html', errors=errors)

@app.route('/calculate', methods = ["GET", "POST"])
def calculate():
    errors = ""
    if request.method == "POST":
        if request.form["action"] == "Clear All":
            clear_all()
        elif request.form["action"] == u"\u2b05":
            back_space()
        elif request.form["action"] == "Calculate":
            try:
                for i in range(master_outs):
                    global function_output
                    function_output[i] = get_func(function_expression, i)
                    if master_ins == 1:
                        function_output[i](1)
                    if master_ins == 2:
                        function_output[i](1, 1)
                    if master_ins ==3:
                        function_output[i](1, 1, 1)
                    if master_ins == 4:
                        function_output[i](1, 1, 1, 1)
                    if master_ins == 5:
                        function_output[i](1, 1, 1, 1, 1)
            except:
                errors += "There is a syntax error in your function.  Please edit and try again."
                return render_template('calculator.html', func_content=func_content, calcfuncs=calcfuncs, ins=master_ins, outs=master_outs, flabels = flabels, errors = errors)
            return redirect(url_for('graphwindow'))
        else:
            calcfuncs[request.form["action"]]()
    return render_template('calculator.html', func_content = func_content, calcfuncs=calcfuncs, ins=master_ins, outs=master_outs, flabels = flabels, errors=errors)

@app.route('/graphwindow', methods = ["GET", "POST"])
def graphwindow():
    global show_table
    global visfunc
    errors = ""
    if request.method == "POST":
        action = request.form["action"]
        if request.form["action"] == "Set Input Values":
            show_table = False
            global varlist
            varlist = []
            try:
                global x
                x = [None]*master_outs
                for i in range(master_outs):
                    x[i]  = ADnum(float(request.form["x"]), ins=master_ins, ind=0)
                var_strs['x']=request.form["x"]
                varlist.append(x)
                if master_ins>1:
                    global y
                    y = [None]*master_outs
                    for i in range(master_outs):
                        y[i]=ADnum(float(request.form["y"]), ins=master_ins, ind=1)
                    var_strs['y']=request.form["y"]
                    varlist.append(y)
                if master_ins>2:
                    global z
                    z = [None]*master_outs
                    for i in range(master_outs):
                        z[i]=ADnum(float(request.form["z"]), ins=master_ins, ind=2)
                    var_strs['z'] = request.form['z']
                    varlist.append(z)
                if master_ins>3:
                    global u
                    u = [None]*master_outs
                    for i in range(master_outs):
                        u[i] = ADnum(float(request.form["u"]), ins=master_ins, ind=3)
                    var_strs['u'] = request.form["u"]
                    varlist.append(u)
                if master_ins>4:
                    global v
                    v = [None]*master_outs
                    for i in range(master_outs):
                        v[i]=ADnum(float(request.form["v"]), ins=master_ins, ind=4)
                    var_strs['v']=request.form["v"]
                    varlist.append(v)
                build_function()    
                return render_template('graph2.html', ins=master_ins, outs = master_outs, errors=errors, var_strs=var_strs, flabels=flabels, func_content=func_content, full=True, val=disp_val, der = disp_der, show_table=False, func_select=False)
            except:
                errors += "Please enter numeric values for all of the inputs."
        
        else:
            global curr_idx
            global rev_dyn_set
            if request.form["action"] == "f1":
                visfunc = 0
                curr_idx = 0
                rev_dyn_set = []
            if request.form["action"] == "f2":
                visfunc = 1
                curr_idx = 0
                rev_dyn_set = []
            if request.form["action"] == "f3":
                visfunc  = 2
                curr_idx = 0
                rev_dyn_set = []
            table = get_table()
            if request.form["action"][0] == 'd':
                curr_idx = 0
                action = request.form["action"]
                i = int(action[-2])
                var = varlist[int(action[-1])]
                rev_dyn_set = ADgraph.get_rev_dynamic_outs(out_num[i], var[i].revder(out_num[i])[1], G[i], edge_labs[i], pos[i], labs[i], var[i].revder(out_num[i])[0])
            if request.form["action"] == "prev":
                curr_idx = curr_idx-1
            if request.form["action"] == "next":
                curr_idx = curr_idx+1
            return render_template('graph2.html', visfunc=visfunc, ins=master_ins, outs=master_outs, errors=errors, var_strs=var_strs, flabels=flabels, func_content=func_content, full=True, val=disp_val, der=disp_der, func_select=True, table=table)
        #if action[0]=="g":
        #if request.form["action"]=="Computational Graph":
         #   comp_graph(int(action[-1]))
          #  if show_table:
           #     df = ADgraph.gen_table(out_num[int(action[-1])])
            #    table = df.to_html(index=False)
            #ADgraph.draw_graph2(out_num[0], G[0], edge_labs[0], pos[0], labs[0])
            #else:
             #   table = 0
            #return render_template('graph.html', ins=master_ins, outs=master_outs, errors=errors, var_strs=var_strs, flabels=flabels, func_content=func_content, full=True, val=disp_val, der=disp_der, show_table=show_table, tables=table)
            #comp_graph(int(action[-1]))
        #if action[0]=="t":
         #   df = ADgraph.gen_table(out_num[int(action[-1])])
          #  table = df.to_html(index=False)
           # show_table = True
            #return render_template('graph.html', ins=master_ins, outs=master_outs, errors=errors, var_strs=var_strs, flabels=flabels, func_content=func_content, full=True, val=disp_val, der=disp_der, show_table = show_table, tables=table)
        #if action[0]=='r':
        #if request.form["action"]=="Reverse Graph":
         #   rev_graph(int(action[-1]))
            #ADgraph.draw_graph_rev2(out_num[0], G[0], edge_labs[0], pos[0], labs[0])
          #  return render_template('graph.html', ins=master_ins, outs=master_outs, errors=errors, var_strs=var_strs, flabels=flabels, func_content=func_content, full=True, val=disp_val, der=disp_der, show_table=show_table)
        #if action[0]=='d':
        #if request.form["action"]=="Rev Dynamic":
         #   rev_dynamic(int(action[-2]), varlist[int(action[-1])])
            #ADgraph.draw_graph_rev_dynamic(out_num[0], x[0].revder(out_num[0])[1], G[0], edge_labs[0], pos[0], labs[0], x[0].revder(out_num[0])[0])
            #return render_template('graph.html', ins=master_ins, outs=master_outs, errors=errors, var_strs=var_strs, flabels=flabels, func_content=func_content, full=True, val=disp_val, der=disp_der, show_table=show_table)
    return render_template('graph2.html', ins=master_ins, outs=master_outs, errors=errors, var_strs=var_strs, flabels = flabels, func_content=func_content, full=False, show_table=False, func_select=False)


global curr_idx
curr_idx = 0

global rev_dyn_set
rev_dyn_set = []


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

global var_strs
var_strs = {}
var_strs["x"] = ""
var_strs["y"] = ""
var_strs["z"] = ""
var_strs["u"] = ""
var_strs["v"] = ""

def build_function():
    global out_num
    out_num = [None]*master_outs
    for i in range(master_outs):
        if master_ins == 1:
            out_num[i] = function_output[i](x[i])
        if master_ins == 2:
            out_num[i] = function_output[i](x[i], y[i])
        if master_ins == 3:
            out_num[i] = function_output[i](x[i], y[i], z[i])
        if master_ins == 4:
            out_num[i] = function_output[i](x[i], y[i], z[i], u[i])
        if master_ins == 5:
            out_num[i] = function_output[i](x[i], y[i], z[i], u[i], v[i])
    global disp_val, disp_der
    disp_val = '['
    disp_der = '['
    for out in out_num:
        #disp_val = str(np.round(out.val, 2))
        #disp_der = str(np.round(out.der, 2))
        try:
            disp_val += str(np.round(out.val, 2))
            disp_der += str(np.round(out.der, 2))
        except:
            disp_val += str(np.round(out, 2))
            disp_der ++ str([0]*master_ins)
        disp_val += ',\n'
        disp_der +=',\n'
    disp_val = disp_val[:-2]+']'
    disp_der = disp_der[:-2]+']'
    global G, edge_labs, pos, labs
    G = [None]*master_outs
    edge_labs = [None]*master_outs
    pos = [None]*master_outs
    labs = [None]*master_outs
    for i, out in enumerate(out_num):
        try:
            G[i], edge_labs[i], pos[i], labs[i] = ADgraph.get_graph_setup(out)
        except AttributeError:
            pass

global visfunc
visfunc = 0

@app.route('/comp_graph')
def comp_graph_embed():
    output = ADgraph.draw_graph2(out_num[visfunc], G[visfunc], edge_labs[visfunc], pos[visfunc], labs[visfunc])
    print('entered function')
    #output = io.BytesIO()
    #FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype='image/svg+xml')

@app.route('/rev_graph')
def rev_graph_embed():
    output = ADgraph.draw_graph_rev2(out_num[visfunc], G[visfunc], edge_labs[visfunc], pos[visfunc], labs[visfunc])
    return Response(output.getvalue(), mimetype='image/svg+xml')

@app.route('/rev_dynamic')
def rev_dynamic():
    global curr_idx
    if len(rev_dyn_set) == 0:
        out = ADgraph.draw_graph_rev2(out_num[visfunc], G[visfunc], edge_labs[visfunc], pos[visfunc], labs[visfunc])
        return Response(out.getvalue(), mimetype = 'image/svg+xml')
    if curr_idx < 0:
        #global curr_idx
        curr_idx = 0
    if curr_idx > len(rev_dyn_set)-1:
        #global curr_idx
        curr_idx = len(rev_dyn_set)-1
    output = rev_dyn_set[curr_idx] #ADgraph.draw_graph_rev2(out_num[visfunc], G[visfunc], edge_labs[visfunc], pos[visfunc], labs[visfunc])
    return Response(output.getvalue(), mimetype='image/svg+xml')


def get_table():
    df = ADgraph.gen_table(out_num[visfunc])
    return df.to_html(index=False)

def comp_graph(i):
    ADgraph.draw_graph2(out_num[i], G[i], edge_labs[i], pos[i], labs[i]) 

def rev_graph(i):
    ADgraph.draw_graph_rev2(out_num[i], G[i], edge_labs[i], pos[i], labs[i])

def rev_dynamic(i, var):
    ADgraph.draw_graph_rev_dynamic(out_num[i], var[i].revder(out_num[i])[1], G[i], edge_labs[i], pos[i], labs[i], var[i].revder(out_num[i])[0])

def edit_f1():
    global editing
    editing = 0

def edit_f2():
    global editing
    editing = 1

def edit_f3():
    global editing
    editing = 2

def clear_all():
    func_content[editing] = ""
    function_expression[editing] = ""

def back_space():
    function_expression[editing] = backstep(function_expression[editing])
    back_func()

def backstep(text):
    if len(text) == 0:
        return ""
    if text[-1]=='(' and text[-2] in ['n', 't', 'p', 's', 'g', '*']:
        if text[-2] == 't':
            return text[:-12]
        elif (text[-2] == '*' and text[-2]=='*'):
            return text[:-3]
        else:
            return text[:-12]
    else:
        return text[:-1]

def back_func():
    content = func_content[editing]
    if len(content)==0:
        content=content
    elif content[-1]=='(' and content[-2] in ['t', 'n', 'w', 's', 'p', 'g', '^']:
        if content[-2] == 't':
            content = content[:-5]
        elif content[-2] == 'w' and content[-3] != 'o':
            content = content[:-1]
        elif content[-2]=='^':
            content = content[:-2]
        else:
            content = content[:-4]
    else:
        content = content[:-1]
    func_content[editing] = content

def get_func(function_expression, i):
    if master_ins == 1:
        def f(x):
            return eval(function_expression[i])
    if master_ins == 2:
        def f(x,y):
            return eval(function_expression[i])
    if master_ins == 3:
        def f(x, y, z):
            return eval(function_expression[i])
    if master_ins == 4:
        def f(x, y, z, u):
            return eval(function_expression[i])
    if master_ins == 5:
        def f(x, y, z, u, v):
            return eval(function_expression[i])
    return f



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
    func_content[editing]+='^('
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
calcfuncs['^']=pow_to
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

if __name__ == '__main__':
    # Discussion about threads in Flask and such
    # https://stackoverflow.com/questions/38876721/handle-flask-requests-concurrently-with-threaded-true/38876915#38876915
    # https://github.com/skvark/opencv-python/issues/134

    app.run(host="0.0.0.0", port=5000, threaded=False) # https://github.com/pyeve/eve/issues/873
