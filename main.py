from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()

# Load the CSV data into a pandas DataFrame
data = pd.read_csv('preprocessed_data.csv')  # Replace with your dataset file path

@app.get("/")
def read_root():
    return {"message": "Welcome to the dashboard API!"}

sample_data = data.head(1000)

@app.get("/charts", response_class=HTMLResponse)
def generate_charts():
    print("Generating chart...")
    # Generate a sample chart using matplotlib
    plt.plot(sample_data['create_time'], sample_data['price'])
    plt.xlabel('Create Time')
    plt.ylabel('Price')

    # Save the chart as a PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the image to base64 for embedding in the HTML response
    chart_img = base64.b64encode(buffer.read()).decode()

    # Create an HTML page with the embedded image
    html_content = f"""
    <html>
    <body>
        <h2>Chart</h2>
        <img src="data:image/png;base64,{chart_img}" alt="Chart">
    </body>
    </html>
    """

    return html_content

# Add a new route to serve the index.html file
@app.get("/dashboard", response_class=HTMLResponse)
def show_dashboard():
    with open("index.html", "r") as file:
        content = file.read()
    return content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
