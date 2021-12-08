import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

##-------------------------------------------
##Read the data and view the data characteristics
file_path=open("/home/zephyn/Groceries_dataset.csv") #use your file_path
data=pd.read_csv(file_path)

data.info()

des=pd.DataFrame(data.describe()).T 
print(des)
print('---------------------------<raw data>---------------------------------')
print(data.head(5))

##--------------------------------------------
data['Date'] = pd.to_datetime(data['Date'])
data['date'] = data['Date'].dt.date

data['month'] = data['Date'].dt.month
data['month'] = data['month'].replace((1,2,3,4,5,6,7,8,9,10,11,12),('January','February','March','April','May','June','July','August','September','October','November','December'))

data['weekday'] = data['Date'].dt.weekday
data['weekday'] = data['weekday'].replace((0,1,2,3,4,5,6),('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'))
data['itemDescription'] = data['itemDescription'].str.strip()
data['itemDescription'] = data['itemDescription'].str.lower()

print('----------------------<Simple processed data>----------------------------')
print(data.head(10))

##---------------------------------------------
##data analsysis
#Top items purchased by members
plt.figure(figsize=(25,10))

sns.lineplot(x = data.itemDescription.value_counts().head(25).index, y = data.itemDescription.value_counts().head(25).values)

plt.xlabel('Items', size = 15)
plt.xticks(rotation=45)
plt.ylabel('Count of Items', size = 15)
plt.title('Top items purchased by members', color = 'green', size = 15)
plt.show()

#Items bought split by month
months = data.groupby('month')['Member_number'].count()

pie, ax = plt.subplots(figsize=[10,6])
plt.pie(x=months, autopct="%.1f%%", explode=[0.05]*12, labels=months.keys(), pctdistance=0.5)
plt.title("Items bought split by month", fontsize=14)
plt.show()

##Number of orders received each day
days = data.groupby('weekday')['Member_number'].count()
plt.figure(figsize=(12,5))
sns.barplot(x=days.keys(), y=days)
plt.xlabel('Week Day', size = 15)
plt.ylabel('Orders per day', size = 15)
plt.title('Number of orders received each day', color = 'blue', size = 15)
plt.show()


