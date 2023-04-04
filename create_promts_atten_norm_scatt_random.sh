#!/usr/bin/env bash

aread=1 #initial number to read
awrite=1  #initial number to write
pathwrite=promts_atten_norm_scatt_random
mkdir $pathwrite

while [ $aread -lt 3 ]
do
    echo $aread
    promt=$1/r00$aread\_WB_FDG_6R7/HImg/r00$aread\_WB_FDG_6R7_50m-60m_20x9_4mm_p.view.img
    ls $promt
    rand_sc=$1/r00$aread\_WB_FDG_6R7/HImg/r00$aread\_WB_FDG_6R7_50m-60m_20x9_4mm_sr.srview.img
    ls $rand_sc
    norm_att=$1/r00$aread\_WB_FDG_6R7/HImg/dircor_WB_FDG_6R7_r00$aread\_20x9_4mm.adgns_view.img
    ls $norm_att
    echo 'imagio_sum:'
    imagio_sum -scale 1 $promt -1 $rand_sc tmp.img
    echo 'imagio_prod:'
    imagio_prod -scale 1000 -exponent 1.0 tmp.img -1.0 $norm_att $pathwrite/promt_$awrite\.img
    petview2interfile $pathwrite/promt_$awrite\.img -floatii -ofo -of $pathwrite/promt_$awrite\.i
    python plot.py $pathwrite/promt_$awrite\.i $pathwrite/promt_$awrite\.i.png
    rm tmp.img
    aread=`expr $aread + 1`
    awrite=`expr $awrite + 1`

done
