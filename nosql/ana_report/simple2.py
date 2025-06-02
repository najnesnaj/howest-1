from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import numpy as np
import plotly.graph_objects as go
import json

app = FastAPI()

# Function to assign colors based on value differences
def get_item_color(data):
    colors = ["blue"]  # First value default
    for i in range(1, len(data)):
        diff = data[i] - data[i - 1]
        if diff > 0:
            colors.append("green")
        elif -7 <= diff <= 0:
            colors.append("orange")
        else:
            colors.append("red")
    return colors

# Generate random data between 1 and 100
def generate_random_data(n=69):
    return np.random.randint(1, 101, size=n).tolist()

# Convert data and colors to Plotly chart JSON
def generate_plot_json(data):
    colors = get_item_color(data)
    fig = go.Figure(
        data=[
            go.Bar(
                x=[f"Q{i+1}" for i in range(len(data))],
                y=data,
                marker_color=colors
            )
        ]
    )
    fig.update_layout(title="Random Data Bar Chart (Color Based on Value Change)")
    return json.loads(fig.to_json())

@app.get("/plot-data", response_class=JSONResponse)
async def get_plot_data():
    data = generate_random_data()
    return generate_plot_json(data)

@app.get("/", response_class=HTMLResponse)
async def root():
    data = generate_random_data()
    plot_json = json.dumps(generate_plot_json(data))

    html_content = f"""
    <html>
        <head>
            <title>Random Data Bar Chart</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                #plot {{ width: 100%; height: 600px; }}
                button {{ padding: 10px 20px; font-size: 16px; cursor: pointer; }}
            </style>
        </head>
        <body>
            <h1>Random Data Bar Chart</h1>
            <button onclick="regeneratePlot()">Regenerate Plot</button>
            <div id="plot"></div>
            <script>
                const initialData = {plot_json};
                Plotly.newPlot('plot', initialData.data, initialData.layout);

                async function regeneratePlot() {{
                    try {{
                        const response = await fetch('/plot-data');
                        const newData = await response.json();
                        Plotly.react('plot', newData.data, newData.layout);
                    }} catch (error) {{
                        console.error('Error regenerating plot:', error);
                    }}
                }}
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

