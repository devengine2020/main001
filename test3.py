import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datafile='data.csv'
data=pd.read_csv(datafile).values
t=data[:,1]
f=data[:,2]

N = len(f) # サンプル数
dt = 1/(2000/60)/(360/0.05)# サンプリング周期(sec)
print(N)
print(dt)

# 高速フーリエ変換(FFT)
F = np.fft.fft(f)

# FFTの複素数結果を絶対値に変換
F_abs = np.abs(F)
# 振幅をもとの信号に揃える
F_abs_amp = F_abs / N * 2 # 交流成分はデータ数で割って2倍
F_abs_amp[0] = F_abs_amp[0] / 2 # 直流成分（今回は扱わないけど）は2倍不要

# 周波数軸のデータ作成
fq = np.linspace(0, 1.0/dt, N) # 周波数軸　linspace(開始,終了,分割数)

# グラフ表示（FFT解析結果）
plt.xlabel('freqency(Hz)', fontsize=14)
plt.ylabel('amplitude', fontsize=14)
plt.plot(fq, F_abs_amp)
plt.xlim(0,10000)
plt.show()

# そのまま普通にIFFTで逆変換した場合
F_ifft = np.fft.ifft(F) # IFFT
F_ifft_real = F_ifft.real # 実数部
plt.plot(t, F_ifft_real, c="g") # グラフ
plt.show()