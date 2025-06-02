from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import numpy as np
import plotly.graph_objects as go
import json

app = FastAPI()

# Simplified function to assign colors
def get_item_color(data):
    return ['green' if value >= 50 else 'red' for value in data]

# Generate simple random data
def generate_random_data():
    np.random.seed()  # Ensure different random output each time
    data = list(np.random.randint(1, 101, size=69))  # 69 random values between 1 and 100
    return data

# Generate Plotly chart as JSON
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
    fig.update_layout(title="Random Data Bar Chart")
    return json.loads(fig.to_json())

# API endpoint for JSON data
@app.get("/plot-data", response_class=JSONResponse)
async def get_plot_data():
    data = generate_random_data()
    return generate_plot_json(data)

# HTML page with embedded Plotly chart
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
                        console.error('Error updating plot:', error);
                    }}
                }}
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Run the app (for standalone execution)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

