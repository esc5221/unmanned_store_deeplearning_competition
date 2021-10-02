for img in ~/2.testset/*.jpg
do ./darknet detector test yolov4.data cfg/yolov4-tiny-custom.cfg ~/BEST_RESULT_backup/v4-t_98.4562.weights $img -dont_show
last=$(echo $img | cut  -d '/' -f5)
cp predictions.jpg predictions/P_$last
#echo $img
done
#./darknet detector test yolov4.data cfg/yolov4-tiny-custom.cfg ../BEST_RESULT_backup/v4-t_98.4562.weights  
