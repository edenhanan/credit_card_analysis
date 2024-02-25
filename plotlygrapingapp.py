from flask import Flask, render_template
import plotly
import plotly.graph_objs as go
import json
import json

app = Flask(__name__)

@app.route('/')
def index():
    # Load data from cumulative_sum.json
    with open('cumulative_sum.json') as f:
        data = json.load(f)

    fig = go.Figure(data=go.Scatter(x=list(data.keys()), y=list(data.values())))
    fig.update_layout(
    xaxis=dict(title='Date'),
    yaxis=dict(title='Cumulative Sum'),
    title='Cumulative Sum Plot',
    xaxis_tickangle=-45
)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)