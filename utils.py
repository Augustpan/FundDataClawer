import numpy as np
import pandas

def dateToQuarter(col):
    def proc(x):
        sp = x.split("-")
        year = sp[0]
        quarter_map = {"01":1, "02":1, "03":1, 
                       "04":2, "05":2, "06":2,
                       "07":3, "08":3, "09":3,
                       "10":4, "11":4, "12":4}
        quarter = "{}-{}".format(year, quarter_map[sp[1]])
        return quarter
    return list(map(proc, col))

