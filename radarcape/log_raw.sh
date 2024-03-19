pkill nc
DIRNAME="data-"$(date +"%Y-%m-%d-%H-%M-%S")
echo $DIRNAME
mkdir $DIRNAME
cd $DIRNAME
nc -C radarcape.local 30003 | grep -a MSG,[13] | split -l1000 -a4 -d --additional-suffix=.csv

