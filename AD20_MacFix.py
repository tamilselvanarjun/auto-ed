import numpy as np
#import AD20
#from AD20.ADnum import ADnum
#from AD20 import ADmath as ADmath
from ADnum_rev_timed_vis import ADnum
import ADmath_rev as ADmath
import ADgraph_GUI as ADgraph


import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandastable import Table


if __name__ == '__main__':
    preset = tk.Tk()
    preset.title('Number of inputs.')
    preset.geometry("300x200")
    num_ins = tk.IntVar()
    tk.Label(preset, text = "Number of function inputs:", height = 3, width = 30).grid(row = 0, column=0)
    tk.Entry(preset, textvariable = num_ins, width = 30).grid(row=1, column =0)
    def close_window():
        if type(num_ins.get())!= int:
            messagebox.showinfo('Error', 'Please enter a positive integer number of inputs.')
        elif num_ins.get()>5:
            messagebox.showinfo('Error', 'More than 5 inputs is not supported in the GUI environment.  Please either use the AD20 package, or experiment with a function of fewer variables.')
        elif num_ins.get()>0:
            preset.destroy()
        else:
            messagebox.showinfo('Error', 'Please enter a positive integer number of inputs.')
    ttk.Button(preset, text = 'Next', width = 30, command = close_window).grid(row = 2, column = 0)
   # def fix():
    #    a = preset.winfo_geometry().split('+')[0]
     #   b = a.split('x')
      #  w = int(b[0])
       # h = int(b[1])
        #preset.geometry('%dx%d' % (w+1, h+1))
    #preset.update()
    #preset.after(0, fix)
    
    preset.mainloop()
    global master_ins
    master_ins = num_ins.get()

    preset2 = tk.Tk()
    preset2.title('Number of outputs.')
    preset2.geometry("300x200")
    num_outs = tk.IntVar()
    tk.Label(preset2, text = "Number of output functions:", height = 3, width = 30).grid(row = 0, column=0)
    tk.Entry(preset2, textvariable = num_outs, width = 30).grid(row=1, column =0)
    def close_window():
        if type(num_outs.get())!= int:
            messagebox.showinfo('Error', 'Please enter a positive integer number of inputs.')
        elif num_outs.get()>3:
            messagebox.showinfo('Error', 'More than 3 functions is not supported in the GUI environment.  Please either use the AD20 package, or experiment with fewer outputs.')
        elif num_outs.get()>0:
            preset2.destroy()
        else:
            messagebox.showinfo('Error', 'Please enter a positive integer number of inputs.')
    ttk.Button(preset2, text = 'Next', width = 30, command = close_window).grid(row = 2, column = 0)
    preset2.mainloop()
    global master_outs
    master_outs = num_outs.get()
    
    master = tk.Tk()
    master.title("AutoDiff Calculator")
    #master.attributes("-fullscreen", True)
    master.state('zoomed')
    #master.bind('<Escape>', end_fullscreen(master))

    def instruction():
        text = "This calculator generates functions of multiple variables.  Use the buttons below to define your function(s)." +\
                "The magenta buttons in the last row are the input variables.  Use standard calculator syntax to define your function." +\
                "When you are done defining your function, press \'Calculate\' to get the result.  Press \'Clear Function\' to start over for a particular function."
        #text = "This calculator performs basic calculations and generates functions of a single variable. \n \n" +\
        #"Use the buttons below to define your function.  The magenta X is the input variable. \n \n" +\
        #"All of the special functions should use standard calculator syntax.  For example, to define the sine of X:" +\
        #"press \'sin\', press \'(\', and then press \')\'.  To define x squared:" +\
        #"press \'X\', press \'pow\', press \'(\', press '2', and press press \')\'. \n \n" +\
        #"When you are done defining your function, press \'Calculate\' to get the result.  Press \'Clear All\' to start over."
        messagebox.showinfo("Welcome to AutoDiff Education Mode",text)

    def versionInfo():
        messagebox.showinfo("Welcome to AutoDiff Education Mode","AD20 version 1.0")
    ##master button
    button_instruction = tk.Button(master, text = "Instructions",fg = "Orange",command = instruction)
    button_instruction.place(relx=0, rely= 0,anchor=tk.NW)

    #button_version = tk.Button(master, text = "Check Version", command = versionInfo)
    #button_version.pack(side = 'top')

    #===End of master configuration


    #===Tool box for global variables
    global function_expression, function_output, func_content
    function_expression = ["", "", ""]
    function_output = [None]*3
    function_output[0] = lambda x: 0
    function_output[1] = lambda x: 0
    function_output[2] = lambda x: 0
    func_content = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
    
    function_expression2 = ""
    function_output2 = lambda x: 0
    func_content2 = tk.StringVar()
    
    function_expression3 = ""
    function_output3 = lambda x: 0
    func_content3 = tk.StringVar()
    #====End of global variables set===

    #===Block for Graph top level window===

    def graph_master():
       # print(function_output)
       # print(function_expression)
       # for i in range(master_outs):
       #     print(function_output[i](1))
       #     f = lambda x: eval(function_expression[i])
       #     print(f(5))
        #if local_func:
         #   for i in range(master_outs):
          #      print(local_func[i](1))

        def show_plot():
            plot_window = tk.Toplevel(graph_window)
            plot_window.title("Function and derivative plot")
            #plot_window.geometry("600x600")
            plot_window.state('zoomed')    
            fig = ADgraph.plot_ADnum(function_output, ins = master_ins)
            canvas = FigureCanvasTkAgg(fig, master=plot_window)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            toolbar = NavigationToolbar2Tk(canvas, plot_window)
            toolbar.update()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        def graph_instructions():
            text = "Use this window to visualize how automatic differentiation is performed on your function.\n \n" +\
            "First, type numbers into the boxes to set values for the input variables.  Press \'Set Input Values\' to calculate the value and" +\
            " derivative of your function at this point. \n \n" +\
            "After setting the input values, you can visualize the computational graph and evaluation table associated with each function in forward mode.  Press the button corresponding to the function you want to analyze under each heading." +\
            "You can also dynamically visualize the steps in the calculation of a derivative in Reverse Mode or view the entire reverse graph."
            messagebox.showinfo('Visualize Function Computations', text, parent=graph_window)

        graph_master = tk.Tk()
        #graph_master = tk.Toplevel(master)
        #graph_window.geometry("400x675")
        graph_master.state('zoomed')
        graph_master.title("Graph Generator")
        graph_window = tk.Frame(graph_master, height = 32, width = 32)
        graph_window.place(relx=.5, rely=.5, anchor=tk.CENTER)
        #global function_output
        instruction_graph = tk.Button(graph_master, text = 'Instructions',fg = "Orange",command = graph_instructions).place(relx=0, rely=0, anchor = tk.NW)

        #if master_ins < 3:
         #   show_plot = tk.Button(graph_window, text = "Visualize function", height = 3, width = 20, command = show_plot).grid(row = 4, column = 0, columnspan = 2)
        value_x = tk.DoubleVar()
        value_y = tk.DoubleVar()
        value_z = tk.DoubleVar()
        value_m = tk.DoubleVar()
        value_n = tk.DoubleVar()
        value_k = tk.DoubleVar()
        def draw_graph():
            try:
                fig = ADgraph.draw_graph2(out_num[0], G[0], edge_labs[0], pos[0], labs[0])    
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def draw_graph1():
            try:
                fig = ADgraph.draw_graph2(out_num[1], G[1], edge_labs[1], pos[1], labs[1])    
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def draw_graph2():
            try:
                fig = ADgraph.draw_graph2(out_num[2], G[2], edge_labs[2], pos[2], labs[2])    
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        
        
        
        def draw_table():
            try:
                plot_graph2 = tk.Toplevel(graph_window)
                plot_graph2.title("Forward Computational Table")
                plot_graph2.geometry("600x600")
    #         fig = ADgraph.gen_table(function_output)
                f = tk.Frame(plot_graph2)
                f.pack(side=tk.TOP,fill=tk.BOTH,expand=1)
                df = ADgraph.gen_table(out_num[0])
                #df = ADgraph.gen_table(function_output(ADnum(value_x.get(),ins=6,ind=0),ADnum(value_y.get(),ins=6,ind=1),ADnum(value_z.get(),ins=6,ind=2),ADnum(value_m.get(),ins=6,ind=3),ADnum(value_n.get(),ins=6,ind=4),ADnum(value_k.get(),ins=6,ind=5)))
                table = pt = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
                pt.show()
            except NameError:
                plot_graph2.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
        def draw_table1():
            try:
                plot_graph2 = tk.Toplevel(graph_window)
                plot_graph2.title("Forward Computational Table")
                plot_graph2.geometry("600x600")
    #         fig = ADgraph.gen_table(function_output)
                f = tk.Frame(plot_graph2)
                f.pack(side=tk.TOP,fill=tk.BOTH,expand=1)
                df = ADgraph.gen_table(out_num[1])
                #df = ADgraph.gen_table(function_output(ADnum(value_x.get(),ins=6,ind=0),ADnum(value_y.get(),ins=6,ind=1),ADnum(value_z.get(),ins=6,ind=2),ADnum(value_m.get(),ins=6,ind=3),ADnum(value_n.get(),ins=6,ind=4),ADnum(value_k.get(),ins=6,ind=5)))
                table = pt = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
                pt.show()
            except NameError:
                plot_graph2.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def draw_table2():
            try:
                plot_graph2 = tk.Toplevel(graph_window)
                plot_graph2.title("Forward Computational Table")
                plot_graph2.geometry("600x600")
    #         fig = ADgraph.gen_table(function_output)
                f = tk.Frame(plot_graph2)
                f.pack(side=tk.TOP,fill=tk.BOTH,expand=1)
                df = ADgraph.gen_table(out_num[2])
                #df = ADgraph.gen_table(function_output(ADnum(value_x.get(),ins=6,ind=0),ADnum(value_y.get(),ins=6,ind=1),ADnum(value_z.get(),ins=6,ind=2),ADnum(value_m.get(),ins=6,ind=3),ADnum(value_n.get(),ins=6,ind=4),ADnum(value_k.get(),ins=6,ind=5)))
                table = pt = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
                pt.show()
            except NameError:
                plot_graph2.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        
        def vis_rev_x():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[0], x[0].revder(out_num[0])[1], G[0], edge_labs[0], pos[0], labs[0], x[0].revder(out_num[0])[0])
            except NameError:
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def vis_rev_y():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[0], y[0].revder(out_num[0])[1], G[0], edge_labs[0], pos[0], labs[0], y[0].revder(out_num[0])[0])
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def vis_rev_z():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[0], z[0].revder(out_num[0])[1], G[0], edge_labs[0], pos[0], labs[0], z[0].revder(out_num[0])[0])
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent = graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def vis_rev_u():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[0], u[0].revder(out_num[0])[1], G[0], edge_labs[0], pos[0], labs[0], u[0].revder(out_num[0])[0])
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def vis_rev_v():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[0], v[0].revder(out_num[0])[1], G[0], edge_labs[0], pos[0], labs[0], v[0].revder(out_num[0])[0])
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
                plt.close()
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        
        def vis_rev_x1():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[1], x[1].revder(out_num[1])[1], G[1], edge_labs[1], pos[1], labs[1], x[1].revder(out_num[1])[0])
            except NameError:
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def vis_rev_y1():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[1], y[1].revder(out_num[1])[1], G[1], edge_labs[1], pos[1], labs[1], y[1].revder(out_num[1])[0])
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def vis_rev_z1():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[1], z[1].revder(out_num[1])[1], G[1], edge_labs[1], pos[1], labs[1], z[1].revder(out_num[1])[0])
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent = graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def vis_rev_u1():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[1], u[1].revder(out_num[1])[1], G[1], edge_labs[1], pos[1], labs[1], u[1].revder(out_num[1])[0])
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
                plt.close()
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def vis_rev_v1():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[1], v[1].revder(out_num[1])[1], G[1], edge_labs[1], pos[1], labs[1], v[1].revder(out_num[1])[0])
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
                plt.close()
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        
        def vis_rev_x2():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[2], x[2].revder(out_num[2])[1], G[2], edge_labs[2], pos[2], labs[2], x[2].revder(out_num[2])[0])
            except NameError:
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def vis_rev_y2():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[2], y[2].revder(out_num[2])[1], G[2], edge_labs[2], pos[2], labs[2], y[2].revder(out_num[2])[0])
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def vis_rev_z2():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[2], z[2].revder(out_num[2])[1], G[2], edge_labs[2], pos[2], labs[2], z[2].revder(out_num[2])[0])
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent = graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def vis_rev_u2():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[2], u[2].revder(out_num[2])[1], G[2], edge_labs[2], pos[2], labs[2], u[2].revder(out_num[2])[0])
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        def vis_rev_v2():
            try:
                fig = ADgraph.draw_graph_rev_dynamic(out_num[2], v[2].revder(out_num[2])[1], G[2], edge_labs[2], pos[2], labs[2], v[2].revder(out_num[2])[0])
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent=graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()


        
        def rev_draw_graph():
            try:
                fig = ADgraph.draw_graph_rev2(out_num[0], G[0], edge_labs[0], pos[0], labs[0])    
            except NameError:
                #plot_graph.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent = graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent = graph_window)
                plt.close()

        def rev_draw_graph1():
            try:
                fig = ADgraph.draw_graph_rev2(out_num[1], G[1], edge_labs[1], pos[1], labs[1])
            except NameError:
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent = graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()

        def rev_draw_graph2():
            try:
                fig = ADgraph.draw_graph_rev2(out_num[2], G[2], edge_labs[2], pos[2], labs[2])
            except NameError:
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent = graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
                plt.close()
        
        def rev_draw_table():
            try:
                plot_graph2 = tk.Toplevel(graph_window)
                plot_graph2.title("Reverse Computational Table")
                plot_graph2.geometry("600x600")
    #         fig = ADgraph.gen_table(function_output)
                f = tk.Frame(plot_graph2)
                f.pack(side=tk.TOP,fill=tk.BOTH,expand=1)
                df = ADgraph.gen_table_rev(out_num[0])
                #df = ADgraph.gen_table(function_output(ADnum(value_x.get(),ins=6,ind=0),ADnum(value_y.get(),ins=6,ind=1),ADnum(value_z.get(),ins=6,ind=2),ADnum(value_m.get(),ins=6,ind=3),ADnum(value_n.get(),ins=6,ind=4),ADnum(value_k.get(),ins=6,ind=5)))
                table = pt = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
                pt.show()
            except NameError:
                plot_graph2.destroy()
                messagebox.showinfo("Error", "Please use \'Set Input Values\' to define your input values.", parent = graph_window)
            except AttributeError:
                messagebox.showinfo('Error', 'Function is a constant.', parent=graph_window)
        if func_content[0].get()[0] != 'f':
            func_content[0].set('f1 = '+func_content[0].get())
        if master_outs > 1:
            if func_content[1].get()[0] != 'f':
                func_content[1].set('f2 = '+func_content[1].get())
        if master_outs >2:
            if func_content[2].get()[0]!= 'f':
                func_content[2].set('f3 = '+func_content[2].get())

        #orientation labels
        if master_outs == 1:
            func_label = tk.Label(graph_window, textvariable = func_content[0], font = ('wasy10', 24)).grid(row=0, column=2, columnspan=2)
        if master_outs == 2:
            func1_label = tk.Label(graph_window, textvariable = func_content[0], font = ('wasy10', 24)).grid(row=0, column = 0, columnspan = 2)
            func2_label = tk.Label(graph_window, textvariable = func_content[1], font = ('wasy10', 24)).grid(row=0, column = 2, columnspan = 3)
        if master_outs == 3:
            func1_label = tk.Label(graph_window, textvariable = func_content[0], font = ('wasy10', 24)).grid(row=0, column = 0, columnspan = 2)
            func2_label = tk.Label(graph_window, textvariable = func_content[1], font = ('wasy10', 24)).grid(row=0, column = 2, columnspan = 3)
            func3_label = tk.Label(graph_window, textvariable = func_content[2], font = ('wasy10', 24)).grid(row=0, column = 5, columnspan=5)
        setup_label = tk.Label(graph_window, text = 'EVALUATE AT', height = 3, width = 30, font= ('wasy10', 20)).grid(row=1, column = 0, columnspan = 2)
        forward_label = tk.Label(graph_window, text = 'FORWARD MODE', height=3, width = 30, font = ('wasy10', 20)).grid(row = 1, column = 2, columnspan = 3)
        reverse_label = tk.Label(graph_window, text = 'REVERSE MODE', height = 3, width = 30, font = ('wasy10', 20)).grid(row=1, column=5, columnspan = 5)


        value_prompt_x = tk.Label(graph_window, text = "  Evaluate at x = ",height = 3, width = 15, font = ('wasy10', 12)).grid(row = 2, column = 0)
        enter_value_x = tk.Entry(graph_window, textvariable = value_x, width = 10).grid(row = 2, column = 1)
        if master_ins > 1:
            value_prompt_y = tk.Label(graph_window, text = "  Evaluate at y = ",height = 3, width = 15, font = ('wasy10',12)).grid(row = 3, column = 0)
            enter_value_y = tk.Entry(graph_window, textvariable = value_y, width = 10).grid(row = 3, column = 1)
            if master_ins >2:
                value_prompt_z = tk.Label(graph_window, text = "  Evaluate at z = ",height = 3, width = 15, font = ('wasy10', 12)).grid(row = 4, column = 0)
                enter_value_z = tk.Entry(graph_window, textvariable = value_z, width = 10).grid(row = 4, column = 1)
                if master_ins > 3:
                    value_prompt_m = tk.Label(graph_window, text = "  Evaluate at u =  ",height = 3, width = 15, font = ('wasy10', 12)).grid(row = 5, column = 0)
                    enter_value_m= tk.Entry(graph_window, textvariable = value_m, width = 10).grid(row = 5, column = 1)
                    if master_ins > 4:
                        value_prompt_n= tk.Label(graph_window, text = "  Evaluate at v = ",height = 3, width = 15, font = ('wasy10', 12)).grid(row = 6, column = 0)
                        enter_value_n= tk.Entry(graph_window, textvariable = value_n, width = 10).grid(row = 6, column = 1)
                        if master_ins>5:
                            value_prompt_k= tk.Label(graph_window, text = "  Evaluate at w = ",height = 3, width = 15).grid(row = 7, column = 0)
                            enter_value_k= tk.Entry(graph_window, textvariable = value_k, width = 10).grid(row = 7, column = 1)
        
        def display():
            if not (type(value_x.get())==float and type(value_y.get())==float and type(value_z.get())==float
                   and type(value_m.get())==float and type(value_n.get())==float and type(value_k.get())==float):
                messagebox.showerror('Error', 'Please enter a numeric value for the inputs.')
            global x
            x = [ADnum(value_x.get(), ins = master_ins, ind = 0)]*master_outs
            if master_ins>1:
                global y
                y = [ADnum(value_y.get(), ins = master_ins, ind =1)]*master_outs
                if master_ins>2:
                    global z
                    z = [ADnum(value_z.get(), ins = master_ins, ind = 2)]*master_outs
                    if master_ins >3:
                        global u
                        u = [ADnum(value_m.get(), ins = master_ins, ind=3)]*master_outs
                        if master_ins > 4:
                            global v
                            v = [ADnum(value_n.get(), ins = master_ins, ind = 4)]*master_outs
                            if master_ins>5:
                                global w
                                w = ADnum(value_k.get(), ins = master_ins, ind = 5)
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
                if master_ins == 6:
                    out_num[i] = function_output[i](x, y, z, u, v, w)
            
            #disp_val = str([np.round(f.val, 2) for f in out_num])
            #disp_der = str([np.round(f.der, 2) for f in out_num])
            disp_val = '['
            disp_der = '['
            for out in out_num:
                try:
                    disp_val += str(np.round(out.val,2))
                    disp_der += str(np.round(out.der, 2))
                except AttributeError:
                    disp_val += str(np.round(out, 2))
                    disp_der += str([0]*master_ins)
                disp_val += ',\n'
                disp_der += ',\n'
            disp_val = disp_val[:-2]+']'
            disp_der = disp_der[:-2]+']'


            show_value = tk.Label(graph_window, text = disp_val, height = 3, width = 15, font = ('wasy10', 12), fg = 'green').grid(row = 3, column = 2, columnspan=3)
            show_derivatice = tk.Label(graph_window, text = disp_der, height = 3, width = 25, font = ('wasy10', 12), fg='green').grid(row = 5, column =2, columnspan = 3)
            
            inputs_list = ['x', 'y', 'z', 'u', 'v']
            vis_funcs = [[vis_rev_x, vis_rev_x1, vis_rev_x2], [vis_rev_y, vis_rev_y1, vis_rev_y2], [vis_rev_z, vis_rev_z1, vis_rev_z2], [vis_rev_u, vis_rev_u1, vis_rev_u2], [vis_rev_v, vis_rev_v1, vis_rev_v2]]
            for i in range(master_ins):
                for j in range(master_outs):
                    tk.Button(graph_window, text = "df" + str(j+1)+"/d" + inputs_list[i], height=3, width=5, command=vis_funcs[i][j]).grid(row=3+j, column=5+i, columnspan =1)
            
            
            
            
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

        
        result_val = tk.Label(graph_window, text = "Function Value:",height = 3, width = 15, font = ('wasy10', 12)).grid(row =2, column =2, columnspan=3)
        result_der = tk.Label(graph_window, text= "Gradient: ",height = 3, width = 15, font = ('wasy10', 12)).grid(row = 4, column = 2, columnspan=3)
        #result_ops = tk.Label(graph_window, text="Forward Ops:", height =3, width=15, font = ('wasy10', 12)).grid(row= 6, column = 2, columnspan=3)
        vis_label = tk.Label(graph_window, text = 'Visualize Reverse Calculation:', height = 3, width = 25, font = ('wasy10', 12)).grid(row=2, column=5, columnspan=5)

        enter_button = tk.Button(graph_window, text = "Set Input Values", height = 3, width = 20, command = display).grid(row = master_ins + 2, column = 0, columnspan = 2)
        #vis_rev_prompt = tk.Button(graph_window, text = "Visualize Reverse Calc", height = 3, width = 20, command = vis_rev_x).grid(row=2, column = 5, columnspan=1)
        eval_label = tk.Label(graph_window, text = 'Computational Graph:', height =3, width = 30, font = ('wasy10', 12)).grid(row=8, column=2, columnspan=3)
        eval_prompt = tk.Button(graph_window, text = "f1",height = 3, width = 5, command = draw_graph).grid(row = 9, column = 2,columnspan = 1)
        table_label = tk.Label(graph_window, text = 'Evaluation Table:', height =3, width =30, font = ('wasy10', 12)).grid(row=10, column=2, columnspan=3)
        table_prompt = tk.Button(graph_window, text = "f1",height = 3, width = 5, command = draw_table).grid(row = 11, column = 2,columnspan = 1)
        rev_eval_label = tk.Label(graph_window, text = "Reverse Graph:", height = 3, width = 30, font = ('wasy10', 12)).grid(row=8, column =5, columnspan=5)
        #rev_table_label = tk.Label(graph_window, text = 'Reverse Table:', height = 3, width = 30, font = ('wasy10', 12)).grid(row=10, column=5, columnspan=5)
        rev_eval_prompt = tk.Button(graph_window, text = "f1",height = 3, width = 5, command = rev_draw_graph).grid(row = 9, column = 6,columnspan = 1)
        #rev_table_prompt = tk.Button(graph_window, text = "f1",height = 3, width = 5, command = rev_draw_table).grid(row = 11, column = 5,columnspan = 1)
        if master_outs>1:
            eval_prompt1 = tk.Button(graph_window, text = "f2",height = 3, width = 5, command = draw_graph1).grid(row = 9, column = 3,columnspan = 1)
            table_prompt1 = tk.Button(graph_window, text = "f2",height = 3, width = 5, command = draw_table1).grid(row = 11, column = 3,columnspan = 1)
            rev_eval_prompt1 = tk.Button(graph_window, text = "f2",height = 3, width = 5, command = rev_draw_graph1).grid(row = 9, column = 7,columnspan = 1)
        if master_outs>2:
            eval_prompt2 = tk.Button(graph_window, text = "f3",height = 3, width = 5, command = draw_graph2).grid(row = 9, column = 4,columnspan = 1)
            table_prompt2 = tk.Button(graph_window, text = "f3",height = 3, width = 5, command = draw_table2).grid(row = 11, column = 4,columnspan = 1)
            rev_eval_prompt2 = tk.Button(graph_window, text = "f3",height = 3, width = 5, command = rev_draw_graph2).grid(row = 9, column = 8,columnspan = 1)
        graph_master.mainloop()
        


    #===Block for Error message====
    def error_window():
        error_window = tk.Toplevel(master)
        error_window.title("Error!")
        error_message = tk.Label(error_window, text = "Invalid expression! Please start over and try again!")
        error_message.pack(side = 'top')
    #=====Function for master configuration's buttons======
    def var_number_x():
        edit_func("x")
        global function_expression
        function_expression[editing] +='x'
    def add():
        edit_func("+")
        global function_expression
        function_expression[editing] +='+'

    def sub():
        edit_func("-")
        global function_expression
        function_expression[editing] +='-'

    def mul():
        edit_func("*")
        global function_expression
        function_expression[editing] +='*'

    def div():
        edit_func("/")
        global function_expression
        function_expression[editing] +='/'

    def num_0():
        edit_func("0")
        global function_expression
        function_expression[editing] +='0'
    def num_1():
        edit_func("1")
        global function_expression
        function_expression[editing] +='1'
    def num_2():
        edit_func("2")
        global function_expression
        function_expression[editing] +='2'
    def num_3():
        edit_func("3")
        global function_expression
        function_expression[editing] += '3'
    def num_4():
        edit_func("4")
        global function_expression
        function_expression[editing] += '4'
    def num_5():
        edit_func("5")
        global function_expression
        function_expression[editing] += '5'
    def num_6():
        edit_func("6")
        global function_expression
        function_expression[editing] += '6'
    def num_7():
        edit_func("7")
        global function_expression
        function_expression[editing] += '7'
    def num_8():
        edit_func("8")
        global function_expression
        function_expression[editing] += '8'
    def num_9():
        edit_func("9")
        global function_expression
        function_expression[editing] += '9'
    def num_dot():
        edit_func(".")
        global function_expression
        function_expression[editing] += '.'
    #===Add more functions to the added buttons===
    def sin():
        edit_func("sin(")
        global function_expression
        function_expression[editing] += 'ADmath.sin('
    def cos():
        edit_func("cos(")
        global function_expression
        function_expression[editing] += 'ADmath.cos('
    def tan():
        edit_func("tan(")
        global function_expression
        function_expression[editing] += 'ADmath.tan('
    def exp():
        edit_func("exp(")
        global function_expression
        function_expression[editing] += 'ADmath.exp('
    def log():
        edit_func("log(")
        global function_expression
        function_expression[editing] += 'ADmath.log('
    def pow_to():
        edit_func("pow(")
        global function_expression
        function_expression[editing] += '**('
    def sqrt():
        edit_func("sqrt(")
        global function_expression
        function_expression[editing] += 'ADmath.sqrt('
    def right_par():
        edit_func("(")
        global function_expression
        function_expression[editing] += '('
    def left_par():
        edit_func(")")
        global function_expression
        function_expression[editing] += ")"
    #====End of Function of master buttons

    #===2019 Add Functions to Extra Buttons===
    def var_number_y():
        edit_func("y")
        global function_expression
        function_expression[editing] +='y'

    def var_number_z():
        edit_func("z")
        global function_expression
        function_expression[editing] +='z'

    def var_number_m():
        edit_func("u")
        global function_expression
        function_expression[editing] +='u'

    def var_number_n():
        edit_func("v")
        global function_expression
        function_expression[editing] +='v'

    def var_number_k():
        edit_func("w")
        global function_expression
        function_expression[editing] +='w'


    #===2019 Add Functions to Extra Buttons Ends===
    def back_space():
        global function_expression
        function_expression[editing] = backstep(function_expression[editing])
        back_func()

    def backstep(text):
        if len(text) == 0:
            func_content[editing].set("")
            return ""
        if text[-1]=='(' and text[-2] in ['n', 't', 'p', 's', 'g', '*']:
            if text[-2] == 't':
                return text[:-12]
            elif (text[-2] == '*' and text[-3]=='*'):
                return text[:-3]
            else:
                return text[:-12]
        else:
            return text[:-1]
    
    
    def clear_all():
        func_content[editing].set("")
        function_expression[editing] = " "
        function_output[editing] = lambda x :0
    
    def get_func(function_expression, i):
        if master_ins == 1:
            def f(x):
                return eval(function_expression[i])
        if master_ins == 2:
            def f(x,y):
                return eval(function_expression[i])
        if master_ins == 3:
            def f(x,y,z):
                return eval(function_expression[i])
        if master_ins == 4:
            def f(x, y, z, u):
                return eval(function_expression[i])
        if master_ins == 5:
            def f(x,y,z,u,v):
                return eval(function_expression[i])
        return f

    def confirm():
        try:
            for i in range(master_outs):
                function_output[i] = get_func(function_expression, i)
                if master_ins ==1:
                    function_output[i](1)
                if master_ins == 2:
                    function_output[i](1,1)
                if master_ins ==3:
                    function_output[i](1,1,1)
                if master_ins ==4:
                    function_output[i](1,1,1,1)
                if master_ins ==5:
                    function_output[i](1,1,1,1,1)
            master.destroy()
            graph_master()
        except AttributeError:
            if master_ins ==1:
                messagebox.showinfo("Constant result:","The value is {}".format(function_output(1)))
            if master_ins ==2:
                messagebox.showinfo("Constant result:","The value is {}".format(function_output(1,1)))
            if master_ins ==3:
                messagebox.showinfo("Constant result:","The value is {}".format(function_output(1,1,1)))
            if master_ins ==4:
                messagebox.showinfo("Constant result:","The value is {}".format(function_output(1,1,1,1)))
            if master_ins ==5:
                messagebox.showinfo("Constant result:","The value is {}".format(function_output(1,1,1,1,1)))
        except NameError:
            messagebox.showerror("Error", "Syntax error in your expression.  Please edit the expression, and try again.")
        except SyntaxError:
            messagebox.showerror("Error", "Syntax error in your expression.  Please edit the expression, and try again.")


    def edit_func(text):
        content = func_content[editing].get()+text
        func_content[editing].set(content)

    def back_func():
        content = func_content[editing].get()
        if len(content) == 0:
          content = content          
        elif content[-1]=='(' and content[-2] in ['t', 'n', 'w', 's', 'p', 'g']:
            if content[-2] == 't':
                content = content[:-5]
            elif content[-2] == 'w' and content[-3]!='o':
                content = content[:-1]
            else:
                content = content[:-4]
        else:
            content = content[:-1]
        func_content[editing].set(content)

    ##Set up button 
    cal_frame = tk.Frame(master,height=32, width=32)
    cal_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    #===2019 Add Variable Buttons===
    if master_ins>1:
        button_y = tk.Button(cal_frame, text = "y", font=('wasy10', 20),fg = "magenta",height=2, width=5,command = var_number_y).grid(row = 8, column = 1)
        if master_ins>2:
            button_z = tk.Button(cal_frame, text = "z", font=('wasy10', 20),fg = "magenta",height=2, width=5,command = var_number_z).grid(row = 8, column = 2)
            if master_ins>3:
                button_m = tk.Button(cal_frame, text = "u", font=('wasy10', 20),fg = "magenta",height=2, width=5,command = var_number_m).grid(row = 8, column = 3)
                if master_ins>4:
                    button_n = tk.Button(cal_frame, text = "v", font=('wasy10', 20),fg = "magenta",height=2, width=5,command = var_number_n).grid(row = 8, column = 4) 
                    if master_ins>5:
                        button_k = tk.Button(cal_frame, text = "w", font=('wasy10', 20),fg = "magenta",height=2, width=5,command = var_number_k).grid(row = 8, column = 5) 
    #===2019 Add Variable Buttons End===
    #===Add Buttons=====
    button_sin = tk.Button(cal_frame, text = "sin", font=('wasy10', 20),height=2, width=5,command = sin).grid(row = 3, column = 0)
    button_cos = tk.Button(cal_frame, text = "cos", font=('wasy10', 20),height=2, width=5,command = cos).grid(row = 3, column = 1)
    button_tan = tk.Button(cal_frame, text = "tan", font=('wasy10', 20),height=2, width=5,command = tan).grid(row = 3, column = 2)
    button_exp = tk.Button(cal_frame, text = "exp", font=('wasy10', 20),height=2, width=5,command = exp).grid(row = 3, column = 3) 
    button_log = tk.Button(cal_frame, text = "log", font=('wasy10', 20),height=2, width=5,command = log).grid(row = 3, column = 4) 
    button_pow = tk.Button(cal_frame, text = "pow", font=('wasy10', 20),height=2, width=5,command = pow_to).grid(row = 4, column = 4)
    button_sqrt = tk.Button(cal_frame, text = "sqrt", font=('wasy10', 20),height=2, width=5,command = sqrt).grid(row = 5, column =4)
    button_rightPar = tk.Button(cal_frame, text = "(", font=('wasy10', 20),height=2, width=5,command = right_par).grid(row = 6, column =4)
    button_leftPar = tk.Button(cal_frame, text = ")", font=('wasy10', 20),height=2, width=5,command = left_par).grid(row = 7, column =4)
    #=====Add Buttons End===
    if master_ins==1:
        show_function = tk.Label(cal_frame, text = "f1(x) = ").grid(row = 0, column = 0)
        if master_outs >1:
            show_function2 = tk.Label(cal_frame, text = "f2(x)= ").grid(row=0, column=9)
        if master_outs >2:
            show_function3 = tk.Label(cal_frame, text = "f3(x)= ").grid(row=0, column=18)

    if master_ins==2:
        show_function = tk.Label(cal_frame, text = "f1(x, y) = ").grid(row = 0, column = 0)
        if master_outs >1:
            show_function2 = tk.Label(cal_frame, text = "f2(x, y)= ").grid(row=0, column=9)
        if master_outs >2:
            show_function3 = tk.Label(cal_frame, text = "f3(x, y)= ").grid(row=0, column=18)
 
    if master_ins==3:
        show_function = tk.Label(cal_frame, text = "f1(x, y, z) = ").grid(row = 0, column = 0)
        if master_outs >1:
            show_function2 = tk.Label(cal_frame, text = "f2(x, y, z)= ").grid(row=0, column=9)
        if master_outs >2:
            show_function3 = tk.Label(cal_frame, text = "f3(x, y, z)= ").grid(row=0, column=18)
       
    if master_ins==4:
        show_function = tk.Label(cal_frame, text = "f1(x, y, z, u) = ").grid(row = 0, column = 0)
        if master_outs >1:
            show_function2 = tk.Label(cal_frame, text = "f2(x, y, z, u)= ").grid(row=0, column=9)
        if master_outs >2:
            show_function3 = tk.Label(cal_frame, text = "f3(x, y, z, u)= ").grid(row=0, column=18)
 
    if master_ins==5:
        show_function = tk.Label(cal_frame, text = "f1(x, y, z, u, v) = ").grid(row = 0, column = 0)
        if master_outs >1:
            show_function2 = tk.Label(cal_frame, text = "f2(x, y, z, u, v)= ").grid(row=0, column=9)
        if master_outs >2:
            show_function3 = tk.Label(cal_frame, text = "f3(x, y, z, u, v)= ").grid(row=0, column=18)
    
    global editing
    editing = 0
    
    def edit_select1():
        global editing
        editing = 0

    def edit_select2():
        global editing
        editing = 1

    def edit_select3():
        global editing
        editing = 2

    if master_outs>1:
        tk.Button(cal_frame, text = "Edit f1", command=edit_select1).grid(row=1, column=0)
        tk.Button(cal_frame, text = "Edit f2", command=edit_select2).grid(row=1, column=9)
    if master_outs>2:
        tk.Button(cal_frame, text = "Edit f3", command = edit_select3).grid(row=1, column=18)

    button_backspace = tk.Button(cal_frame, text= u'\u2B05', font=('wasy10', 20), height=2, width=5,command= back_space).grid(row=7, column = 2)

    button_x = tk.Button(cal_frame, text = "x", font=('wasy10', 20),fg = "magenta",height=2, width=5,command = var_number_x).grid(row = 8, column =0)

    button_add = tk.Button(cal_frame, text = '+', font=('wasy10', 20),height=2, width=5,command = add).grid(row = 4, column = 3) # can add command

    button_sub = tk.Button(cal_frame, text = "-",font=('wasy10', 20),height=2, width=5,command = sub).grid(row = 5, column = 3)

    button_mul = tk.Button(cal_frame, text = "*",font=('wasy10', 20),height=2, width=5,command = mul).grid(row = 6, column = 3)

    button_div = tk.Button(cal_frame, text = "/",font=('wasy10', 20),height=2, width=5,command = div).grid(row = 7, column = 3)

    button_0 = tk.Button(cal_frame, text = "0",font=('wasy10', 20),height=2, width=5,command = num_0).grid(row = 7, column = 0)

    button_1 = tk.Button(cal_frame, text = "1",font=('wasy10', 20),height=2, width=5,command = num_1).grid(row = 6, column = 0)

    button_2 = tk.Button(cal_frame, text = "2",font=('wasy10', 20),height=2, width=5,command = num_2).grid(row = 6, column = 1)

    button_3 = tk.Button(cal_frame, text = "3",font=('wasy10', 20),height=2, width=5,command = num_3).grid(row = 6, column = 2)

    button_4 = tk.Button(cal_frame, text = "4",font=('wasy10', 20),height=2, width=5,command = num_4).grid(row = 5, column = 0)

    button_5 = tk.Button(cal_frame, text = "5",font=('wasy10', 20),height=2, width=5,command = num_5).grid(row = 5, column = 1)

    button_6 = tk.Button(cal_frame, text = "6",font=('wasy10', 20),height=2, width=5,command = num_6).grid(row = 5, column = 2)

    button_7 = tk.Button(cal_frame, text = "7",font=('wasy10', 20),height=2, width=5,command = num_7).grid(row = 4, column = 0)

    button_8 = tk.Button(cal_frame, text = "8",font=('wasy10', 20),height=2, width=5,command = num_8).grid(row = 4, column = 1)

    button_9 = tk.Button(cal_frame, text = "9",font=('wasy10', 20),height=2, width=5,command = num_9).grid(row = 4, column = 2)

    button_dot = tk.Button(cal_frame, text = ".",font=('wasy10', 20),height=2, width=5,command = num_dot).grid(row = 7, column = 1)

    button_confirm = tk.Button(cal_frame, text = "Calculate",font=('wasy10', 20),height=2, width=22,command = confirm).grid(row = 9, columnspan =8)

    button_clearAll = tk.Button(cal_frame, text = "Clear Function",font=('wasy10', 20),height=2, width=22,command = clear_all).grid(row = 10,columnspan =8)

    show_func = tk.Label(cal_frame, textvariable = func_content[0],height=2, width=30,bg = 'Seashell').grid(row = 0,column = 1,columnspan =7)
    if master_outs>1:
        show_func2 = tk.Label(cal_frame, textvariable = func_content[1],height=2, width=30,bg = 'Seashell').grid(row = 0,column = 10,columnspan =7)
    if master_outs>2:
        show_func3 = tk.Label(cal_frame, textvariable = func_content[2],height=2, width=30,bg = 'Seashell').grid(row = 0,column = 19,columnspan =7)
    #=====End of configuration========
   
    
    # if __name__=='main':
    master.resizable(width=True, height=True)
    master.mainloop()
