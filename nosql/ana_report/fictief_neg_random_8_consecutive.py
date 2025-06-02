from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import numpy as np
import plotly.graph_objects as go
import json

app = FastAPI()

# Function to get bar colors based on data changes
def get_item_color(data):
    colors = []
    for i in range(len(data)):
        if i == 0:  # No previous value for the first item
            colors.append('blue')  # Default color for the first item
        else:
            if data[i - 1] == 0:
                change = 0
            else:
                change = (data[i] - data[i - 1]) / data[i - 1] * 100  # Percentage change
            if data[i] < 0:
                change = -100  # Negative change
            if change > 0:
                colors.append('green')  # Positive change
            elif -7 <= change <= 0:
                colors.append('orange')  # Small negative or no change
            elif change < -7:
                colors.append('red')  # Large negative change
    return colors

# Function to generate random data
def generate_random_data():
    np.random.seed()  # Remove seed for true randomness
    # Initialize 69 random values between 0 and 100
    data = np.random.randint(0, 101, size=69).tolist()
    
    # Randomly select a starting index for the 8 consecutive red/orange bars
    start_idx = np.random.randint(0, 62)  # 0 to 61 to fit 8 bars within 69
    
    # Ensure the 8 consecutive bars (start_idx to start_idx+7) are red or orange, non-zero
    last_value = data[start_idx - 1] if start_idx > 0 else 50  # Use previous value or default
    for i in range(start_idx, start_idx + 8):
        if np.random.choice([True, False], p=[0.5, 0.5]):  # Red: 50% chance
            # Ensure new_value < last_value * 0.93 for < -7% change, and >= 1
            max_val = int(last_value * 0.93)
            new_value = np.random.randint(1, max_val) if max_val > 1 else 1
        else:  # Orange: 50% chance
            min_val = int(last_value * 0.93)
            new_value = np.random.randint(max(min_val, 1), last_value + 1)
        data[i] = new_value
        last_value = new_value
    
    return data, start_idx  # Return start_idx for debugging

# Function to generate Plotly chart JSON
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
    fig.update_layout(title="Random Data Bar Chart (8 Consecutive Red or Orange, Non-Zero)")
    return json.loads(fig.to_json())

@app.get("/plot-data", response_class=JSONResponse)
async def get_plot_data():
    data, start_idx = generate_random_data()
    return generate_plot_json(data)

@app.get("/", response_class=HTMLResponse)
async def root():
    # Initial plot data
    data, start_idx = generate_random_data()
    plot_json = json.dumps(generate_plot_json(data))
    
    # HTML with a button to regenerate the plot
    html_content = f"""
    <html>
        <head>
            <title>Random Data Bar Chart</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                #plot {{ width: 100%; height: 500px; }}
                button {{ padding: 10px 20px; font-size: 16px; cursor: pointer; }}
            </style>
        </head>
        <body>
            <h1>Random Data Bar Chart</h1>
            <button onclick="regeneratePlot()">Regenerate Plot</button>
            <div id="plot"></div>
            <script>
                // Initial plot
                const initialData = {plot_json};
                Plotly.newPlot('plot', initialData.data, initialData.layout);

                async function regeneratePlot() {{
                    try {{
                        console.log('Fetching new plot data...');
                        const response = await fetch('/plot-data');
                        if (!response.ok) {{
                            console.error('Failed to fetch new plot data:', response.status, response.statusText);
                            return;
                        }}
                        const newData = await response.json();
                        console.log('Received new plot data:', newData);
                        console.log('Last 8 values (for reference):', newData.data[0].y.slice(-8));
                        console.log('Consecutive red/orange bars start at Q' + ({start_idx} + 1));
                        Plotly.react('plot', newData.data, newData.layout);
                        console.log('Plot updated successfully');
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
