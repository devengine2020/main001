import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal
import csv
import math


x_min = -40
x_max = 20
x_interval = 0.05
x_val = np.arange(x_min, x_max, x_interval)
# 関数f(x)を格納する配列
y_val = []

offset_x = 3
abs_x = 1/5
# それぞれ配列に格納していく(便宜上、nは0.1間隔でセット)
for i in range(len(x_val)):
    y_val.append(-0.2*(abs_x*x_val[i]+offset_x) ** 4 + 0.3*(abs_x*x_val[i]+offset_x) ** 3 + 5*(abs_x*x_val[i]+offset_x) ** 2 + 5 * (abs_x*x_val[i]+offset_x) - 10)


X_SAMPLE = len(y_val)
print(X_SAMPLE)
WAVE_SMP_TIME = 1/(2000/60)/(360/x_interval)
print(WAVE_SMP_TIME)
# noise_1
noize_f = 6000
NOISE_1_INT = (1/noize_f)/WAVE_SMP_TIME
NOISE_1_INT_OFF = -20
AMP_NOISE_1 = 10
SIGMA_NOISE_1 = 5
noise1_int = 1/noize_f
noise1_freq = np.round(1 / noise1_int, 1)

xx = [ i for i in range(X_SAMPLE)]

noise_1=[]
cnt_1=0
for i in range(len(xx)):
    if i % NOISE_1_INT == 0:
        cnt_1+=1
    noise_peak_time = NOISE_1_INT* cnt_1 + NOISE_1_INT_OFF
    noise_1.append(AMP_NOISE_1*math.exp(-((i- noise_peak_time)**2 )/(2*SIGMA_NOISE_1**2)))



y_val = [x + y for (x, y) in zip(y_val, noise_1)]

df = pd.DataFrame( x_val, columns=['x'] )
df['y'] = y_val
df.to_csv("data.csv")



#グラフ作成
plt.plot(x_val, y_val)
plt.ylim(-40,100)
plt.show()

