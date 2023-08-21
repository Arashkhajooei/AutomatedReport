from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.express as px
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Load data and convert date columns to datetime
df = pd.read_csv('dataset_orders.csv')
df['create_time'] = pd.to_datetime(df['create_time'])
df['accept_time'] = pd.to_datetime(df['accept_time'])

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load templates
templates = Jinja2Templates(directory="templates")

# Define routes
@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    hourly_plot, daily_plot = create_plots()
    return templates.TemplateResponse("dashboard.html", {"request": request, "hourly_plot": hourly_plot, "daily_plot": daily_plot})

def create_plots():
    hourly_plot = create_hourly_plot()
    daily_plot = create_daily_plot()
    return hourly_plot.to_html(), daily_plot.to_html()

def create_hourly_plot():
    hourly_data = df[df['status'] == 'DELIVERED']
    hourly_data['hour'] = hourly_data['create_time'].dt.hour
    hourly_data = hourly_data.groupby(['hour'])['order_id'].count().reset_index()

    hourly_plot = px.line(hourly_data, x='hour', y='order_id', title='Hourly Trend of Delivered Orders')
    return hourly_plot

def create_daily_plot():
    daily_data = df[df['status'] == 'DELIVERED']
    daily_data['date'] = daily_data['create_time'].dt.date
    daily_data = daily_data.groupby(['date'])['order_id'].count().reset_index()

    daily_plot = px.line(daily_data, x='date', y='order_id', title='Daily Trend of Delivered Orders')
    return daily_plot

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
