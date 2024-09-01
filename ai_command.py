import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error
import random as rd
import pandas as pd
from sklearn.impute import SimpleImputer
import numpy as np



class model():
    def __init__(self,train_data:pd.DataFrame,n_estimators:int,finding_col:str,train_ratio:int=0.5):
        self.train_data = train_data
        self.finding_col = finding_col
        y = train_data.loc[:,finding_col]
        X = train_data.drop(finding_col,axis=1)
        self.train_X_1,self.valid_X_1,self.train_y_1,self.valid_y_1 = train_test_split(X,y,train_size=train_ratio,)

        imputer = SimpleImputer(strategy='mean')
        self.train_X = pd.DataFrame(imputer.fit_transform(self.train_X_1))
        self.valid_X = pd.DataFrame(imputer.transform(self.valid_X_1))
        self.train_X.columns = self.train_X_1.columns
        self.valid_X.columns = self.valid_X_1.columns

        imputer2 = SimpleImputer(strategy='mean')
        self.train_y = pd.DataFrame(imputer2.fit_transform(np.array(self.train_y_1).reshape(-1, 1)))
        self.valid_y = pd.DataFrame(imputer2.transform(np.array(self.valid_y_1).reshape(-1, 1)))
        self.train_y.columns = [finding_col]
        self.valid_y.columns = [finding_col]

        self.model = RandomForestRegressor(n_estimators=n_estimators)
        self.model.fit(self.train_X,self.train_y.values.ravel())

    def find(self,val:str):
        cols = self.train_X.columns
        values = val.split(",")
        values = [int(i) for i in values]
        val_dic = { i:[j] for i,j in zip(cols,values) }
        return self.model.predict(pd.DataFrame(val_dic))
        
    def get_mpae(self):
        self.preds = self.model.predict(self.valid_X)
        return mean_absolute_percentage_error(self.preds,self.valid_y)

    def save_model(self,filepath:str):
        joblib.dump(self.model,filepath)

def load_model(filepath:str):
    model =  joblib.load(filepath)
    return model


if __name__ == '__main__':
    a = model(pd.DataFrame({'a':[1,2,3,5],'b':[4,5,6,5],'c':[7,8,9,5]}),100,'c')
    val = a.find('1,4')
    print(val)
