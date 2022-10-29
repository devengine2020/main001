import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal
from scipy import signal
import csv
#バターワースフィルタ（ローパス）
def lowpass(x, samplerate, fp, fs, gpass, gstop):
    fn = samplerate / 2                           #ナイキスト周波数
    wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, "low")            #フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x)                  #信号に対してフィルタをかける
    return y                                      #フィルタ後の信号を返す

# データ読み込み
datafile='data.csv'
data=pd.read_csv(datafile).values
x_val=data[:,1]
y_val=data[:,2]

#フィルター処理開始

if 0:
    window=21
    deg=3
    smooth1=scipy.signal.savgol_filter(y_val, window, deg)
else:
    rpm = 2000
    samplerate = 1/(1/(rpm/60)/(360/0.05))
    print(samplerate)
    fp = 5000  # 通過域端周波数[Hz]
    fs = 8000  # 阻止域端周波数[Hz]
    gpass = 3  # 通過域端最大損失[dB]
    gstop = 40  # 阻止域端最小損失[dB]
    smooth1 = lowpass(y_val, samplerate, fp, fs, gpass, gstop)



max_index = np.where(y_val == y_val.max())[0][0]
index_st = np.where(x_val > -30)[0][0]
temp_min = 1e10
for i in reversed(range(max_index)):
    if i > index_st:
        if y_val[i] < temp_min:
            temp_min = y_val[i]

print(temp_min)

result = np.where(y_val == temp_min)[0][0]

print(result)

#グラフ作成
plt.plot(x_val, y_val)
plt.plot(x_val, smooth1)
plt.ylim(-40,100)
plt.show()
