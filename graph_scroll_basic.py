import matplotlib.pyplot as plt
import numpy as np
from ADnum_rev_timed_vis import ADnum
import ADmath_rev as ADmath
import ADgraph_GUI as ADgraph

#x = ADnum(1, ins=1, ind=0)
#f = x**3-3*x**2

#ADgraph.draw_graph_rev_dynamic(f, x.revder(f)[1])

#fig = ADgraph.draw_graph(f)
#plt.show()


#fig, figset = ADgraph.draw_graph_rev_dynamic(f, x.revder(f)[1])
#plt.show()





# define your x and y arrays to be plotted
t = np.linspace(start=0, stop=2*np.pi, num=100)
y1 = np.cos(t)
y2 = np.sin(t)
y3 = np.tan(t)
plots = [(t,y1), (t,y2), (t,y3)]

# now the real code :)





curr_pos = 0


def key_event(e):
    global curr_pos

    if e.key == "right":
        curr_pos = curr_pos + 1
    elif e.key == "left":
        curr_pos = curr_pos - 1
    else:
        return
    #curr_pos = curr_pos % len(figset)

    
    #figset[curr_pos].show()
    ax.cla()
    ax.plot(plots[curr_pos][0], plots[curr_pos][1])
    fig.canvas.draw()

fig = plt.figure()
fig.canvas.mpl_connect('key_press_event', key_event)
#figset[0].show()
ax = fig.add_subplot(111)
ax.plot(t,y1)
plt.show()

