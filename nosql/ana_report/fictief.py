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
    # Generate random data
    np.random.seed(42)  # For reproducibility
    data = np.random.randint(0, 101, size=69)  # 69 random values between 0 and 100
    df = pd.DataFrame(data, columns=['Value'])

    # Generate the plot
    plot_html = generate_plot(data, "Random Data Bar Chart")

    # Create HTML response with the DataFrame and the plot
    html_content = f"""
    <html>
        <head>
            <title>Random Data Visualization</title>
        </head>
        <body>
#            <h1>DataFrame with Random Values</h1>
#            {df.to_html()}
            <h1>Bar Chart</h1>
            {plot_html}
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
