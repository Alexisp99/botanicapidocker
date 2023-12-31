# 1. Library imports
import uvicorn
from fastapi import FastAPI
from model import IrisModel, IrisSpecies, bddinputs
from typing import Optional, List
from dotenv import load_dotenv
import pymysql
import os
from urllib.parse import urlparse

# 2. Create app and model objects
app = FastAPI()
model = IrisModel()


def connect():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    # Parse the database URL
    url_components = urlparse(database_url)
    db_host = url_components.hostname
    db_user = url_components.username
    db_password = url_components.password
    db_name = url_components.path[1:]  

    # Configurer la connexion à la base de données MySQL
    conn = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return conn

# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted flower species with the confidence
@app.post('/predict')  # Changed from GET to POST
def predict_species(iris: Optional[IrisSpecies] = None):
    if iris is None:
        return {"message": "No input data provided"}
    
    # data = iris.dict()
    data = iris.model_dump()
    prediction, probability = model.predict_species(
        data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width']
    )
    return {
        'prediction': prediction,
        'probability': probability
    }
    
    
@app.get('/getpredict')
def predict_species(sepal_length: Optional[float] = None, sepal_width: Optional[float] = None,
                    petal_length: Optional[float] = None, petal_width: Optional[float] = None):
    if sepal_length is None or sepal_width is None or petal_length is None or petal_width is None:
        return {"message": "Insufficient data provided"}
    prediction, probability = model.predict_species(sepal_length, sepal_width, petal_length, petal_width)
    return {
        'prediction': prediction,
        'probability': probability
    }


#BDD
@app.get("/")
async def get_items() -> List[bddinputs]:
    # Effectuer des opérations sur la base de données
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM train_table")
        results = cursor.fetchall()

    # Convertir les résultats en une liste d'objets Test a refacto par la suite
    items = []
    for row in results:
        data_dict = {
            "input": row[0],
            "prediction" : row[1],
            "probability" : row[2],
            "istrue" : row[3],
        }

        data_user = bddinputs(**data_dict)
        items.append(data_user)

    # Retourner les résultats de l'API
    return items

@app.post("/add")
async def create_item(item: bddinputs):
    # Effectuer des opérations sur la base de données
    conn = connect()
    with conn.cursor() as cursor:
        query = "INSERT INTO train_table (input, prediction, probability, istrue) " \
                 "VALUES (%s, %s, %s, %s)"
        values = (item.input, item.prediction, item.probability, item.istrue)
        cursor.execute(query, values)
        conn.commit()

    return {"message": "Item created successfully"}


@app.delete("/del")
async def delete_item():
    # Effectuer des opérations sur la base de données
    conn = connect()
    with conn.cursor() as cursor:
        query = "DELETE FROM train_table"
        cursor.execute(query)
        conn.commit()

    return {"message": "Items deleted successfully"}


# # 4. Run the API with uvicorn
# #    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, reload = True)