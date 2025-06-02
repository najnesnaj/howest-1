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
    
    # Initialize data with first value between 1 and 100
    data = [np.random.randint(1, 101)]
    
    # Generate first 64 values with [-14, 14] interval constraint
    for i in range(64):  # Generate up to index 64 (65 values total)
        last_value = data[-1]
        # Calculate bounds: ±14 units from last_value, capped at 1 and 100
        min_val = max(1, last_value - 14)
        max_val = min(100, last_value + 14)
        new_value = np.random.randint(min_val, max_val + 1)
        data.append(new_value)
    
    # Randomly select a starting index for the 5 consecutive red/orange bars
    start_idx = np.random.randint(0, 65)  # 0 to 64 to fit 5 bars within 69
    
    # Generate remaining values, applying red/orange constraints for the 5 consecutive bars
    for i in range(65, 69):  # Generate indices 65 to 68
        last_value = data[i - 1]
        # Calculate ±14 bounds
        min_val_14 = max(1, last_value - 14)
        max_val_14 = min(100, last_value + 14)
        
        if start_idx <= i < start_idx + 5:  # In the 5 consecutive red/orange bars
            if np.random.choice([True, False], p=[0.5, 0.5]):  # Red: 50% chance
                # Red: new_value < last_value * 0.93 for < -7% change, non-zero
                max_val_red = int(last_value * 0.93)
                max_val = min(max_val_red, max_val_14)  # Respect -7% and ±14
                new_value = np.random.randint(max(1, last_value - 14), max_val) if max_val > 1 else 1
            else:  # Orange: 50% chance
                # Orange: last_value * 0.93 <= new_value <= last_value
                min_val_orange = max(1, int(last_value * 0.93))
                max_val = min(last_value, max_val_14)  # Respect last_value and ±14
                new_value = np.random.randint(max(min_val_orange, min_val_14), max_val + 1) if min_val_orange <= max_val else last_value
        else:  # Outside the 5 consecutive bars
            new_value = np.random.randint(min_val_14, max_val_14 + 1)
        
        data.append(new_value)
    
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
    fig.update_layout(title="Random Data Bar Chart (5 Consecutive Red or Orange, Non-Zero, [-14, 14] Interval)")
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
                #plot {{ width: 100%; height: 600px; }}
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
                        console.log('Last 5 values (for reference):', newData.data[0].y.slice(-5));
                        console.log('Consecutive red/orange bars start at Q' + ({start_idx} + 1));
                        // Log absolute differences to verify [-14, 14] interval
                        const y = newData.data[0].y;
                        const diffs = y.slice(1).map((val, i) => val - y[i]).map(d => d.toFixed(1));
                        console.log('Absolute differences:', diffs);
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
