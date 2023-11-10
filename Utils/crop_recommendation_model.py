import pandas as pd
import pickle
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold, cross_val_score
from sklearn.calibration import CalibratedClassifierCV

from sklearn.ensemble import RandomForestClassifier


class AI_models :
    def __init__(self, *args, **kwargs) :
        self.dataset = "Utils/Crop_recommendation.csv"
        self.ordered_set = ["N", "temperature", "humidity", "rainfall", "P", "K", "ph"]
    
    
    def data_preprocessing(self) :
        # Inititalize the dataframe
        self.df = pd.read_csv(self.dataset)

        # Change the column values as necessary
        # Phosophorous
        p_levels = ["L" if i<=48.33 else "M" if i>48.33 and i<=96.66 else "H" for i in self.df.P]
        self.df["P"] = pd.Series(p_levels)
        # Acidity
        ph_levels = ["SA" if i<=5.633 else "MA" if i>5.633 and i<=7.766 else "N" for i in self.df.ph]
        self.df["ph"] = pd.Series(ph_levels)
        # Pottassium
        k_levels = ["L" if i<=68.33 else "M" if i>68.33 and i<=136.66 else "H" for i in self.df.K]
        self.df["K"] = pd.Series(k_levels)
        
        # Defining the Attribute and feature set and encoding
        e_df, Y = self.data_encoding()
        X = e_df.drop(columns=["label"])
        
        # Return the training and testing sets
        train_x, train_y, test_x, test_y = train_test_split(X, Y, test_size=0.33)
        return train_x, train_y, test_x, test_y, X, Y
    
    
    def data_encoding(self, label=True) :
        # Encoding the attribute values
        e_df = pd.get_dummies(self.df, columns=["P", "K", "ph"])
        # print(f"e_df: {e_df}")
        if label :
            Y = self.df["label"]
            # Label encoding Y
            le = LabelEncoder()
            le.fit(Y.unique())
            Y = le.transform(Y)
            
            # Dump the label encoder
            with open("binary_files/label_encoder.pkl", "wb") as l_file :
                pickle.dump(le, l_file)
        else :
            Y = None
        
        return e_df, Y
    
    
    def train_crop_recommendation_model(self) :
        # Get the preprocessed datasets
        train_x, test_x, train_y, test_y, X, Y = self.data_preprocessing()
        
        # model training
        model = RandomForestClassifier()
        model.fit(train_x, train_y)
        
        # Prediction and accuracy
        predictions = model.predict(test_x)
        accuracy_score(predictions, test_y)
        
        # K-fold cross validation
        kfold = KFold(n_splits=5, shuffle=True, random_state=42)
        scores = cross_val_score(model, X, Y, cv=kfold)
        print("Random Forest Classifier:")
        print(f"The Scores are: {scores}")
        print(f"The avg score is: {round(scores.mean()*100, 4)}\n")
        
        # Dump the model into a .pkl file
        with open("binary_files/random_forest_model.pkl", "wb") as m_file :
            pickle.dump(model, m_file)
            
    
    def predict_crops_in_order(self, data) :
        # Get the preprocessed datasets
        train_x, test_x, train_y, test_y, X, Y = self.data_preprocessing()

        # Load the model
        with open("binary_files/random_forest_model.pkl", "rb") as m_file :
            model = pickle.load(m_file)
        
        # Load the label encoder
        with open("binary_files/label_encoder.pkl", "rb") as l_file :
            le = pickle.load(l_file)
        
        # Curate the data to pass into the model
        l = []
        s = {"P_H": [1, 0, 0], "P_L": [0, 1, 0], "P_M": [0, 0, 1], "K_H": [1, 0, 0], "P_L": [0, 1, 0], "K_M": [0, 0, 1], "ph_MA": [1, 0, 0], "ph_N": [0, 1, 0], "ph_SA": [0, 0, 1]}
        for i in self.ordered_set :
            if f"{i}_{data[i]}" not in s :
                l.append(data[i])
            else :
                l.extend(s[f"{i}_{data[i]}"])
        # print(f"l: {l}")
        # self.df = pd.Series(l, index=self.ordered_set)
        
        # print(f"self.df: {self.df}")
        # e_df, _ = self.data_encoding(label=False)
        
        # Define and fit calibration model
        calibrated = CalibratedClassifierCV(model, method='sigmoid', cv=5)
        calibrated.fit(train_x, train_y)
        
        # Prediction
        # print(f"\n{e_df}\n")
        predicted_proba = calibrated.predict_proba([l])
        
        a = list(zip(predicted_proba[0,:], list(le.inverse_transform(calibrated.classes_))))
        a = sorted(a, key=lambda x:x[0], reverse=True)
        ranked = [i[1] for i in a]
        
        return ranked[1:5]
    
if __name__ == "__main__" :
    ai = AI_models()
    ai.train_crop_recommendation_model()