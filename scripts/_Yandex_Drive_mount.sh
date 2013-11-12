#!/bin/sh
#############################################################################
#                                                                           #
# Скрипт для монтирования Яндекс.Дисков (перемонтирование при обрыве связи) #
# В корне каждого Яндекс.Дика должен быть файл mounted содержащий строку OK #
#                                                                           #
#############################################################################

ScriptDirectory=`dirname $0`
while true;
do
    cat $ScriptDirectory/./../../DATA/YandexMountConfig.conf | while read line;
    do
    if [ "$line" != "" ];
    then
    username=`echo $line | awk -F";" '{ print $1}'`
    password=`echo $line | awk -F";" '{ print $2}'`
    mountp=`echo $line | awk -F";" '{ print $3}'`
    owneruser=`echo $line | awk -F";" '{ print $4}'`
    if [ "$owneruser" != "" ];
	then
	result=`cat $mountp/mounted`
	if [ "$result" != "OK" ];
	    then
	    #fuser -km $mountp
	    umount $mountp
	    echo "https://webdav.yandex.ru	$username	$password" > /etc/davfs2/secrets
	    mount.davfs -o uid=$owneruser https://webdav.yandex.ru $mountp
	fi
    fi
    fi
    done
sleep 20
done