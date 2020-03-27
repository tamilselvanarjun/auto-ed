import random
import io

from flask import Flask, make_response, send_file, render_template, url_for
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

@app.route('/plot.png')
def plot():
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]

    axis.plot(xs, ys)

    canvas = FigureCanvas(fig)

    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/fig/')
def fig():
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    xs = [1, 2, 3, 4, 5]
    ys = [1, 2, 3, 4, 5]
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)

    output = io.BytesIO()
    fig.savefig(output)
    output.seek(0)
    return send_file(output, mimetype='image/png')

@app.route('/reports/')
def reports():
    return render_template('report.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, threaded=False)
