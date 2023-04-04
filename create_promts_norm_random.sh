aread=1 #initial number to read
awrite=1  #initial number to write
pathwrite=promts_norm_random

while [ $aread -lt 3 ]
do
    echo $aread
    promt=../anon/r00$aread\_WB_FDG_6R7/HImg/r00$aread\_WB_FDG_6R7_50m-60m_20x9_4mm_p.view.img
    ls $promt
    rand=../anon/r00$aread\_WB_FDG_6R7/HImg/r00$aread\_WB_FDG_6R7_50m-60m_20x9_4mm_3_final.randview.img
    ls $rand
    norm=../anon/r00$aread\_WB_FDG_6R7/HImg/dircor_WB_FDG_6R7_20x9_4mm.0dgns_view.img
    ls $norm
    imagio_sum -scale 1 $promt -1 $rand tmp.img
    imagio_prod -scale 1000 -exponent 1.0 tmp.img -1.0 $norm $pathwrite/promt_$awrite\.img
    petview2interfile $pathwrite/promt_$awrite\.img -floatii -ofo -of $pathwrite/promt_$awrite\.i
    python plot.py $pathwrite/promt_$awrite\.i $pathwrite/promt_$awrite\.i.png
    rm tmp.img
    awrite=`expr $awrite + 1`
    aread=`expr $aread + 1`
done
