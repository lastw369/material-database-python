import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline
import sqlite3


# object = Database("/Users/mac/Desktop/crystal.db")
conn = sqlite3.connect("/Users/mac/Desktop/crystal.db")
cnn = conn.cursor()
cnn.execute("SELECT * FROM {}".format('AgO_IV'))
iv_points = []
x_lst = []
y_lst = []
for coordinate in cnn.fetchall():
    iv_points.append(tuple([coordinate[1], coordinate[2]]))
for p in iv_points:
    x_lst.append(p[0])
    y_lst.append(p[1])
conn.close()
x_array = np.array(x_lst)
y_array = np.array(y_lst)
x_new = np.linspace(x_array.min(), x_array.max(), 300)
y_smooth = spline(x_array, y_array, x_new)
plt.xlabel("V")
plt.ylabel("I")
plt.plot(x_new, y_smooth)
plt.show()

