from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np
import plotly.express as px

app = FastAPI()

# Provided function to get bar colors based on data changes
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

# Provided function to generate a Plotly bar chart
def generate_plot(data, title):
    colors = get_item_color(data)  # Get colors for each bar
    fig = px.bar(
        x=[f"Q{i+1}" for i in range(len(data))],  # Labels for the x-axis
        y=data,  # Data for the y-axis
        title=title
    )
    # Update the bar colors
    fig.update_traces(marker_color=colors)
    return fig.to_html(full_html=False)

@app.get("/", response_class=HTMLResponse)
async def root():
    # Generate random data with specific conditions for the last 10 values
    np.random.seed(42)  # For reproducibility
    # First 59 values: random between 0 and 100
    data = np.random.randint(0, 101, size=59).tolist()
    
    # Last 10 values: ensure green (positive change) or orange (-7% to 0% change)
    last_value = data[-1] if data else 50  # Start with the last of the first 59 or a default
    for _ in range(10):
        # Calculate a new value that ensures green or orange
        # Green: new_value > last_value
        # Orange: last_value * 0.93 <= new_value <= last_value
        if np.random.choice([True, False]):  # Randomly choose green or orange
            # Green: increase by at least 1
            new_value = np.random.randint(last_value + 1, min(last_value + 20, 101))
        else:
            # Orange: between 93% and 100% of last_value
            min_val = int(last_value * 0.93)
            new_value = np.random.randint(max(min_val, 0), last_value + 1)
        data.append(new_value)
        last_value = new_value

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['Value'])

    # Generate the plot
    plot_html = generate_plot(data, "Random Data Bar Chart (Last 10 Green or Orange)")

    # Create HTML response with the DataFrame and the plot
    html_content = f"""
    <html>
        <head>
            <title>Random Data Visualization</title>
        </head>
        <body>
            <h1>DataFrame with Random Values</h1>
            {df.to_html()}
            <h1>Bar Chart</h1>
            {plot_html}
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
