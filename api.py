from fastapi import FastAPI
import joblib
import pandas as pd
import mysql.connector

app = FastAPI()

# ML model
model = joblib.load("mymodel.pkl")


# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=" ",
        database="ml_api"
    )


# Test API
@app.get("/")
def testing():
    return {"test": "all ok"}


# Prediction + MySQL storage
@app.post("/prediction")
def my_prediction(hours: float):

    # Prediction
    newdata = pd.DataFrame({
        "StudyHours": [hours]
    })

    result = model.predict(newdata)
    prediction = float(result[0])

    # Store in MySQL
    db = get_db_connection()
    cursor = db.cursor()

    query = """
        INSERT INTO predictions (study_hours, prediction)
        VALUES (%s, %s)
    """

    cursor.execute(query, (hours, prediction))

    db.commit()

    cursor.close()
    db.close()

    return {
        "study_hours": hours,
        "prediction": prediction,
        "message": "Prediction stored successfully"
    }


# Get prediction list
@app.get("/predictions")
def get_predictions():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, study_hours, prediction, created_at
        FROM predictions
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return {
        "predictions": data
    }