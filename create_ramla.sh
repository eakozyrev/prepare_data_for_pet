aread=1 #initial number to read
awrite=1  #initial number to write
pathwrite=ramla

while [ $aread -lt 3 ]
do
    echo $aread
    ramla=../anon/r00$aread\_WB_FDG_6R7/Img/r00$aread\_WB_FDG_6R7_50m-60m_dir-rml_4mm_RM_c1.img
    petview2interfile $ramla -floatii -ofo -of $pathwrite/ramla_$awrite\.i
    python plot.py $pathwrite/ramla_$awrite\.i $pathwrite/ramla_$awrite\.i.png
    awrite=`expr $awrite + 1`
    aread=`expr $aread + 1`
done
