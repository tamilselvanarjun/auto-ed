from flask import Flask, render_template, request
app = Flask(__name__)

import matplotlib.pyplot as plt
import numpy as np

@app.route('/', methods=['GET', 'POST'])

def go():
    if request.method == "POST":
        make_plot()
    return render_template('basic_test.html')

def make_plot():
    x = np.linspace(0, np.pi, 100)
    plt.plot(x, np.sin(x))
    plt.show()

if __name__ == '__main__':
    app.run('0.0.0.0', port = 5000, threaded = False)
