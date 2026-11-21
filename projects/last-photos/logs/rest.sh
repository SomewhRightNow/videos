cd /home/user/Filmler/last-photos
python3 logs/commons.py "STS-107 crew in orbit" 2>&1 | grep -v wait; cp research/commons.json research/commons4.json
python3 logs/commons.py "Challenger crew walkout" 2>&1 | grep -v wait; cp research/commons.json research/commons5.json
python3 logs/dl.py '[["research/commons1.json","Titanic Queenstown 1912 Browne",2,"titanic_cobh"],["research/commons3.json","Challenger STS-51-L liftoff",2,"sts51l"],["research/commons3.json","Challenger STS-51-L liftoff",7,"challenger_gpn"],["research/commons4.json","STS-107 crew in orbit",0,"columbia_crew"]]'
echo REST-DONE
