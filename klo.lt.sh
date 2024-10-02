#!/bin/env bash
echo `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`
cd /mnt/sd3/record/klo.lt/
git pull
rm temp
pip3 install --user -r requirements.txt
# Update rss - update 08C
python3 update.py 08c
python3 merge.py 08c
python3 annotate.py 08c > record/08c/filter.txt
python3 export.py 08c `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update ASC
python3 update.py asc
python3 merge.py asc
python3 annotate.py asc > record/asc/filter.txt
python3 export.py asc `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update AYS
python3 update.py ays
python3 merge.py ays
python3 annotate.py ays > record/ays/filter.txt
python3 export.py ays `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update BLG
python3 update.py blg
python3 merge.py blg
python3 annotate.py blg > record/blg/filter.txt
python3 export.py blg `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update bts
python3 update.py bts
python3 merge.py bts
python3 annotate.py bts > record/bts/filter.txt
python3 export.py bts `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update ct4
python3 update.py ct4
python3 merge.py ct4
python3 annotate.py ct4 > record/ct4/filter.txt
python3 export.py ct4 `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update EXR
python3 update.py exr
python3 merge.py exr
python3 annotate.py exr > record/exr/filter.txt
python3 export.py exr `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update fcf
python3 update.py fcf
python3 merge.py fcf
python3 annotate.py fcf > record/fcf/filter.txt
python3 export.py fcf `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update fnf
python3 update.py fnf
python3 merge.py fnf
python3 annotate.py fnf > record/fnf/filter.txt
python3 export.py fnf `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update hsd
python3 update.py hsd
python3 merge.py hsd
python3 annotate.py hsd > record/hsd/filter.txt
python3 export.py hsd `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update inf
python3 update.py inf
python3 merge.py inf
python3 annotate.py inf > record/inf/filter.txt
python3 export.py inf `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update JST
python3 update.py jst
python3 merge.py jst
python3 annotate.py jst > record/jst/filter.txt
python3 export.py jst `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update nkw
python3 update.py nkw
python3 merge.py nkw
python3 annotate.py nkw > record/nkw/filter.txt
python3 export.py nkw `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update plr
python3 update.py plr
python3 merge.py plr
python3 annotate.py plr > record/plr/filter.txt
python3 export.py plr `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update pws
python3 update.py pws
python3 merge.py pws
python3 annotate.py pws > record/pws/filter.txt
python3 export.py pws `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update stp
python3 update.py stp
python3 merge.py stp
python3 annotate.py stp > record/stp/filter.txt
python3 export.py stp `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update tts
python3 update.py tts
python3 merge.py tts
python3 annotate.py tts > record/tts/filter.txt
python3 export.py tts `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update twc
python3 update.py twc
python3 merge.py twc
python3 annotate.py twc > record/twc/filter.txt
python3 export.py twc `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

# Update rss - update wbr
python3 update.py wbr
python3 merge.py wbr
python3 annotate.py wbr > record/wbr/filter.txt
python3 export.py wbr `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo `git status --porcelain` > temp
cat temp
if [[ "$temp" == "" ]]; then
    git add -A
    git commit -S -m "___ RSS FEED UPDATE "`TZ='<UTC+8>-8' date +'%b_%d,_%Y_%H:%M:%S'`" #bot_action"
    git push
fi

if [ ! -f `TZ='<UTC+8>-8' date +'/mnt/sd3/record/backup/klolt-%b%d_%Y.7z'` ]; then
    echo "Creating baseline archive: "`TZ='<UTC+8>-8' date +'/mnt/sd3/record/backup/klolt-%b%d_%Y.7z'`
    7z a -r `TZ='<UTC+8>-8' date +'/mnt/sd3/record/backup/klolt-%b%d_%Y.7z'` /mnt/sd3/record/klo.lt
fi
