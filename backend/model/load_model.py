import os
import tensorflow as tf
import lightgbm as lgb

# Define model paths
DNN_MODEL_PATH = os.path.join("model", "saved models", "dnn_ids_model_1.h5")
LGBM_MODEL_PATH = os.path.join("model", "saved models", "lgbm_ids_model_1.txt")

# Load the pretrained DNN model
def load_dnn_model():
    try:
        return tf.keras.models.load_model(DNN_MODEL_PATH)
    except Exception as e:
        print(f"❌ Error loading DNN model: {e}")
        return None

dnn_model = load_dnn_model()

# Load the pretrained LightGBM model
def load_lgbm_model():
    try:
        return lgb.Booster(model_file=LGBM_MODEL_PATH)
    except Exception as e:
        print(f"❌ Error loading LightGBM model: {e}")
        return None