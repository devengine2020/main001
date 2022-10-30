# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate
from matplotlib.colors import Normalize

import datetime

now = datetime.datetime.now()
now = now.strftime("%y%m%d")


def plot_func(contour_fill_flag):
    # テキストファイルをpandasデータフレーム形式で読み込む
    # 区切り文字はsepで指定できる。例えば、タブ区切りの場合はsep='\t'と記述する
    df = pd.read_csv(input_file, sep=',', encoding="utf-8")

    # x, y, zデータを1次元のnumpyアレイ型へ変換
    x = df['NE'].values
    y = df['TRQ'].values
    z = df['NOx'].values

    # データ数と最小値、最大値を抽出
    x_min = x.min()
    x_max = x.max()
    y_min = y.min()
    y_min = 30
    y_max = y.max()
    y_max = 100

    xrange = x_max - x_min
    yrange = y_max - y_min

    ratio = 0.5


    # データ点数を減らし等間隔の格子点用のデータを抜粋して作成する
    n = 200
    xi, yi = np.linspace(x.min(), x.max(), n), np.linspace(y.min(), y.max(), n)
    xi, yi = np.meshgrid(xi, yi)
    # データ抜けがある場合にデータを線形補完
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # 画像のインスタンスを生成
    fig = plt.figure(figsize=(12, 8))

    # 等高線
    if contour_fill_flag:  # 等高線を塗りつぶす場合
        ax1 = fig.add_subplot(111)
        contour1 = ax1.contour(zi, vmin=z.min(), vmax=z.max(),
                               origin='lower', levels=my_levels, colors=['black'],
                               extent=[x.min(), x.max(), y.min(), y.max()], linestyles='dashed', linewidths=1)
        contour2 = plt.contourf(xi, yi, zi, cmap=my_cmap, norm=Normalize(vmin=z.min(), vmax=40))
        contour1.clabel(fmt='%1.1f', fontsize=10)
        # colorbarのサイズを縦横0.5倍にする。
        plt.colorbar(contour2,ax=ax1, shrink=0.5)

    else:
        # 背景色の設定 https://xkcd.com/color/rgb/
        ax1 = fig.add_subplot(111, facecolor="#ffffe4")  # 背景色：オフホワイト
        contour1 = ax1.contour(zi, vmin=z.min(), vmax=z.max(),
                               origin='lower', levels=my_levels, cmap=my_cmap,
                               extent=[x.min(), x.max(), y.min(), y.max()])
        contour1.clabel(fmt='%1.1f', fontsize=10)
        plt.colorbar(contour1)

    # ラベル
    my_fontsize = 12
    ax1.set_xlabel(my_xlabel, fontsize=my_fontsize)
    ax1.set_ylabel(my_ylabel, fontsize=my_fontsize)

    # 軸の範囲
    buf_x = (x_max - x_min) * 0.001
    buf_y = (y_max - y_min) * 0.001
    ax1.set_xlim(x_min - buf_x, x_max + buf_x)
    ax1.set_ylim(y_min - buf_y, y_max + buf_y)
    ax1.set_aspect(ratio/ax1.get_data_ratio(), adjustable='box')

    # 格子グリッド
    plt.grid()
    # X,Y軸の1目盛りの表示の縦横比を揃える
    #plt.gca().set_aspect('equal', adjustable='box')
    plt.tick_params(labelsize=my_fontsize)
    plt.tight_layout()
    fig.savefig(now + '_' + file_name + "_contour_" + str(contour_fill_flag) + ".png")

    plt.show()
    plt.close()


if __name__ == "__main__":
    # 読み出すcsvファイル
    input_file = 'test4.csv'

    # 等高線の数
    my_levels = 20

    # カラーマップ
    my_cmap = 'jet'  # 'bwr' 'bwr_r' jet PuOr

    # ラベル
    my_xlabel = 'NE'
    my_ylabel = 'TRQ'
    file_name = 'p1'


    # 等高線図を作成する関数の呼び出し
    plot_func(True)  # コンターを塗りつぶす場合はTrue
