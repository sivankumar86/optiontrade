

def hammer(changes):
    neg = [num for num in changes if num >= 0]
    return len(neg)

def findingwig(row):
    if row["open"] < row["ltp"]:
        row['bwigh'] = ((row["open"] - row["low"]))
        row['twigh'] = (row["high"] - row["ltp"])
    else:
        row['bwigh'] = ((row["ltp"] - row["low"]))
        row['twigh'] = (row["high"] - row["open"])
    row["hammer"]=round(row['twigh']) < 2 and row['bwigh'] > round(abs(3 * row['diff']))
    return row

def hammerPattern(dfp):
    dfp['bpc'] = dfp['diff'].rolling(5).apply(hammer)
    dfp= dfp.apply(findingwig, axis=1)
    return dfp

def shootingStar(dfp):
    dfp["shotingstar"]= dfp.apply(lambda row : row['bwigh'] <2 and row['twigh'] > round(abs(3 * row['diff'])) , axis=1)
    return dfp

def piercing(dfp):
    dfp['yc'] = dfp['ltp'].shift(1)
    dfp['yo'] = dfp['open'].shift(1)
    dfp["piercing"] = dfp.apply(
        lambda row: (3* row['twigh']) < row['diff'] and row['yc'] < row['yo'] and row['yc'] > row['open'] and  row['ltp'] >row['yc'] , axis=1)
    return dfp
