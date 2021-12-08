import pandas as pd


file_path=open("/home/zephyn/Groceries_dataset.csv") #use your file_path
data=pd.read_csv(file_path)

data=data.groupby(['Member_number','Date'])['itemDescription'].apply(lambda x: list(x))

transactions = data.values.tolist()

print(data.head(10))
print('\ndata shape:\n',data.shape)
print('\napriori takes list as an input:\n',transactions[:10])

