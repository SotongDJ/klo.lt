#!/bin/env bash
echo `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`
cd /store/record/klo.lt/
git pull
rm temp
# pip3 install -r requirements.txt

echo Update rss - update 08C
python3 update.py 08c
python3 merge.py 08c
python3 annotate.py 08c > record/08c/filter.txt
python3 export.py 08c `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update ASC
python3 update.py asc
python3 merge.py asc
python3 annotate.py asc > record/asc/filter.txt
python3 export.py asc `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update AYS
python3 update.py ays
python3 merge.py ays
python3 annotate.py ays > record/ays/filter.txt
python3 export.py ays `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update BLG
python3 update.py blg
python3 merge.py blg
python3 annotate.py blg > record/blg/filter.txt
python3 export.py blg `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update bts
python3 update.py bts
python3 merge.py bts
python3 annotate.py bts > record/bts/filter.txt
python3 export.py bts `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update ct4
python3 update.py ct4
python3 merge.py ct4
python3 annotate.py ct4 > record/ct4/filter.txt
python3 export.py ct4 `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update EXR
python3 update.py exr
python3 merge.py exr
python3 annotate.py exr > record/exr/filter.txt
python3 export.py exr `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update fcf
python3 update.py fcf
python3 merge.py fcf
python3 annotate.py fcf > record/fcf/filter.txt
python3 export.py fcf `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update fnf
python3 update.py fnf
python3 merge.py fnf
python3 annotate.py fnf > record/fnf/filter.txt
python3 export.py fnf `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update hsd
python3 update.py hsd
python3 merge.py hsd
python3 annotate.py hsd > record/hsd/filter.txt
python3 export.py hsd `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update inf
python3 update.py inf
python3 merge.py inf
python3 annotate.py inf > record/inf/filter.txt
python3 export.py inf `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update JST
python3 update.py jst
python3 merge.py jst
python3 annotate.py jst > record/jst/filter.txt
python3 export.py jst `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update nkw
python3 update.py nkw
python3 merge.py nkw
python3 annotate.py nkw > record/nkw/filter.txt
python3 export.py nkw `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update plr
python3 update.py plr
python3 merge.py plr
python3 annotate.py plr > record/plr/filter.txt
python3 export.py plr `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update pws
python3 update.py pws
python3 merge.py pws
python3 annotate.py pws > record/pws/filter.txt
python3 export.py pws `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update stp
python3 update.py stp
python3 merge.py stp
python3 annotate.py stp > record/stp/filter.txt
python3 export.py stp `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update tts
python3 update.py tts
python3 merge.py tts
python3 annotate.py tts > record/tts/filter.txt
python3 export.py tts `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update twc
python3 update.py twc
python3 merge.py twc
python3 annotate.py twc > record/twc/filter.txt
python3 export.py twc `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo Update rss - update wbr
python3 update.py wbr
python3 merge.py wbr
python3 annotate.py wbr > record/wbr/filter.txt
python3 export.py wbr `TZ='<UTC+8>-8' date +'d%y%m%dt%H%M'`

echo `git status --porcelain` > temp
cat temp
if [[ -s temp ]]; then
    git add -A
    git commit -S -m "___ RSS FEED UPDATE "`TZ='<UTC+8>-8' date +'%b_%d,_%Y_%H:%M:%S'`" #bot_action"
    git push
    git push github main
fi

# 7z u -up0q0r2x2y2z1w2
#     -u[-][p#][q#][r#][x#][y#][z#][!newArchiveName]
#         Update options
#         p	File exists in archive, but is not matched with wildcard
#             0	Ignore file (don't create item in new archive for this file)
#         q	File exists in archive, but doesn't exist on disk.
#             0	Ignore file (don't create item in new archive for this file)
#         r	File doesn't exist in archive, but exists on disk.
#             2	Compress (compress file from disk to new archive)
#         x	File in archive is newer than the file on disk.
#             2	Compress (compress file from disk to new archive)
#         y	File in archive is older than the file on disk.
#             2	Compress (compress file from disk to new archive)
#         z	File in archive is same as the file on disk
#             1	Copy file (copy from old archive to new)
#         w	Can not be detected what file is newer (times are the same, sizes are different)
#             2	Compress (compress file from disk to new archive)
full_backup=`TZ='<UTC+8>-8' date +'/store/record/backup/klolt-Full-%b_%Y.7z'`
if [ ! -f $full_backup ]; then
    echo "Creating baseline archive: "$full_backup
    7z u -up0q0r2x2y2z1w2 $full_backup /store/record/klo.lt/*
fi

# 7z u -u- -"up0q3r2x2y2z0w2!{incr_backup}"
#     -u[-][p#][q#][r#][x#][y#][z#][!newArchiveName]
#         Update options
#         p	File exists in archive, but is not matched with wildcard
#             0	Ignore file (don't create item in new archive for this file)
#         q	File exists in archive, but doesn't exist on disk.
#             3	Create Anti-item (item that will delete file or directory during extracting)
#         r	File doesn't exist in archive, but exists on disk.
#             2	Compress (compress file from disk to new archive)
#         x	File in archive is newer than the file on disk.
#             2	Compress (compress file from disk to new archive)
#         y	File in archive is older than the file on disk.
#             2	Compress (compress file from disk to new archive)
#         z	File in archive is same as the file on disk
#             0	Ignore file (don't create item in new archive for this file)
#         w	Can not be detected what file is newer (times are the same, sizes are different)
#             2	Compress (compress file from disk to new archive)
incr_backup=`TZ='<UTC+8>-8' date +'/store/record/backup/klolt-Incr-%b%d_%Y.7z'`
if [ ! -f $incr_backup ]; then
    echo "Creating baseline archive: "$incr_backup
    7z u -u- $full_backup /store/record/klo.lt/* -"up0q3r2x2y2z0w2!"`TZ='<UTC+8>-8' date +'/store/record/backup/klolt-Incr-%b%d_%Y.7z'`  
fi
