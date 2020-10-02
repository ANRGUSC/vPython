#!/bin/sh
 
file_name=vpython
extension=".txt"
 
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
#echo "Current Time : $current_time"
 
new_fileName=$file_name$current_time$extension
#echo "New FileName: " "$new_fileName"

full_file_name=$file_name$extension

cp $full_file_name $new_fileName
#echo "You should see new file generated with timestamp on it.."

