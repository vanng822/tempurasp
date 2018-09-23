temp=$(sudo vcgencmd measure_temp)
if [ "$temp" != "" ]; then
	temp=$(echo $temp | cut -d'=' -f2 | cut -d"'" -f1)
fi
$(echo $temp > /tmp/gpu_temp)
