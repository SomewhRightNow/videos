cd /home/user/Filmler/mil1/photos
UA="SomewhereRightNowBot/1.0 (https://www.youtube.com/@somewhrightnow)"
declare -A P=( [stadium]="5/5e/Gate_7_tribute%2C_Olympiacos_-_Xanthi_3-1_%282019-20%29.jpg" )
for i in $(seq 1 15); do
  c=$(curl -s -o /dev/null -w "%{http_code}" -A "$UA" "https://upload.wikimedia.org/wikipedia/commons/8/8d/Omari_Hutchinson_22122025_%281%29.jpg")
  if [ "$c" = "200" ]; then echo OPEN; exit 0; fi
  sleep 60
done
echo STILL_BLOCKED
