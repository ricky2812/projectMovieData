import pandas as pd

def rectify():
    dat = pd.read_csv('imdb_data.csv')
    print(dat.shape)
    dat = dat.drop_duplicates(subset=['ID'], keep='first')
    print(dat.shape)
    dat.to_csv('imdb_data.csv', index=False)
    
    meta = pd.read_csv('metadata.csv')
    print(meta.shape)
    meta = meta[~meta['ID'].isin(dat['ID'])]
    print(meta.shape)
    meta.to_csv('metadata.csv', index=False)

if __name__ == '__main__':
    rectify()