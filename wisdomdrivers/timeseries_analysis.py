# views.py
from rest_pandas import PandasSimpleView
import pandas as pd

class TimeSeriesView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        return pd.read_csv('data.csv')
