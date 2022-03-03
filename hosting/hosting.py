from flask import Flask, request, jsonify
import traceback
import pandas as pd
import joblib
from utils import CategoricalTransformer, NumericalTransformer

# Your API definition
app = Flask(__name__)


@app.route("/predict", methods=['GET', 'POST'])  # use decorator pattern for the route
def predict():
    if model:
        try:
            json_ = request.json
            print(json_)
            query = pd.DataFrame(json_).reindex(fill_value=0)
            print(query)
            # Fit your data on the scaler object
            # scaler = StandardScaler()
            # scaled_df = scaler.fit_transform(query)
            # query = pd.DataFrame(scaled_df, columns=model_columns)
            # print(query)
            transformed_query = pipeline.transform(query)

            prediction = list(model.predict(transformed_query))
            print({'prediction': str(prediction)})
            return jsonify({'prediction': str(prediction)})

        except:

            return jsonify({'trace': traceback.format_exc()})
    else:
        print('Train the model first')
        return ('No model here to use')



pipeline = joblib.load('data/experiment3/ex3_pipeline.pkl')
obj_model = joblib.load('ensemble/gbrt_clf.pkl')
model = obj_model

# model_columns = joblib.load('bicycle_columns.pkl')
app.run(port=12345, debug=True)
