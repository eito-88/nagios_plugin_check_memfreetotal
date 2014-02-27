# check_memfreetotal - Checking overall  memory free space (RAM + Swap) plugin for Nagios

- Copyright(C) 2014 Yuichiro SAITO (@koemu)

- This software is released under the MIT License, see LICENSE.txt.


## check_memfreetotal とは？

メモリの空き容量を確認する事ができます。容量は、物理メモリ＋スワップメモリを合計した値を元に算出します。

その上で、一定以下の空き容量になったときに、WarningまたはCriticalを返します。閾値は、パーセンテージと実容量を選択可能です。

## 他のメモリチェックプラグインとの違い

check_swap を用いると、スワップメモリの空き容量を確認する事ができます。この方法だと、仮に物理メモリに空き容量が出た場合でも、ページアウトしたメモリページが残っていてもステータスがOKにならない場合があります。また、スワップメモリの使用量が多量になっただけではパフォーマンス劣化には直接は結びつきません。

また、2014年2月現在、nagios-pluginsでまとめて頒布されているプラグインの中に、物理メモリの空き容量確認を行えるプラグインはありません。また、スワップメモリに十分な空き容量が確保できていれば、物理メモリ不足だけではOOMKillerが発動する等の問題は発生しません。

以上の事から、メモリの空き容量を確認するには、物理メモリ及びスワップメモリの両方を確認する事が大切になります。

## Requirements

- OS: Linux Kernel 2.6.18 or above
- Python: 2.6 or 2.7

## Usage

- --version 本プログラムのバージョンを表示します。
- -h, --help コマンドラインのヘルプを表示します。
- -w \<free\>, --warning=\<free\> メモリの空き容量が指定した値未満になった場合、Warningステータスを返します。パーセントか、キロバイトを選択して設定できます。
- -c \<free\>, --critical=\<free\> メモリの空き容量が指定した値未満になった場合、Criticalステータスを返します。パーセントか、キロバイトを選択して設定できます。
- -V, --verbose メッセージを詳細に表示します。デバッグ用です。

## changelog

* 2013-02 0.0.1 Initial release.

