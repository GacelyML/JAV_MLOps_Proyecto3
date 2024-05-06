from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os


import mlflow
from typing import List, Optional
import pandas as pd

### Llamar a partir de mlflow, el URI del modelo puesto en producción. 
# set minio environment variables
os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://10.43.101.154:8081"
os.environ['AWS_ACCESS_KEY_ID'] = 'minio_user'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minio_pwd'

# connect to mlflow
# mlflow.set_tracking_uri("http://10.43.101.154:8083")

model_name = "final_model"

# logged_model = 'runs:/71428bebed2b4feb9635714ea3cdb562/model'
model_production_uri = "models:/{model_name}/production".format(model_name=model_name)

### Inicializar FASTAPI
app = FastAPI()

### JSON que define mis variables de entrada de la API. 
class model_input(BaseModel):
    Elevation :  int
    Aspect : int
    Slope : int
    Horizontal_Distance_To_Hydrology : int
    Vertical_Distance_To_Hydrology : int
    Horizontal_Distance_To_Roadways : int
    Hillshade_9am : int
    Hillshade_Noon : int
    Hillshade_3pm : int
    Horizontal_Distance_To_Fire_Points : int
    Wilderness_Area : str
    Soil_Type : str

# Función Predict que se encarga de ejecutar el predict sobre el modelo generado y retorna una predicción. 
# OJO: tener en cuenta hacer alguna especie de try except que muestre los errores presentes sobre la API. 
@app.post("/predict/")
def predict(item:model_input):

    # global loaded_model
    # Load model as a PyFuncModel.
    try:

       # loaded_model = mlflow.pyfunc.load_model(model_uri=model_production_uri)

        data_dict = item.dict()
        model_info = data_dict.pop('model', None)
        
        # Predice con respecto al modelo que se le especifique. 
        X = pd.DataFrame({key: value for key, value in data_dict.items()})

        categorical_variables = ['Wilderness_Area', 'Soil_Type']
        numerical_variables = [feature for feature in X.columns if feature not in categorical_variables]
        
        prediction = loaded_model.predict(X.iloc[0].to_frame().T)

        return prediction
    except Exception as e: 
        return f"Ocurrió un error: {e} "
