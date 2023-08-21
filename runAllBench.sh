python3 main.py -d mysql20-80 -t 130 -test mysql20-80.sh
sleep 200
python3 main.py -d wesql20-80 -t 130 -test wesql20-80.sh
sleep 50
python3 plot.py -d "wesql20-80 mysql20-80" -o "data20-80.csv"

sleep 200
python3 main.py -d mysql50-50 -t 130 -test mysql50-50.sh
sleep 200
python3 main.py -d wesql50-50 -t 130 -test wesql50-50.sh
sleep 50
python3 plot.py -d "wesql50-50 mysql50-50" -o "data50-50.csv"

sleep 200
python3 main.py -d mysql80-20 -t 130 -test mysql80-20.sh
sleep 200
python3 main.py -d wesql80-20 -t 130 -test wesql80-20.sh
sleep 50
python3 plot.py -d "wesql80-20 mysql80-20" -o "data80-20.csv"