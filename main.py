from fastapi import FastAPI, Query, HTTPException
import pandas as pd
import os

app = FastAPI(title="Airline Delay Prediction API")

DATA_PATH = "/app/data/T_ONTIME_REPORTING.csv"

@app.on_event("startup")
def load_data():
    global df
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        df = pd.DataFrame()

@app.get("/")
def root():
    return {"message": "API is functional"}

@app.get("/predict/delays")
def predict_delays(
    arrival_airport: str = Query(..., description="Arrival airport code (e.g., LAX)"),
    departure_airport: str = Query(..., description="Departure airport code (e.g., ATL)"),
    departure_time_local: str = Query(..., description="Local departure time (ISO string)"),
    arrival_time_local: str = Query(..., description="Local arrival time (ISO string)")
):
    if df.empty:
        raise HTTPException(status_code=500, detail="Data not loaded")

    # filter by route
    route_data = df[(df["ORIGIN"] == departure_airport) & (df["DEST"] == arrival_airport)]
    if route_data.empty:
        raise HTTPException(status_code=404, detail="Route not found in dataset")

    avg_delay = route_data["DEP_DELAY"].mean()

    return {
        "departure_airport": departure_airport,
        "arrival_airport": arrival_airport,
        "average_departure_delay_min": round(float(avg_delay), 2),
    }