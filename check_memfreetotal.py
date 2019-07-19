#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------
# check_memfreetotal
# 物理メモリとスワップメモリを合計した空き容量を
# チェックします
#
# Copyright(C) 2014 Yuichiro SAITO
# This software is released under the MIT License, see LICENSE.txt.
# ----------------------------------------------

import sys
import os
import glob
import time
import re
import commands
import logging
import logging.config
from optparse import OptionParser

#-----------------------------------------------
# Global Variables
#-----------------------------------------------
LOG_FORMAT      = '%(levelname)s\t%(asctime)s\t%(name)s\t%(funcName)s\t"%(message)s"'
PROGRAM_VERSION = "0.0.2"


#-----------------------------------------------
# 内部クラス: _MemFree
#-----------------------------------------------
class _MemFree:
    """
    内部クラス _MemFreeクラス
    """

    # クラス変数
    STATE_OK        = 0
    STATE_WARNING   = 1
    STATE_CRITICAL  = 2
    STATE_UNKNOWN   = 3
    STATE_DEPENDENT = 4
    MODE_UNKNOWN    = 0
    MODE_INTEGER    = 1
    MODE_PERCENT    = 2

    #-----------------------------------------------

    def __init__( self, proc_meminfo = None ):
        """
        Constractor
        """
        self.log = logging.getLogger( self.__class__.__name__ )

        self.log.debug( "START" )

        if proc_meminfo is None:
            proc_meminfo = commands.getoutput( 'cat /proc/meminfo' )
        self.mem_info = self._parseMemInfo( proc_meminfo )

        self.warning_mode   = self.MODE_UNKNOWN
        self.warning        = 0
        self.critical_mode  = self.MODE_UNKNOWN
        self.critical       = 0

        self.log.debug( "END" )

    #-----------------------------------------------

    def __del__( self ):
        """
        Destructor
        """
        self.log.debug( "START" )
        pass
        self.log.debug( "END" )

    #-----------------------------------------------

    def _printWarning( self, msg ):
        """
        Warningを出力し、返り値を設定します。
        """
        print "WARNING: %s" % msg
        
        return self.STATE_WARNING

    #-----------------------------------------------

    def _printCritical( self, msg ):
        """
        Criticalを出力し、返り値を設定します。
        """
        print "CRITICAL: %s" % msg
        
        return self.STATE_CRITICAL

    #-----------------------------------------------

    def _printUnknown( self, msg ):
        """
        Unknownを出力し、返り値を設定します。
        """
        print "UNKNOWN: %s" % msg
        
        return self.STATE_UNKNOWN

    #-----------------------------------------------

    def _parseMemInfo( self, mem_info ):
        """
        /proc/meminfo をパースします
        @param mem_info /proc/meminfoの内容を入力します
        @return dictにパースした状態を返します。なお、単位はKiBです。
        """
        self.log.debug( "START" )

        lines = mem_info.split( "\n" )
        result = {}

        for line in lines:
            columns = line.split( ":" )
            if len( columns ) < 2:
                continue
            values = columns[1].strip().split( " " )
            result[ columns[0] ] = int( values[0] )
            if len( values ) == 1:
                result[ columns[0] ] /= 1024  # バイト単位をKiB単位に変換

        self.log.debug( result )
        self.log.debug( "END" )

        return result

    #-----------------------------------------------

    def _setValue( self, value ):
        """
        評価の値を設定します。%がついていればパーセンテージ、なければKiBが評価モードとなります。
        @param value セットしたい値を入れます
        @return dictでセットした値を返します。valueが値, modeが評価のモードです
        """
        self.log.debug( "START" )
        
        set_value = { "value": None, "mode": self.MODE_UNKNOWN }

        if re.match( "(.*)%$", value ):
            set_value[ "mode" ]  = self.MODE_PERCENT
            set_value[ "value" ] = int( value.replace( "%", "" ) )
        else:
            set_value[ "mode" ]  = self.MODE_INTEGER
            set_value[ "value" ] = int( value )

        self.log.debug( set_value )
        self.log.debug( "END" )

        return set_value

    #-----------------------------------------------

    def _isValidThreshold( self ):
        """
        閾値の関係に異常が無いかを評価します
        @return ステータスを返します
        """
        self.log.debug( "START" )

        if self.warning_mode == self.MODE_UNKNOWN or self.critical_mode == self.MODE_UNKNOWN:
            # まだ値が設定されていないので評価しない
            pass
        elif self.warning_mode != self.critical_mode:
            # 単位の関係が一緒でない時は評価できないんでエラー
            return self._printUnknown( "Mismatch threshold unit." )
        elif self.warning_mode == self.MODE_PERCENT and self.warning > 100:
            return self._printUnknown( "Warning is over 100%." )
        elif self.critical_mode == self.MODE_PERCENT and self.critical > 100:
            return self._printUnknown( "Critical is over 100%." )
        elif self.warning < self.critical:
            return self._printUnknown( "Warning value should be more than critical value." )

        self.log.debug( "END" )

        return self.STATE_OK

    #-----------------------------------------------

    def setWarning( self, warning ):
        """
        warning値をセットします
        @param warning warning値をセットします
        """
        self.log.debug( "START" )

        set_value = self._setValue( warning )
        self.warning_mode = set_value[ "mode" ]
        self.warning      = set_value[ "value" ]

        ret = self._isValidThreshold()
        if ret != self.STATE_OK:
            self.log.debug( "EXIT" )
            return ret

        self.log.debug( "END" )

        return self.STATE_OK

    #-----------------------------------------------

    def setCritical( self, critical ):
        """
        critical値をセットします
        @param critical critical値をセットします
        """
        self.log.debug( "START" )

        set_value = self._setValue( critical )
        self.critical_mode = set_value[ "mode" ]
        self.critical      = set_value[ "value" ]

        ret = self._isValidThreshold()
        if ret != self.STATE_OK:
            self.log.debug( "EXIT" )
            return ret

        self.log.debug( "END" )

        return self.STATE_OK

    #-----------------------------------------------

    def checkMemFree( self, withoutswap ):
        """
        閾値を評価します
        @param withoutswap スワップ領域を除いて計算するかどうか
        @return Nagiosの規則に沿った結果を返します
        """
        self.log.debug( "START" )
        self.log.debug( "Witout Swap: " + str(withoutswap) )

        # メモリ量計算のベース値
        mem_total = self.mem_info[ "MemTotal" ]
        mem_free  = self.mem_info[ "MemFree" ] + self.mem_info[ "Buffers" ] + self.mem_info[ "Cached" ]

        # meminfoにMemAvailableやActive/Inactive(file)がある場合は置換します
        if "MemAvailable" in self.mem_info: #  > RHEL7
            self.log.debug( "MemAvailable has detected." )
            mem_free = self.mem_info[ "MemAvailable" ]
        elif "Active(file)" in self.mem_info and "Inactive(file)" in self.mem_info: # RHEL6
            self.log.debug( "Active/Inactive(file) has detected." )
            mem_free = self.mem_info[ "MemFree" ] + self.mem_info[ "Active(file)" ] + self.mem_info[ "Inactive(file)" ]

        # スワップを入れたい場合はその分を加算
        if not withoutswap:
            mem_total += self.mem_info[ "SwapTotal" ]
            mem_free  += self.mem_info[ "SwapFree" ]

        mem_free_percent = ( 100.0 * mem_free ) / mem_total

        # 割合で評価
        if self.critical_mode == self.MODE_PERCENT and self.critical > mem_free_percent:
            return self._printCritical( "Free memory is drying up (%.1f%%)." % mem_free_percent )
        elif self.warning_mode == self.MODE_PERCENT and self.warning > mem_free_percent:
            return self._printWarning( "Free memory is not enough (%.1f%%)." % mem_free_percent )
        # 値で評価
        if self.critical_mode == self.MODE_INTEGER and self.critical > mem_free:
            return self._printCritical( "Free memory is drying up (%d KiB)." % mem_free )
        elif self.warning_mode == self.MODE_INTEGER and self.warning > mem_free:
            return self._printWarning( "Free memory is not enough (%d KiB)." % mem_free )
        
        print "OK: Remained free memory is %d KiB (%.1f%%)." % ( mem_free, mem_free_percent )
        
        self.log.debug( "END" )

        return self.STATE_OK


#-----------------------------------------------
# Main
#-----------------------------------------------

def main():
    """
    Main
    """

    # 引数のパース
    usage   = "Usage: %prog [option ...]"
    version ="%%prog %s\nCopyright (C) 2014 Yuichiro SAITO." % ( PROGRAM_VERSION )
    parser  = OptionParser( usage = usage, version = version )
    parser.add_option("-w", "--warning",
                      type="string",
                      dest="warning",
                      metavar="<free>",
                      help="Exit with WARNING status if less than value of space is free. You can choice kilobyte (integer) or percent (%).")
    parser.add_option("-c", "--critical",
                      type="string",
                      dest="critical",
                      metavar="<free>",
                      help="Exit with CRITICAL status if less than value of space is free. You can choice kilobyte (integer) or percent (%).")
    parser.add_option("-s", "--without_swap",
                      action="store_true",
                      dest="withoutswap",
                      default=False,
                      help="Calculate without swap. Default is False.")
    parser.add_option("-V", "--verbose",
                      action="store_true",
                      dest="verbose",
                      default=False,
                      help="Verbose mode. (For debug only)")
    ( options, args ) = parser.parse_args()
    prog_name = parser.get_prog_name()

    if len( sys.argv ) < 4:
        OptionParser.print_version( parser )
        return _MemFree.STATE_UNKNOWN

    if options.verbose:
        logging.basicConfig( level=logging.DEBUG, format = LOG_FORMAT )
    else:
        logging.basicConfig( level=logging.WARNING, format = LOG_FORMAT )

    logging.debug( "START" )

    # 評価を実施
    mem_free = _MemFree()
    ret = mem_free.setWarning( options.warning )
    if ret != _MemFree.STATE_OK:
        logging.debug( "EXIT" )
        return ret
    ret = mem_free.setCritical( options.critical )
    if ret != _MemFree.STATE_OK:
        logging.debug( "EXIT" )
        return ret
    ret = mem_free.checkMemFree( options.withoutswap )
    if ret != _MemFree.STATE_OK:
        logging.debug( "EXIT" )
        return ret

    logging.debug( "END" )

#-----------------------------------------------

if __name__ == '__main__':
    sys.exit( main() )

