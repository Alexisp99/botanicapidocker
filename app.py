# 1. Library imports
import uvicorn
from fastapi import FastAPI
from typing import Optional
from model import IrisModel, IrisSpecies

# 2. Create app and model objects
app = FastAPI()
model = IrisModel()

# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted flower species with the confidence
@app.post('/predict')  # Changed from GET to POST
def predict_species(iris: Optional[IrisSpecies] = None):
    if iris is None:
        return {"message": "No input data provided"}
    data = iris.dict()
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


# # 4. Run the API with uvicorn
# #    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, reload = True)
