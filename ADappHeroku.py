from flask import Flask, render_template, redirect, url_for, request, Response, session, jsonify
from flask_session import Session

import io, sympy
from sympy import latex, sympify
import numpy as np
import pandas as pd
from matplotlib.backends.backend_svg import FigureCanvasSVG
from ADnum import ADnum
import ADmath
import ADgraph
from base64 import b64encode
from datetime import timedelta


#set up for flask app
app = Flask(__name__)
sess = Session()
app.secret_key = 'gaeirogrioghogjfi'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # Heroku dyno sleeps after 30 minutes of inactivity, and its ephemeral filesystem is discarded.
sess.init_app(app)


# python functions for jinja template
# https://stackoverflow.com/a/32034945/10012842
@app.context_processor
def my_utility_processor():
    def convert_latex(string):
        return latex(sympify(string, evaluate=False))

    def wrap_brackets(string):
        if string[-1] != ')':
            string = '(' + string + ')'
        return string

    def clean_latex(string):
        # convert sigmoid to lowercase sigma
        string = string.replace('sig', '\sigma')
        
        return string

    def to_matrix(string):
        string = string.replace(',\n', '<br>')
        return string

    return dict(convert_latex=convert_latex, wrap_brackets=wrap_brackets, clean_latex=clean_latex, to_matrix=to_matrix)







@app.route('/', methods = ["GET", "POST"])
def startup():
    
    errors = ''
    # if redirected from other pages due to expired session
    if session.get('refresh_message') != None:
        errors = session.get('refresh_message')
        session.pop('refresh_message')


    #global func_content
    #global function_expression
    #global function_output
    #global var_strs
    session['func_content'] = ["", "", ""]
    session['function_expression'] = ["", "", ""]
    session['function_output'] = [None]*3
    session['constant_fs'] = [0]*3
    session['var_strs'] = {}
    session['curr_idx'] = 0
    session['flabels'] = ['', 'x0', 'x0, x1', 'x0, x1, x2', 'x0, x1, x2, x3', 'x0, x1, x2, x3, x4']
    session['rev_dyn_set'] = []
    session['dispval']=''
    session['editing']=0
    session['var_strs'] = {}
    session['var_strs']["x"] = ""
    session['var_strs']["y"] = ""
    session['var_strs']["z"] = ""
    session['var_strs']["u"] = ""
    session['var_strs']["v"] = ""
    session['visfunc']=0
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
        #global master_ins
        session['master_ins'] = ins
        #global master_outs
        session['master_outs'] = outs
        return redirect(url_for('calculate'))
    return render_template('welcome.html', errors=errors)







@app.route('/calculate', methods = ["GET", "POST"])
def calculate():
    errors = ""

    # redirect to start page if session expired
    if 'master_ins' not in session:
        session['refresh_message'] = 'Your session has expired, please start again!'
        return redirect(url_for('startup'))


    if request.method == "POST": # when "Calculate" button pressed!
        try:
            if session['master_outs']>0: #for i in range(session['master_outs']):
                #global function_output
                #session['function_output'][i] = f #get_func(session['function_expression'], i)
                if session['master_ins'] == 1:
                    session['function_output'][0] = f0
                    session['function_output'][0](1)
                if session['master_ins'] == 2:
                    session['function_output'][0] = f1
                    session['function_output'][0](1, 1) 
                if session['master_ins'] ==3:
                    session['function_output'][0] = f2
                    session['function_output'][0](1, 1, 1)
                if session['master_ins']== 4:
                    session['function_output'][0] = f3
                    session['function_output'][0](1, 1, 1, 1)
                if session['master_ins'] == 5:
                    session['function_output'][0] = f4
                    session['function_output'][0](1, 1, 1, 1, 1)
            if session['master_outs']>1: #for i in range(session['master_outs']):
                #global function_output
                #session['function_output'][i] = f #get_func(session['function_expression'], i)
                if session['master_ins'] == 1:
                    session['function_output'][1] = g0
                    session['function_output'][1](1)
                if session['master_ins'] == 2:
                    session['function_output'][1] = g1
                    session['function_output'][1](1, 1) 
                if session['master_ins'] ==3:
                    session['function_output'][1] = g2
                    session['function_output'][1](1, 1, 1)
                if session['master_ins']== 4:
                    session['function_output'][1] = g3
                    session['function_output'][1](1, 1, 1, 1)
                if session['master_ins'] == 5:
                    session['function_output'][1] = g4
                    session['function_output'][1](1, 1, 1, 1, 1)
            if session['master_outs']>2: #for i in range(session['master_outs']):
                #global function_output
                #session['function_output'][i] = f #get_func(session['function_expression'], i)
                if session['master_ins'] == 1:
                    session['function_output'][2] = h0
                    session['function_output'][2](1)
                if session['master_ins'] == 2:
                    session['function_output'][2] = h1
                    session['function_output'][2](1, 1) 
                if session['master_ins'] ==3:
                    session['function_output'][2] = h2
                    session['function_output'][2](1, 1, 1)
                if session['master_ins']== 4:
                    session['function_output'][2] = h3
                    session['function_output'][2](1, 1, 1, 1)
                if session['master_ins'] == 5:
                    session['function_output'][2] = h4
                    session['function_output'][2](1, 1, 1, 1, 1)
        except:
            errors += "There is a syntax error in your function.  Please edit and try again."
            return render_template('calculator.html', func_content=session['func_content'], calcfuncs=calcfuncs, ins=session['master_ins'], outs=session['master_outs'], flabels = session['flabels'], errors = errors)
        return redirect(url_for('graphwindow'))

    return render_template('calculator.html', func_content = session['func_content'], calcfuncs=calcfuncs, ins=session['master_ins'], outs=session['master_outs'], flabels = session['flabels'], errors=errors)



@app.route('/clear-function-calculator', methods=["POST"])
def clear_function_calculator():

    clear_all()
    data = {'func_content': session['func_content'], 'editing': session['editing']}
    return jsonify(data)


@app.route('/press-calculator', methods = ["POST"])
def press_calculator():

    button_value = request.form.get("action")

    # if backspace
    if button_value  == u"\u2b05":
        back_space()

    else:
        calcfuncs[button_value]()
    data = {'button': button_value, 'func_content': session['func_content'], 'editing': session['editing']}
    return jsonify(data)










@app.route('/graphwindow', methods = ["GET", "POST"])
def graphwindow():
    #global show_table
    #global visfunc
    errors = ""

    # redirect to start page if session expired
    if ('master_ins' not in session):
        session['refresh_message'] = 'Your session has expired, please start again!'
        return redirect(url_for('startup'))

    # also redirect to start page if user erroneously moved back and forth on web ex. graph -> click previous arrow back to main -> attempt to click forward arrow back to graph
    if any(session['func_content']) == False: # if all function contents are empty
        session['refresh_message'] = 'Your session has expired, please start again!'
        return redirect(url_for('startup'))


    if request.method == "POST":
        
        action = request.form["action"]
        if request.form["action"] == "Set Input Values":
            session['show_table'] = False
            #global varlist
            session['varlist'] = []
            try:
                #global x
                session['x'] = [None]*session['master_outs']
                for i in range(session['master_outs']):
                    session['x'][i]  = ADnum(float(request.form["x"]), ins=session['master_ins'], ind=0)
                session['var_strs']['x']=request.form["x"]
                session['varlist'].append(session['x'])
                if session['master_ins']>1:
                    #global y
                    session['y'] = [None]*session['master_outs']
                    for i in range(session['master_outs']):
                        session['y'][i]=ADnum(float(request.form["y"]), ins=session['master_ins'], ind=1)
                    session['var_strs']['y']=request.form["y"]
                    session['varlist'].append(session['y'])
                if session['master_ins']>2:
                    #global z
                    session['z'] = [None]*session['master_outs']
                    for i in range(session['master_outs']):
                        session['z'][i]=ADnum(float(request.form["z"]), ins=session['master_ins'], ind=2)
                    session['var_strs']['z'] = request.form['z']
                    session['varlist'].append(session['z'])
                if session['master_ins']>3:
                    #global u
                    session['u'] = [None]*session['master_outs']
                    for i in range(session['master_outs']):
                        session['u'][i] = ADnum(float(request.form["u"]), ins=session['master_ins'], ind=3)
                    session['var_strs']['u'] = request.form["u"]
                    session['varlist'].append(session['u'])
                if session['master_ins']>4:
                    #global v
                    session['v'] = [None]*session['master_outs']
                    for i in range(session['master_outs']):
                        session['v'][i]=ADnum(float(request.form["v"]), ins=session['master_ins'], ind=4)
                    session['var_strs']['v']=request.form["v"]
                    session['varlist'].append(session['v'])
                build_function()    
                
                return render_template('graph2.html', ins=session['master_ins'], outs = session['master_outs'], errors=errors, var_strs=session['var_strs'], flabels=session['flabels'], func_content=session['func_content'], full=True, show_vis=True, val=session['disp_val'], der = session['disp_der'], show_table=False, func_select=False, constants=session['constant_fs'])
            except:
                errors += "Please enter numeric values for all of the inputs."
        
        # else:
        #     #global curr_idx
        #     # global rev_dyn_set

        #     if request.form["action"] == "prev":
        #         session['curr_idx'] = session['curr_idx']-1
        #     if request.form["action"] == "next":
        #         session['curr_idx'] = session['curr_idx']+1
        #     return render_template('graph2.html', visfunc=session['visfunc'], ins=session['master_ins'], outs=session['master_outs'], errors=errors, var_strs=session['var_strs'], flabels=session['flabels'], func_content=session['func_content'], full=True, val=session['disp_val'], der=session['disp_der'], func_select=True, table=table)

    
    return render_template('graph2.html', ins=session['master_ins'], outs=session['master_outs'], errors=errors, var_strs=session['var_strs'], flabels = session['flabels'], func_content=session['func_content'], full=False, show_vis = False, show_table=False, func_select=False, constants=session['constant_fs'])



@app.route('/select-func-viz', methods = ["POST"])
def select_func_viz():
    
    # get selected function information
    selected_function = request.form.get("action")

    if selected_function == "f1":
        session['visfunc'] = 0
    elif selected_function == "f2":
        session['visfunc'] = 1
    elif selected_function == "f3":
        session['visfunc']  = 2

    #Attempts that did not work to pass to visualization portion
    #if session['constant_fs'][session['visfunc']]:
        #data = {'show_vis' : False}
        #return jsonify(data)
        #show_vis = False
        #return redirect(url_for('graphwindow'))
        #session['refresh_message'] = 'TEST'
        #errors = 'The function you are trying to visualize is a constant, so visualizing with a graph and table is not needed for computing the derivative.'
        #data = {'show_vis' : False, 'errors' : errors}
        #return jsonify(data)
        #return render_template('graph2.html', ins=session['master_ins'], outs=session['master_outs'], errors=errors, var_strs=session['var_strs'], flabels=session['flabels'], func_content=session['func_content'], full= True, show_vis = False, val=session['disp_val'], der = session['disp_der'], show_table=False, func_select=False, constants=session['constant_fs'])
    
    # set initial vars
    session['curr_idx'] = 0
    session['rev_dyn_set'] = []
    
    # generate evaluation table
    table = get_table()


    # get appropriate graphs. Initial dynamic reverse graph is same as reverse graph
    comp_graph_raw = ADgraph.draw_graph2(session['out_num'][session['visfunc']], session['G'][session['visfunc']], session['edge_labs'][session['visfunc']], session['pos'][session['visfunc']], session['labs'][session['visfunc']])
    comp_graph = b64encode(comp_graph_raw.getvalue()).decode('ascii')

    rev_graph_raw = ADgraph.draw_graph_rev2(session['out_num'][session['visfunc']], session['G'][session['visfunc']], session['edge_labs'][session['visfunc']], session['pos'][session['visfunc']], session['labs'][session['visfunc']])
    rev_graph = b64encode(rev_graph_raw.getvalue()).decode('ascii')

   
    data = {'visfunc': session['visfunc'], 'ins': session['master_ins'], 'table': table, 'comp_graph': comp_graph, 'rev_graph': rev_graph, 'rev_dynamic_graph': rev_graph, 'show_vis' : True}
    return jsonify(data)


@app.route('/partial-der', methods = ["POST"])
def partial_der():

    no_steps = False
     # get selected partial derivative option
    action = request.form.get("action")

    session['curr_idx'] = 0
    i = int(action[-2])
    var = session['varlist'][int(action[-1])]
    session['rev_dyn_set'] = ADgraph.get_rev_dynamic_outs(session['out_num'][i], var[i].revder(session['out_num'][i])[1], session['G'][i], session['edge_labs'][i], session['pos'][i], session['labs'][i], var[i].revder(session['out_num'][i])[0])


    if session['curr_idx'] == len(session['rev_dyn_set'])-1: # if no steps available
        no_steps = True


    print(session['var_strs'])
    print(session['func_content'])
    print(session['varlist'])
    print(session['rev_dyn_set']) #[]
    print(session['curr_idx'])

     # get initial dynamic reverse calculation graph

    rev_dynamic_raw = session['rev_dyn_set'][session['curr_idx']] #ADgraph.draw_graph_rev2(out_num[visfunc], G[visfunc], edge_labs[visfunc], pos[visfunc], labs[visfunc])
    rev_dynamic_graph = b64encode(rev_dynamic_raw.getvalue()).decode('ascii')


    data = {'partial_der': action, 'no_steps': no_steps, 'curr_idx': session['curr_idx'], 'rev_dynamic_graph': rev_dynamic_graph}
    return jsonify(data)



@app.route('/navigate-steps', methods = ["POST"])
def navigate_steps():
    
    reached_max = False
    
    action = request.form.get("action")
    if action == "prev":
        session['curr_idx'] = session['curr_idx']-1
    if action == "next":
        session['curr_idx'] = session['curr_idx']+1

    # check if current idx position has reached the max idx
    if session['curr_idx'] == len(session['rev_dyn_set'])-1:
        reached_max = True

    # fix idx going beyond limits
    # if session['curr_idx'] < 0:
    #     session['curr_idx'] = 0
    # if session['curr_idx'] > len(session['rev_dyn_set'])-1:
    #     session['curr_idx'] = len(session['rev_dyn_set'])-1
    
    # get appropriate dynamic rev graph
    rev_dynamic_raw = session['rev_dyn_set'][session['curr_idx']]
    rev_dynamic_graph = b64encode(rev_dynamic_raw.getvalue()).decode('ascii')

    data = {'step': action, 'reached_max': reached_max, 'curr_idx': session['curr_idx'], 'rev_dynamic_graph': rev_dynamic_graph}
    return jsonify(data)




def f0(x):
    return eval(session['function_expression'][0])

def f1(x,y):
    return eval(session['function_expression'][0])

def f2(x, y, z):
    return eval(session['function_expression'][0])

def f3(x, y, z, u):
    return eval(session['function_expression'][0])

def f4(x, y, z, u, v):
    return eval(session['function_expression'][0])

def g0(x):
    return eval(session['function_expression'][1])

def g1(x,y):
    return eval(session['function_expression'][1])

def g2(x, y, z):
    return eval(session['function_expression'][1])

def g3(x, y, z, u):
    return eval(session['function_expression'][1])

def g4(x, y, z, u, v):
    return eval(session['function_expression'][1])

def h0(x):
    return eval(session['function_expression'][2])

def h1(x,y):
    return eval(session['function_expression'][2])

def h2(x, y, z):
    return eval(session['function_expression'][2])

def h3(x, y, z, u):
    return eval(session['function_expression'][2])

def h4(x, y, z, u, v):
    return eval(session['function_expression'][2])

def build_function():
    #global out_num
    session['out_num'] = [None]*session['master_outs']
    #session['constant_fs'] = [0]*session['master_outs']
    for i in range(session['master_outs']):
        if session['master_ins'] == 1:
            session['out_num'][i] = session['function_output'][i](session['x'][i])
        if session['master_ins'] == 2:
            session['out_num'][i] = session['function_output'][i](session['x'][i], session['y'][i])
        if session['master_ins'] == 3:
            session['out_num'][i] = session['function_output'][i](session['x'][i], session['y'][i], session['z'][i])
        if session['master_ins'] == 4:
            session['out_num'][i] = session['function_output'][i](session['x'][i], session['y'][i], session['z'][i], session['u'][i])
        if session['master_ins'] == 5:
            session['out_num'][i] = session['function_output'][i](session['x'][i], session['y'][i], session['z'][i], session['u'][i], session['v'][i])
    #global disp_val, disp_der
    session['disp_val'] = '['
    session['disp_der'] = '['
    for i, out in enumerate(session['out_num']):
        #disp_val = str(np.round(out.val, 2))
        #disp_der = str(np.round(out.der, 2))
        try:
            session['disp_val'] += str(np.round(out.val, 2))
            session['disp_der'] += str(np.round(out.der, 2))
        except:
            session['disp_val'] += str(np.round(out, 2))
            session['disp_der'] += str([0]*session['master_ins'])
            session['constant_fs'][i] = 1
        session['disp_val'] += ',\n'
        session['disp_der'] +=',\n'
    session['disp_val'] = session['disp_val'][:-2]+']'
    session['disp_der'] = session['disp_der'][:-2]+']'
    #global G, edge_labs, pos, labs
    session['G'] = [None]*session['master_outs']
    session['edge_labs'] = [None]*session['master_outs']
    session['pos'] = [None]*session['master_outs']
    session['labs'] = [None]*session['master_outs']
    for i, out in enumerate(session['out_num']):
        try:
            session['G'][i], session['edge_labs'][i], session['pos'][i], session['labs'][i] = ADgraph.get_graph_setup(out)
        except:
            pass



def get_table():
    df = ADgraph.gen_table(session['out_num'][session['visfunc']])
    return df.to_html(index=False)


def comp_graph(i):
    ADgraph.draw_graph2(session['out_num'][i], session['G'][i], session['edge_labs'][i], session['pos'][i], session['labs'][i]) 

def rev_graph(i):
    ADgraph.draw_graph_rev2(session['out_num'][i], session['G'][i], session['edge_labs'][i], session['pos'][i], session['labs'][i])

def rev_dynamic(i, var):
    ADgraph.draw_graph_rev_dynamic(session['out_num'][i], var[i].revder(session['out_num'][i])[1], session['G'][i], session['edge_labs'][i], session['pos'][i], session['labs'][i], var[i].revder(session['out_num'][i])[0])

def edit_f1():
    #global editing
    session['editing'] = 0

def edit_f2():
    #global editing
    session['editing'] = 1

def edit_f3():
    #global editing
    session['editing'] = 2

def clear_all():
    session['func_content'][session['editing']] = ""
    session['function_expression'][session['editing']] = ""

def back_space():
    session['function_expression'][session['editing']] = backstep(session['function_expression'][session['editing']])
    back_func()

def backstep(text):
    if len(text) == 0 or len(text)== 1:
        return ""
    if text[-1]=='(' and text[-2] in ['n', 't', 'p', 's', 'g', '*', 'h', 'u']:
        if text[-2] == 't':
            return text[:-12]
        elif text[-2]=='h' or text[-2]=='u':
            return text[:-12]
        elif (text[-2] == '*' and text[-3]=='*'):
            return text[:-3]
        else:
            return text[:-11]
    else:
        return text[:-1]

def back_func():
    content = session['func_content'][session['editing']]
    if len(content)==0 or len(content)==1:
        content=''
    elif content[-2] == 'x':
        content = content[:-2]
    elif content[-1]=='(' and content[-2] in ['t', 'n', 'w', 's', 'p', 'g', '^', 'h', 'u']:
        if content[-2] == 't':
            content = content[:-5]
        elif content[-2] == 'h' or content[-2]=='u':
            content = content[:-5]
        elif content[-2] == 'w' and content[-3] != 'o':
            content = content[:-1]
        elif content[-2]=='^':
            content = content[:-2]
        else:
            content = content[:-4]
    else:
        content = content[:-1]
    session['func_content'][session['editing']] = content

def get_func(function_expression, i):
    if session['master_ins'] == 1:
        def f(x):
            return eval(function_expression[i])
    if session['master_ins'] == 2:
        def f(x,y):
            return eval(function_expression[i])
    if session['master_ins'] == 3:
        def f(x, y, z):
            return eval(function_expression[i])
    if session['master_ins'] == 4:
        def f(x, y, z, u):
            return eval(function_expression[i])
    if session['master_ins'] == 5:
        def f(x, y, z, u, v):
            return eval(function_expression[i])
    return f


def check(x):
    return x


def add():
    #global func_content
    session['func_content'][session['editing']]+='+'
    #global function_expression
    session['function_expression'][session['editing']] +='+'

def sub():
    #global func_content
    session['func_content'][session['editing']]+='-'
    #global function_expression
    session['function_expression'][session['editing']] +='-'

def mul():
    #global func_content
    session['func_content'][session['editing']]+='*'
    #global function_expression
    session['function_expression'][session['editing']] +='*'

def div():
    #global func_content
    session['func_content'][session['editing']]+='/'
    #global function_expression
    session['function_expression'][session['editing']] +='/'

def zero():
    #global func_content
    session['func_content'][session['editing']]+='0'
    #global function_expression
    session['function_expression'][session['editing']] +='0'

def one():
    #global func_content
    session['func_content'][session['editing']]+='1'
    #global function_expression
    session['function_expression'][session['editing']] +='1'

def two():
    #global func_content
    session['func_content'][session['editing']]+='2'
    #global function_expression
    session['function_expression'][session['editing']] +='2'

def three():
    #global func_content
    session['func_content'][session['editing']]+='3'
    #global function_expression
    session['function_expression'][session['editing']] +='3'

def four():
    #global func_content
    session['func_content'][session['editing']]+='4'
    #global function_expression
    session['function_expression'][session['editing']] +='4'

def five():
    #global func_content
    session['func_content'][session['editing']]+='5'
    #global function_expression
    session['function_expression'][session['editing']] +='5'

def six():
    #global func_content
    session['func_content'][session['editing']]+='6'
    #global function_expression
    session['function_expression'][session['editing']] +='6'

def seven():
    #global func_content
    session['func_content'][session['editing']]+='7'
    #global function_expression
    session['function_expression'][session['editing']] +='7'

def eight():
    #global func_content
    session['func_content'][session['editing']]+='8'
    #global function_expression
    session['function_expression'][session['editing']] +='8'

def nine():
    #global func_content
    session['func_content'][session['editing']]+='9'
    #global function_expression
    session['function_expression'][session['editing']] +='9'

def dot():
    #global func_content
    session['func_content'][session['editing']]+='.'
    #global function_expression
    session['function_expression'][session['editing']] +='.'

def sin():
    #global func_content
    session['func_content'][session['editing']]+='sin('
    #global function_expression
    session['function_expression'][session['editing']] +='ADmath.sin('

def cos():
    #global func_content
    session['func_content'][session['editing']]+='cos('
    #global function_expression
    session['function_expression'][session['editing']] +='ADmath.cos('


def tan():
    #global func_content
    session['func_content'][session['editing']]+='tan('
    #global function_expression
    session['function_expression'][session['editing']] +='ADmath.tan('

def sinh():
    #global func_content
    session['func_content'][session['editing']]+='sinh('
    #global function_expression
    session['function_expression'][session['editing']] +='ADmath.sinh('

def cosh():
    #global func_content
    session['func_content'][session['editing']]+='cosh('
    #global function_expression
    session['function_expression'][session['editing']] +='ADmath.cosh('


def tanh():
    #global func_content
    session['func_content'][session['editing']]+='tanh('
    #global function_expression
    session['function_expression'][session['editing']] +='ADmath.tanh('

def sig():
    #global func_content
    session['func_content'][session['editing']]+='sig('
    #global function_expression
    session['function_expression'][session['editing']]+= 'ADmath.sig('

def relu():
    #global func_content
    session['func_content'][session['editing']] += 'relu('
    #global function_expression
    session['function_expression'][session['editing']] += 'ADmath.relu('

def exp():
    #global func_content
    session['func_content'][session['editing']]+='exp('
    #global function_expression
    session['function_expression'][session['editing']] +='ADmath.exp('

def log():
    #global func_content
    session['func_content'][session['editing']]+='log('
    #global function_expression
    session['function_expression'][session['editing']] +='ADmath.log('

def pow_to():
    #global func_content
    session['func_content'][session['editing']]+='^('
    #global function_expression
    session['function_expression'][session['editing']] +='**('

def sqrt():
    #global func_content
    session['func_content'][session['editing']]+='sqrt('
    #global function_expression
    session['function_expression'][session['editing']] +='ADmath.sqrt('

def left_par():
    #global func_content
    session['func_content'][session['editing']]+='('
    #global function_expression
    session['function_expression'][session['editing']] +='('

def right_par():
    #global func_content
    session['func_content'][session['editing']]+=')'
    #global function_expression
    session['function_expression'][session['editing']] +=')'
    
def xvar():
    #global func_content
    session['func_content'][session['editing']]+='x0'
    #global function_expression
    session['function_expression'][session['editing']] +='x'

def yvar():
    #global func_content
    session['func_content'][session['editing']]+='x1'
    #global function_expression
    session['function_expression'][session['editing']] +='y'

def zvar():
    #global func_content
    session['func_content'][session['editing']]+='x2'
    #global function_expression
    session['function_expression'][session['editing']] +='z'

def uvar():
    #global func_content
    session['func_content'][session['editing']]+='x3'
    #global function_expression
    session['function_expression'][session['editing']] +='u'

def vvar():
    #global func_content
    session['func_content'][session['editing']]+='x4'
    #global function_expression
    session['function_expression'][session['editing']] +='v'

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
calcfuncs['x0']=xvar
calcfuncs['x1']=yvar
calcfuncs['x2']=zvar
calcfuncs['x3']=uvar
calcfuncs['x4']=vvar
calcfuncs['sinh'] = sinh
calcfuncs['cosh']=cosh
calcfuncs['tanh']=tanh
calcfuncs['sig'] = sig
calcfuncs['relu'] = relu

calcfuncs['Edit f1'] = edit_f1
calcfuncs['Edit f2'] = edit_f2
calcfuncs['Edit f3'] = edit_f3

if __name__ == '__main__':
    # Discussion about threads in Flask and such
    # https://stackoverflow.com/questions/38876721/handle-flask-requests-concurrently-with-threaded-true/38876915#38876915
    # https://github.com/skvark/opencv-python/issues/134

    app.run(host="0.0.0.0", port=5000, threaded=False) # https://github.com/pyeve/eve/issues/873
