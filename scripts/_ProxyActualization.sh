#!/bin/sh
##################################################################
#                                                                #
# "Демонизация" скрипта ProxyProxyActualization.py               #
# В rc.local добавляем в виде форкнутых процессов.               #
#                                                                #
##################################################################
#                                                                #
# Скрипт является частью проекта "acisi"                         #
# Автор: Черноусов Антон (acisi82@mail.ru)                       #
# WEB: http://www.acisi.ru                                       #
#                                                                #
##################################################################

ScriptDirectory=`dirname $0`
while true;
do
    $ScriptDirectory/./../scripts/ProxyActualization.py
    sleep 2
done
