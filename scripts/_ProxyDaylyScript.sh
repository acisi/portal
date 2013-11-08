#!/bin/sh
################################################################
#                                                              #
# Скрипт является частью проекта "acisi"                       #
# Автор: Черноусов Антон (acisi82@mail.ru)                     #
# WEB: http://www.acisi.ru                                     #
#                                                              #
################################################################
#                                                              #
# Скрипт занимается сбором данных со сторонних ресурсов,       #
# данные о сайтах содержащих списки прокси-серверов получаются #
# запросом к серверу Рамблер скриптом Get_Proxy_Urls.py        #
# в дальнейшем производится сбор данных средствами wget и      #
# выборка ip-адресов средствами grep (полностью типовой shell  #
# скрипт). Дальнейшая обработка и перенос в БД осушествляется  #
# скриптом Upload_Proxy_IP.py                                  #
#                                                              #
################################################################

ScriptDirectory=`dirname $0`
mkdir $ScriptDirectory/../data/tmp/
mkdir $ScriptDirectory/../data/tmp/web
rm -R $ScriptDirectory/../data/tmp/web/*
cat $ScriptDirectory/../data/listtodownload.data | sort | uniq > $ScriptDirectory/../data/listtodownload.data.uniq
cat $ScriptDirectory/../data/listtodownload.data.uniq | while read url;
    do
    echo $url
    wget -q -r --referer="http://www.google.com" --user-agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6" \
    --header="Accept: text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5" --header="Accept-Language: en-us,en;q=0.5" \
    --header="Accept-Encoding: deflate" --header="Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7" --header="Keep-Alive: 300" \
    --directory-prefix=$ScriptDirectory/../data/tmp/web/ "$url" &
    pid_to_kill=`echo $!`
    sleep 240
    kill $pid_to_kill
    done
echo > $ScriptDirectory/../data/tmp/metafile.dat
find $ScriptDirectory/../data/tmp/web/ -type f | while read files;
    do
    cat $files >> $ScriptDirectory/../data/tmp/metafile.dat
    done
rm -R $ScriptDirectory/../data/tmp/web/*
cat $ScriptDirectory/../data/tmp/metafile.dat | grep -a -E -o '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)' > $ScriptDirectory/../data/tmp/iplist.dat
rm $ScriptDirectory/../data/tmp/metafile.dat
cat $ScriptDirectory/../data/tmp/iplist.dat | sort | uniq > $ScriptDirectory/../data/tmp/iplist.lst
rm $ScriptDirectory/../data/tmp/iplist.dat
