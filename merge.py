import pandas as pd


file1 = pd.read_csv('imdb_data.csv')
file2 = pd.read_csv('imdb_data2.csv')
print(file1.shape)
print(file2.shape) 
# source1 = pd.read_csv('metadata.csv')
# source2 = pd.read_csv('metadata3.csv')
# print(source1.shape)
# print(source2.shape)
#merge the two files
concat = pd.concat([file1,file2])
# concat = pd.concat([source1, source2])
print(concat.shape)
concat.to_csv('imdb_data_merged.csv', index=False)
# concat.to_csv('imdb_data_merged.csv', index=False)