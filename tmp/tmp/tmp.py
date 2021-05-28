import math

import numpy as np
import pandas as pd


if __name__ == '__main__':
    tmp = pd.read_csv('../../data/tmp/chessboard_tmp.csv', header=None)
    res = pd.read_csv('../../data/tmp/Results.csv')

    r = np.array([['n', 'BX', 'BY']])

    for i in range(15):
        for j in range(21):
            index = tmp.iloc[j, i]
            if not math.isnan(index):
                r = np.append(r, np.expand_dims(res.iloc[int(index-1), 0:3].values, 0), axis=0)

    columns = r[0, :]
    df = pd.DataFrame(r[1:, :], columns=columns, dtype=int)
    df.to_csv('../../data/res.csv', index=False)

    print(0)
