# -*- coding: utf-8 -*-

# ----------------------------------------------
# test_check_memfreetotal.py
#
# Copyright(C) 2014 Yuichiro SAITO
# This software is released under the MIT License, see LICENSE.txt.
# ----------------------------------------------

import unittest
from check_memfreetotal import _MemFree


#-----------------------------------------------

class TestSequenceFunctions(unittest.TestCase):

    #-----------------------------------------------

    def setUp( self ):
        self.dataSwapUsed = """MemTotal:        1922800 kB
MemFree:           96780 kB
Buffers:           42612 kB
Cached:           889020 kB
SwapTotal:       2064376 kB
SwapFree:        1377560 kB"""
        self.dataSwapFree = """MemTotal:        1922368 kB
MemFree:          112552 kB
Buffers:          230168 kB
Cached:          1228720 kB
SwapTotal:       4726776 kB
SwapFree:        4726776 kB"""
        self.dataSwapNone = """MemTotal:        1922368 kB
MemFree:           84100 kB
Buffers:          230164 kB
Cached:          1228664 kB
SwapTotal:             0 kB
SwapFree:              0 kB"""
        self.dataRHEL6 = """MemTotal:        3774832 kB
MemFree:         1676628 kB
Buffers:              84 kB
Cached:           856536 kB
Active(file):     225336 kB
Inactive(file):   444076 kB
SwapTotal:       4063228 kB
SwapFree:        3611828 kB"""
        self.dataRHEL7 = """MemTotal:        3774832 kB
MemFree:         1690284 kB
MemAvailable:    2228584 kB
Buffers:              84 kB
Cached:           853608 kB
SwapTotal:       4063228 kB
SwapFree:        3611828 kB"""
        pass

    #-----------------------------------------------

    def test_paramCheck_OK_1( self ):
        """
        矛盾しないチェック %
        """
        mem_free = _MemFree( self.dataSwapUsed )
        ret = mem_free.setWarning( "20%" )
        self.assertEqual( ret, _MemFree.STATE_OK )
        ret = mem_free.setCritical( "10%" )
        self.assertEqual( ret, _MemFree.STATE_OK )

    #-----------------------------------------------

    def test_paramCheck_OK_2( self ):
        """
        矛盾しないチェック value
        """
        mem_free = _MemFree( self.dataSwapUsed )
        ret = mem_free.setWarning( "2048" )
        self.assertEqual( ret, _MemFree.STATE_OK )
        ret = mem_free.setCritical( "1024" )
        self.assertEqual( ret, _MemFree.STATE_OK )

    #-----------------------------------------------

    def test_paramCheck_Unknown_1( self ):
        """
        矛盾チェック %
        """
        mem_free = _MemFree( self.dataSwapUsed )
        ret = mem_free.setWarning( "10%" )
        self.assertEqual( ret, _MemFree.STATE_OK )
        ret = mem_free.setCritical( "20%" )
        self.assertEqual( ret, _MemFree.STATE_UNKNOWN )

    #-----------------------------------------------

    def test_paramCheck_Unknown_2( self ):
        """
        矛盾チェック %
        """
        mem_free = _MemFree( self.dataSwapUsed )
        ret = mem_free.setCritical( "20%" )
        self.assertEqual( ret, _MemFree.STATE_OK )
        ret = mem_free.setWarning( "10%" )
        self.assertEqual( ret, _MemFree.STATE_UNKNOWN )

    #-----------------------------------------------

    def test_paramCheck_Unknown_3( self ):
        """
        矛盾チェック value
        """
        mem_free = _MemFree( self.dataSwapUsed )
        ret = mem_free.setWarning( "1024" )
        self.assertEqual( ret, _MemFree.STATE_OK )
        ret = mem_free.setCritical( "2048" )
        self.assertEqual( ret, _MemFree.STATE_UNKNOWN )

    #-----------------------------------------------

    def test_paramCheck_Unknown_4( self ):
        """
        矛盾チェック value
        """
        mem_free = _MemFree( self.dataSwapUsed )
        ret = mem_free.setCritical( "2048" )
        self.assertEqual( ret, _MemFree.STATE_OK )
        ret = mem_free.setWarning( "1024" )
        self.assertEqual( ret, _MemFree.STATE_UNKNOWN )

    #-----------------------------------------------

    def test_paramCheck_Unknown_5( self ):
        """
        型不一致チェック
        """
        mem_free = _MemFree( self.dataSwapUsed )
        ret = mem_free.setCritical( "2048" )
        self.assertEqual( ret, _MemFree.STATE_OK )
        ret = mem_free.setWarning( "10%" )
        self.assertEqual( ret, _MemFree.STATE_UNKNOWN )

    #-----------------------------------------------

    def test_paramCheck_Unknown_6( self ):
        """
        型不一致チェック
        """
        mem_free = _MemFree( self.dataSwapUsed )
        ret = mem_free.setCritical( "20%" )
        self.assertEqual( ret, _MemFree.STATE_OK )
        ret = mem_free.setWarning( "1024" )
        self.assertEqual( ret, _MemFree.STATE_UNKNOWN )

    #-----------------------------------------------

    def test_validCheck_OK_1( self ):
        """
        バリデーション 正常チェック % スワップあり
        """
        mem_free = _MemFree( self.dataSwapUsed )
        mem_free.setCritical( "10%" )
        mem_free.setWarning( "60%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_OK )

    #-----------------------------------------------

    def test_validCheck_OK_2( self ):
        """
        バリデーション 正常チェック % スワップ空
        """
        mem_free = _MemFree( self.dataSwapFree )
        mem_free.setCritical( "10%" )
        mem_free.setWarning( "94%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_OK )

    #-----------------------------------------------

    def test_validCheck_OK_3( self ):
        """
        バリデーション 正常チェック % スワップなし
        """
        mem_free = _MemFree( self.dataSwapNone )
        mem_free.setCritical( "10%" )
        mem_free.setWarning( "80%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_OK )

    #-----------------------------------------------

    def test_validCheck_OK_4( self ):
        """
        バリデーション 正常チェック value スワップあり
        """
        mem_free = _MemFree( self.dataSwapUsed )
        mem_free.setCritical( "1024" )
        mem_free.setWarning( "2405972" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_OK )

    #-----------------------------------------------

    def test_validCheck_OK_5( self ):
        """
        バリデーション 正常チェック value スワップ空
        """
        mem_free = _MemFree( self.dataSwapFree )
        mem_free.setCritical( "1024" )
        mem_free.setWarning( "6298216" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_OK )

    #-----------------------------------------------

    def test_validCheck_OK_6( self ):
        """
        バリデーション 正常チェック value スワップなし
        """
        mem_free = _MemFree( self.dataSwapNone )
        mem_free.setCritical( "1024" )
        mem_free.setWarning( "1542928" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_OK )

    #-----------------------------------------------

    def test_validCheck_OK_7( self ):
        """
        バリデーション 正常チェック % スワップあり (RHEL 6)
        """
        mem_free = _MemFree( self.dataRHEL6 )
        mem_free.setCritical( "10%" )
        mem_free.setWarning( "60%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_OK )

    #-----------------------------------------------

    def test_validCheck_OK_8( self ):
        """
        バリデーション 正常チェック % スワップ未考慮 (RHEL 6)
        """
        mem_free = _MemFree( self.dataRHEL6 )
        mem_free.setCritical( "10%" )
        mem_free.setWarning( "60%" )
        self.assertEqual( mem_free.checkMemFree( True ), _MemFree.STATE_OK )

    #-----------------------------------------------

    def test_validCheck_OK_9( self ):
        """
        バリデーション 正常チェック % スワップあり (RHEL 7)
        """
        mem_free = _MemFree( self.dataRHEL7 )
        mem_free.setCritical( "10%" )
        mem_free.setWarning( "60%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_OK )

    #-----------------------------------------------

    def test_validCheck_OK_10( self ):
        """
        バリデーション 正常チェック % スワップ未考慮 (RHEL 7)
        """
        mem_free = _MemFree( self.dataRHEL7 )
        mem_free.setCritical( "10%" )
        mem_free.setWarning( "50%" )
        self.assertEqual( mem_free.checkMemFree( True ), _MemFree.STATE_OK )

    #-----------------------------------------------

    def test_validCheck_Warning_1( self ):
        """
        バリデーション Warningチェック % スワップあり
        """
        mem_free = _MemFree( self.dataSwapUsed )
        mem_free.setCritical( "60%" )
        mem_free.setWarning( "61%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_Warning_2( self ):
        """
        バリデーション Warningチェック % スワップ空
        """
        mem_free = _MemFree( self.dataSwapFree )
        mem_free.setCritical( "90%" )
        mem_free.setWarning( "95%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_Warning_3( self ):
        """
        バリデーション Warningチェック % スワップなし
        """
        mem_free = _MemFree( self.dataSwapNone )
        mem_free.setCritical( "80%" )
        mem_free.setWarning( "81%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_Warning_4( self ):
        """
        バリデーション Warningチェック value スワップあり
        """
        mem_free = _MemFree( self.dataSwapUsed )
        mem_free.setCritical( "1000000" )
        mem_free.setWarning( "2405973" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_Warning_5( self ):
        """
        バリデーション Warningチェック value スワップ空
        """
        mem_free = _MemFree( self.dataSwapFree )
        mem_free.setCritical( "5000000" )
        mem_free.setWarning( "6298217" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_Warning_6( self ):
        """
        バリデーション Warningチェック value スワップなし
        """
        mem_free = _MemFree( self.dataSwapNone )
        mem_free.setCritical( "500000" )
        mem_free.setWarning( "1542929" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_Critical_1( self ):
        """
        バリデーション Criticalチェック % スワップあり
        """
        mem_free = _MemFree( self.dataSwapUsed )
        mem_free.setCritical( "61%" )
        mem_free.setWarning( "62%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_CRITICAL )

    #-----------------------------------------------

    def test_validCheck_Critical_2( self ):
        """
        バリデーション Criticalチェック % スワップ空
        """
        mem_free = _MemFree( self.dataSwapFree )
        mem_free.setCritical( "95%" )
        mem_free.setWarning( "96%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_CRITICAL )

    #-----------------------------------------------

    def test_validCheck_Critical_3( self ):
        """
        バリデーション Criticalチェック % スワップなし
        """
        mem_free = _MemFree( self.dataSwapNone )
        mem_free.setCritical( "81%" )
        mem_free.setWarning( "82%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_CRITICAL )

    #-----------------------------------------------

    def test_validCheck_Critical_4( self ):
        """
        バリデーション Criticalチェック value スワップあり
        """
        mem_free = _MemFree( self.dataSwapUsed )
        mem_free.setCritical( "2405973" )
        mem_free.setWarning( "2405974" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_CRITICAL )

    #-----------------------------------------------

    def test_validCheck_Critical_5( self ):
        """
        バリデーション Criticalチェック value スワップ空
        """
        mem_free = _MemFree( self.dataSwapFree )
        mem_free.setCritical( "6298217" )
        mem_free.setWarning( "6298218" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_CRITICAL )

    #-----------------------------------------------

    def test_validCheck_Critical_6( self ):
        """
        バリデーション Criticalチェック value スワップなし
        """
        mem_free = _MemFree( self.dataSwapNone )
        mem_free.setCritical( "1542929" )
        mem_free.setWarning( "1542930" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_CRITICAL )

    #-----------------------------------------------

    def test_validCheck_WarningOnly_1( self ):
        """
        バリデーション Warning Onlyチェック % スワップあり
        """
        mem_free = _MemFree( self.dataSwapUsed )
        mem_free.setWarning( "61%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_WarningOnly_2( self ):
        """
        バリデーション Warning Onlyチェック % スワップ空
        """
        mem_free = _MemFree( self.dataSwapFree )
        mem_free.setWarning( "95%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_WarningOnly_3( self ):
        """
        バリデーション Warning Onlyチェック % スワップなし
        """
        mem_free = _MemFree( self.dataSwapNone )
        mem_free.setWarning( "81%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_WarningOnly_4( self ):
        """
        バリデーション Warning Onlyチェック value スワップあり
        """
        mem_free = _MemFree( self.dataSwapUsed )
        mem_free.setWarning( "2405973" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_WarningOnly_5( self ):
        """
        バリデーション Warning Onlyチェック value スワップ空
        """
        mem_free = _MemFree( self.dataSwapFree )
        mem_free.setWarning( "6298217" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_WarningOnly_6( self ):
        """
        バリデーション Warning Onlyチェック value スワップなし
        """
        mem_free = _MemFree( self.dataSwapNone )
        mem_free.setWarning( "1542929" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_CriticalOnly_1( self ):
        """
        バリデーション Critical Onlyチェック % スワップあり
        """
        mem_free = _MemFree( self.dataSwapUsed )
        mem_free.setCritical( "61%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_CRITICAL )

    #-----------------------------------------------

    def test_validCheck_CriticalOnly_2( self ):
        """
        バリデーション Critical Onlyチェック % スワップ空
        """
        mem_free = _MemFree( self.dataSwapFree )
        mem_free.setCritical( "95%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_CRITICAL )

    #-----------------------------------------------

    def test_validCheck_CriticalOnly_3( self ):
        """
        バリデーション Critical Onlyチェック % スワップなし
        """
        mem_free = _MemFree( self.dataSwapNone )
        mem_free.setCritical( "81%" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_CRITICAL )

    #-----------------------------------------------

    def test_validCheck_CriticalOnly_4( self ):
        """
        バリデーション Critical Onlyチェック value スワップあり
        """
        mem_free = _MemFree( self.dataSwapUsed )
        mem_free.setCritical( "2405973" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_CRITICAL )

    #-----------------------------------------------

    def test_validCheck_CriticalOnly_5( self ):
        """
        バリデーション Critical Onlyチェック value スワップ空
        """
        mem_free = _MemFree( self.dataSwapFree )
        mem_free.setCritical( "6298217" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_CRITICAL )

    #-----------------------------------------------

    def test_validCheck_Critical_6( self ):
        """
        バリデーション Critical Onlyチェック value スワップなし
        """
        mem_free = _MemFree( self.dataSwapNone )
        mem_free.setCritical( "1542929" )
        self.assertEqual( mem_free.checkMemFree( False ), _MemFree.STATE_CRITICAL )
        
    #-----------------------------------------------

#-----------------------------------------------

if __name__ == '__main__':
    unittest.main()

#-----------------------------------------------
