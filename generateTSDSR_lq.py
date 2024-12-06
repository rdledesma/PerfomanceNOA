import pandas as pd

d = pd.concat([ pd.read_csv('DSR/LQ/lq_2020.csv'),
               pd.read_csv('DSR/LQ/lq_2021.csv')])


d.to_csv('DSR/LQ/lq_60.csv', index=False)
