mkdir -p /home/seluser/Downloads
count=1
while true
count=$(($count + 1))
do
number_of_files=$(ls -la /home/seluser/Downloads | grep .pdf | wc -l)
if [ $number_of_files -gt 0 ]
then
rm -rf /home/seluser/Downloads/file_name
ls -la  /home/seluser/Downloads/ | grep .pdf |awk '{print $9}' > /home/seluser/Downloads/file_name
input="/home/seluser/Downloads/file_name"
unset filename
declare -a filename

while IFS= read -r line
do
  filename+=($line)
done < "$input"

for i in "${filename[@]}"; do
aws s3 cp /home/seluser/Downloads/$i  s3://selenium-repute/
rm -rf /home/seluser/Downloads/$i
echo $i copied and deleted
done
fi
rm -rf /home/seluser/Downloads/file_name
sleep 1
done
