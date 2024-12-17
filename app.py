from dash import Dash, dcc, html, Input, Output 
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import random

# Initialize the app
app = Dash(__name__)

# Initial data
start_time = datetime.now()
df = pd.DataFrame({
    "Time": [start_time + timedelta(seconds=i) for i in range(5)],
    "Celsius": [random.randint(0, 40) for _ in range(5)],
    "Fahrenheit": [random.randint(32, 104) for _ in range(5)],
})

# App layout
app.layout = html.Div([
    html.H1("Real-Time Temperature Converter", style={"textAlign": "center"}),
    dcc.Graph(id="temperature-graph"),
    dcc.Slider(
        id="temp-slider",
        min=-50,
        max=50,
        value=0,
        step=1,
        marks={i: str(i) for i in range(-50, 51, 10)},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.P("Adjust Celsius Value", style={"textAlign": "center"})
])

# Callback to update graph
@app.callback(
    Output("temperature-graph", "figure"),
    Input("temp-slider", "value")
)

def update_graph(celsius):
    global df
    current_time = datetime.now()
    fahrenheit = (celsius * 9/5) + 32

    # Add new data to the dataframe
    new_row = {
        "Time": current_time,
        "Celsius": celsius,
        "Fahrenheit": fahrenheit,
    }
    df = pd.concat([df, pd.DataFrame([new_row])]).tail(10)  

    # Create the graph
    fig = px.line(df, x="Time", y=["Celsius", "Fahrenheit"], 
                  labels={"value": "Temperature", "variable": "Scale"}, 
                  title="Temperature Over Time")
    fig.update_traces(mode="lines+markers")
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
