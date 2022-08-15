import pandas as pd

df = pd.read_csv('movies.csv')

#drop unwanted columns
df.drop(['Votes','Rating(10)','Year','Timing(min)','Genre','Language'], axis=1, inplace=True) 

df = df[df['ID'] != '-'] #drop row if ID is '-'
df.drop_duplicates(inplace=True) #drop duplicates
df.reset_index(drop=True, inplace=True) #reset index

df.to_csv('metadata.csv', index=False) #save to csv
