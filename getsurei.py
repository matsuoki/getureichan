#!/usr/local/bin/python3.8

"""
下記のサイトをもとにちょとだけ調整したもの。

大阪市立科学館　学芸員　江越　航のホームページ
python で今日の月 (PyEphem版)
http://www.sci-museum.kita.osaka.jp/~egoshi/astronomy/python/python_moon.html
"""

#import random
import datetime
import ephem
import numpy as np
#import matplotlib.pyplot as plt
import matplotlib
import pylab as plt
from mpl_toolkits.mplot3d import Axes3D

DEBUG=0
MYFONT=""

if DEBUG==1 :
    #matplotlib.use()  # desktopheadless
    MYFONT='IMS Gothic'
else:
    matplotlib.use('Agg')  # headless
    MYFONT='ipagothic'

# 観測地設定
osaka = ephem.Observer()
osaka.lat = '34.6914'
osaka.lon = '135.4917'
osaka.date = datetime.datetime.utcnow()

def main():
    """
    main
    """

    fname=f"{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.png"
    info=makefig(fname)
    print(info)

def makefig(fpath):
    """
    画像作成
    """
    # 月
    moon = ephem.Moon()

    # 次回　月の出・月の入り等を表示
    if 0 :
        print('次の月の出　 :', ephem.localtime(osaka.next_rising(moon)).strftime("%Y"))
        print('次の月の入り :', ephem.localtime(osaka.next_setting(moon)))
        print('次の新月 :', ephem.localtime(ephem.next_new_moon(osaka.date)))
        print('次の上弦 :', ephem.localtime(ephem.next_first_quarter_moon(osaka.date)))
        print('次の満月 :', ephem.localtime(ephem.next_full_moon(osaka.date)))
        print('次の下弦 :', ephem.localtime(ephem.next_last_quarter_moon(osaka.date)))
        print('現在の月齢 :', osaka.date - ephem.previous_new_moon(osaka.date))

    # 月と太陽の離角を計算
    moon.compute(osaka)
    moon_elong = np.rad2deg(moon.elong)

    # 描画領域を準備
    #fig = plt.figure(figsize=(5,5))
    fig = plt.figure(figsize=(5,5))

    #ax = fig.gca(projection='3d')
    #ax = fig.gca()
    ax = fig.add_subplot(projection='3d')

    # x, y, z軸の範囲設定
    ax.set_xlim([-1., 1.])
    ax.set_ylim([-1., 1.])
    ax.set_zlim([-1, 1.])


    #背景の x, y, z面を非表示に
    if DEBUG!=1:
        ax.set_axis_off()
    #for a in [ax.w_xaxis, ax.w_yaxis, ax.w_zaxis]:
    #    a.line.set_linewidth(0)
    #    a.set_pane_color((0., 0., 0., 0.))

    # 背面
    #ax.set_facecolor('lightgray')
    if DEBUG!=1:
        ax.set_facecolor('black')

    # メッシュ状の球面 (u, v) を準備し、(x, y, z) 値を計算
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:25j] # u:接線方向　v:動経方向
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)

    # メッシュの球面に貼りつける色を準備（半分だけ黄色に）

    colors = np.zeros((50, 25, 3))
    for i in range(0, 25):
        for j in range(0, 25):
            colors[i][j][0] = 1
            colors[i][j][1] = 1
            colors[i][j][2] = 0

    # 球面をプロット
    ax.plot_surface(x, y, z, facecolors = colors, shade=False)
    # グラフを見る方向を設定
    ax.view_init(elev = 0, azim = moon_elong - 90)

    e=ephem.localtime
    print (e(osaka.next_rising(moon)))
    info_text=""
    info_text= (
        '月の出　:{0:%m/%d %H:%M}\n'
        '月の入り:{1:%m/%d %H:%M}\n'
        '新月    :{2:%m/%d %H:%M}\n'
        '上弦    :{3:%m/%d %H:%M}\n'
        '満月    :{4:%m/%d %H:%M}\n'
        '下弦    :{5:%m/%d %H:%M}\n'
        '月齢    :{6:.2f} (0-15)\n'
        '観測場所:大阪\n').format(
        ephem.localtime(osaka.next_rising(moon))
        ,ephem.localtime(osaka.next_setting(moon))
        ,ephem.localtime(ephem.next_new_moon(osaka.date))
        ,ephem.localtime(ephem.next_first_quarter_moon(osaka.date))
        ,ephem.localtime(ephem.next_full_moon(osaka.date))
        ,ephem.localtime(ephem.next_last_quarter_moon(osaka.date))
        ,osaka.date - ephem.previous_new_moon(osaka.date))

    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_box_aspect((1,1,1)) #アスペクト比
    plt.savefig(fpath)

    if DEBUG == 1:
        plt.show()

    return info_text

if __name__ == "__main__":
    main()



