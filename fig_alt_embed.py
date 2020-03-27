import io
import random
from flask import Flask, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG

from matplotlib.figure import Figure

app = Flask(__name__)

@app.route('/')
def index():
    num_x_points = int(request.args.get("num_x_points", 50))

    return f"""
    <h1>Flask and matplotlib</h1>

    <h2>Random data with num_x_points={num_x_points}</h2>

    <form method=get action='/'>
    <input name="num_x_points" type=number value="{num_x_points}" />
    <input type=submit value = "update graph">
    </form>

    <h3>Plot as a png</h3>
    <img src='/matplot-as-image-{num_x_points}.png' alt='random points as png' height="200">

    <h3> Plot as a SVG </h3>
    <img src='/matplot-as-image-{num_x_points}.svg' alt='random points as svg' height='200'>
    """

@app.route("/matplot-as-image-<int:num_x_points>.png")
def plot_png(num_x_points=50):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(num_x_points)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route("/matplot-as-image-<int:num_x_points>.svg")
def plot_svg(num_x_points=50):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(num_x_points)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])
    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype='image/svg+xml')

if __name__=='__main__':
    app.run('0.0.0.0', port=5000, threaded=False)
