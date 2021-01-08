#!/ usr/bin/python
# -*- coding:utf-8 -*-

# GPS设备得到的结果是WGS84大地坐标（经纬度）
# 两端程序结果差不多
# 转换软件：浙江省第一测绘院CGCS2000坐标计算
#           输入的时候经纬度应输入度分秒格式
#           而程序中经纬度是将度分秒格式转成十进制，转换工具https://www.osgeo.cn/app/s2703




# 1、https://blog.csdn.net/normalstudent/article/details/82223350

import math


def LatLon2XY(latitude, longitude):
    a = 6378137.0
    # b = 6356752.3142
    # c = 6399593.6258
    # alpha = 1 / 298.257223563
    e2 = 0.0066943799013
    # epep = 0.00673949674227


    #将经纬度转换为弧度
    latitude2Rad = (math.pi / 180.0) * latitude

    beltNo = int((longitude + 1.5) / 3.0) #计算3度带投影度带号
    L = beltNo * 3 #计算中央经线
    l0 = longitude - L #经差
    tsin = math.sin(latitude2Rad)
    tcos = math.cos(latitude2Rad)
    t = math.tan(latitude2Rad)
    m = (math.pi / 180.0) * l0 * tcos
    et2 = e2 * pow(tcos, 2)
    et3 = e2 * pow(tsin, 2)
    X = 111132.9558 * latitude - 16038.6496 * math.sin(2 * latitude2Rad) + 16.8607 * math.sin(
        4 * latitude2Rad) - 0.0220 * math.sin(6 * latitude2Rad)
    N = a / math.sqrt(1 - et3)

    x = X + N * t * (0.5 * pow(m, 2) + (5.0 - pow(t, 2) + 9.0 * et2 + 4 * pow(et2, 2)) * pow(m, 4) / 24.0 + (
    61.0 - 58.0 * pow(t, 2) + pow(t, 4)) * pow(m, 6) / 720.0)
    y = 500000 + N * (m + (1.0 - pow(t, 2) + et2) * pow(m, 3) / 6.0 + (
    5.0 - 18.0 * pow(t, 2) + pow(t, 4) + 14.0 * et2 - 58.0 * et2 * pow(t, 2)) * pow(m, 5) / 120.0)

    return x, y


def XY2LatLon(X, Y, L0): # L0中央经线

    iPI = 0.0174532925199433
    a = 6378137.0
    f= 0.00335281006247
    ZoneWide = 3 #按3度带进行投影

    ProjNo = int(X / 1000000)
    L0 = L0 * iPI
    X0 = ProjNo * 1000000 + 500000
    Y0 = 0
    xval = X - X0
    yval = Y - Y0

    e2 = 2 * f - f * f #第一偏心率平方
    e1 = (1.0 - math.sqrt(1 - e2)) / (1.0 + math.sqrt(1 - e2))
    ee = e2 / (1 - e2) #第二偏心率平方

    M = yval
    u = M / (a * (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256))

    fai = u \
          + (3 * e1 / 2 - 27 * e1 * e1 * e1 / 32) * math.sin(2 * u) \
          + (21 * e1 * e1 / 16 - 55 * e1 * e1 * e1 * e1 / 32) * math.sin(4 * u) \
          + (151 * e1 * e1 * e1 / 96) * math.sin(6 * u)\
          + (1097 * e1 * e1 * e1 * e1 / 512) * math.sin(8 * u)
    C = ee * math.cos(fai) * math.cos(fai)
    T = math.tan(fai) * math.tan(fai)
    NN = a / math.sqrt(1.0 - e2 * math.sin(fai) * math.sin(fai))
    R = a * (1 - e2) / math.sqrt(
        (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)))
    D = xval / NN

    #计算经纬度（弧度单位的经纬度）
    longitude1 = L0 + (D - (1 + 2 * T + C) * D * D * D / 6 + (
    5 - 2 * C + 28 * T - 3 * C * C + 8 * ee + 24 * T * T) * D * D * D * D * D / 120) / math.cos(fai)
    latitude1 = fai - (NN * math.tan(fai) / R) * (
    D * D / 2 - (5 + 3 * T + 10 * C - 4 * C * C - 9 * ee) * D * D * D * D / 24 + (
    61 + 90 * T + 298 * C + 45 * T * T - 256 * ee - 3 * C * C) * D * D * D * D * D * D / 720)

    #换换为deg
    longitude = longitude1 / iPI
    latitude = latitude1 / iPI

    return latitude, longitude

# 
# print LatLon2XY(40.07837722329, 116.23514827596)
# print XY2LatLon(434760.7611718801, 4438512.040474475, 117.0)



# 2、https://blog.csdn.net/m0_37667770/article/details/104024952?utm_medium=distribute.wap_relevant_download.none-task-blog-BlogCommendFromBaidu-3.nonecase&depth_1-utm_source=distribute.wap_relevant_download.none-task-blog-BlogCommendFromBaidu-3.nonecase
#       java程序，比较全面（注释见链接）

package com.example.androiddaggerstudy.lat;
import org.jetbrains.annotations.NotNull;
import kotlin.jvm.internal.Intrinsics;
/**
 * 版权：渤海新能 版权所有
 *
 * @author feiWang
 * 版本：1.5
 * 创建日期：2020/10/16
 * 描述：AndroidDaggerStudy
 * E-mail : 1276998208@qq.com
 * CSDN:https://blog.csdn.net/m0_37667770/article
 * GitHub:https://github.com/luhenchang
 */
public class JavaRtkUtils {
    private  double p = 206264.80624709636D;
    @NotNull
    public  Tuple xyTowgs84(double x, double y, double L0) {
        double a = 6378137.0D;
        double efang = 0.0066943799901413D;
        double e2fang = 0.0067394967422764D;
        y = y - (double)500000;
        double m0 = 0.0D;
        double m2 = 0.0D;
        double m4 = 0.0D;
        double m6 = 0.0D;
        double m8 = 0.0D;
        m0 = a * ((double)1 - efang);
        m2 = 1.5D * efang * m0;
        m4 = efang * m2 * 5.0D / 4.0D;
        m6 = efang * m4 * 7.0D / 6.0D;
        m8 = efang * m6 * 9.0D / 8.0D;
        double a0 = 0.0D;
        double a2 = 0.0D;
        double a4 = 0.0D;
        double a6 = 0.0D;
        double a8 = 0.0D;
        a0 = m0 + m2 / 2.0D + m4 * 3.0D / 8.0D + m6 * 5.0D / 16.0D + m8 * 35.0D / 128.0D;
        a2 = m2 / 2.0D + m4 / 2.0D + m6 * 15.0D / 32.0D + m8 * 7.0D / 16.0D;
        a4 = m4 / 8.0D + m6 * 3.0D / 16.0D + m8 * 7.0D / 32.0D;
        a6 = m6 / 32.0D + m8 / 16.0D;
        a8 = m8 / 128.0D;
        double FBf = 0.0D;
        double Bf0 = x / a0;

        for(double Bf1 = 0.0D; Bf0 - Bf1 >= 1.0E-4D; Bf0 = (x - FBf) / a0) {
            Bf1 = Bf0;
            FBf = -a2 * Math.sin((double)2 * Bf0) / (double)2 + a4 * Math.sin((double)4 * Bf0) / (double)4 - a6 * Math.sin((double)6 * Bf0) / (double)6 + a8 * Math.sin((double)8 * Bf0) / (double)8;
        }

        double Wf = Math.sqrt((double)1 - efang * Math.sin(Bf0) * Math.sin(Bf0));
        double Nf = a / Wf;
        double Mf = a * ((double)1 - efang) / Math.pow(Wf, 3.0D);
        double nffang = e2fang * Math.cos(Bf0) * Math.cos(Bf0);
        double tf = Math.tan(Bf0);
        double B = Bf0 - tf * y * y / ((double)2 * Mf * Nf) + tf * ((double)5 + (double)3 * tf * tf + nffang - (double)9 * nffang * tf * tf) * Math.pow(y, 4.0D) / ((double)24 * Mf * Math.pow(Nf, 3.0D)) - tf * ((double)61 + (double)90 * tf * tf + (double)45 * Math.pow(tf, 4.0D)) * Math.pow(y, 6.0D) / ((double)720 * Mf * Math.pow(Nf, 5.0D));
        double l = y / (Nf * Math.cos(Bf0)) - ((double)1 + (double)2 * tf * tf + nffang) * Math.pow(y, 3.0D) / ((double)6 * Math.pow(Nf, 3.0D) * Math.cos(Bf0)) + ((double)5 + (double)28 * tf * tf + (double)24 * Math.pow(tf, 4.0D)) * Math.pow(y, 5.0D) / ((double)120 * Math.pow(Nf, 5.0D) * Math.cos(Bf0));
        double L = l + L0;
        double[] array_B = this.rad2dms(B);
        double[] array_L = this.rad2dms(L);
        double Bdec = this.dms2dec(array_B);
        double Ldec = this.dms2dec(array_L);
        return new Tuple(Bdec, Ldec);
    }
    public  double gaussLongToDegreen(double B, double L, int N) {
        double L00 = (double)Math.round(L / (double)3) * (double)3;
        return L00 / (double)180 * 3.1415926D;
    }
    @NotNull
    public  double[] rad2dms(double rad) {
        double[] a = new double[]{0.0D, 0.0D, 0.0D};
        double dms = rad * p;
        a[0] = Math.floor(dms / 3600.0D);
        a[1] = Math.floor((dms - a[0] * (double)3600) / 60.0D);
        a[2] = (double)((int)Math.floor(dms - a[0] * (double)3600)) - a[1] * (double)60;
        return a;
    }

    public  double dms2dec(@NotNull double[] dms) {
        Intrinsics.checkNotNullParameter(dms, "dms");
        double dec = 0.0D;
        dec = dms[0] + dms[1] / 60.0D + dms[2] / 3600.0D;
        return dec;
    }

    @NotNull
    public  Tuple GetXY(double B, double L, double degree) {
        double[] xy = new double[]{0.0D, 0.0D};
        double a = 6378137.0D;
        double b = 6356752.314245179D;
        double e = 0.081819190842621D;
        double eC = 0.0820944379496957D;
        double L0 = 0.0D;
        int n;
        if (degree == 6.0D) {
            n = (int)Math.round((L + degree / (double)2) / degree);
            L0 = degree * (double)n - degree / (double)2;
        } else {
            n = (int)Math.round(L / degree);
            L0 = degree * (double)n;
        }

        double radB = B * 3.141592653589793D / (double)180;
        double radL = L * 3.141592653589793D / (double)180;
        double deltaL = (L - L0) * 3.141592653589793D / (double)180;
        double N = a * a / b / Math.sqrt((double)1 + eC * eC * Math.cos(radB) * Math.cos(radB));
        double C1 = 1.0D + 0.75D * e * e + 0.703125D * Math.pow(e, 4.0D) + 0.68359375D * Math.pow(e, 6.0D) + 0.67291259765625D * Math.pow(e, 8.0D);
        double C2 = 0.75D * e * e + 0.9375D * Math.pow(e, 4.0D) + 1.025390625D * Math.pow(e, 6.0D) + 1.07666015625D * Math.pow(e, 8.0D);
        double C3 = 0.234375D * Math.pow(e, 4.0D) + 0.41015625D * Math.pow(e, 6.0D) + 0.538330078125D * Math.pow(e, 8.0D);
        double C4 = 0.068359375D * Math.pow(e, 6.0D) + 0.15380859375D * Math.pow(e, 8.0D);
        double C5 = 0.00240325927734375D * Math.pow(e, 8.0D);
        double t = Math.tan(radB);
        double eta = eC * Math.cos(radB);
        double X = a * ((double)1 - e * e) * (C1 * radB - C2 * Math.sin((double)2 * radB) / (double)2 + C3 * Math.sin((double)4 * radB) / (double)4 - C4 * Math.sin((double)6 * radB) / (double)6 + C5 * Math.sin((double)8 * radB));
        xy[0] = X + N * Math.sin(radB) * Math.cos(radB) * Math.pow(deltaL, 2.0D) * ((double)1 + Math.pow(deltaL * Math.cos(radB), 2.0D) * ((double)5 - t * t + (double)9 * eta * eta + (double)4 * Math.pow(eta, 4.0D)) / (double)12 + Math.pow(deltaL * Math.cos(radB), 4.0D) * ((double)61 - (double)58 * t * t + Math.pow(t, 4.0D)) / (double)360) / (double)2;
        xy[1] = N * deltaL * Math.cos(radB) * ((double)1 + Math.pow(deltaL * Math.cos(radB), 2.0D) * ((double)1 - t * t + eta * eta) / (double)6 + Math.pow(deltaL * Math.cos(radB), 4.0D) * ((double)5 - (double)18 * t * t + Math.pow(t, 4.0D) - (double)14 * eta * eta - (double)58 * eta * eta * t * t) / (double)120) + (double)500000;
        return new Tuple(xy[0], xy[1]);
    }

}

