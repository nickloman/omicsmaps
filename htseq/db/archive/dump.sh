PYTHONPATH=/home/nick/maps:/home/nick/maps/htseq DJANGO_SETTINGS_MODULE="htseq.settings"
export PYTHONPATH DJANGO_SETTINGS_MODULE
export DB_FROM_ARGV="yes"

python dump.py 2010-03-21T00:00.sqlite "2010-03-21" >full_dump.txt
python dump.py 2010-06-06T00:00.sqlite "2010-06-06" | tail -n +2 >>full_dump.txt
python dump.py 2010-09-05T00:00.sqlite "2010-09-05" | tail -n +2 >>full_dump.txt
python dump.py 2010-12-05T00:00.sqlite "2010-12-05" | tail -n +2 >>full_dump.txt
python dump.py 2011-01-02T00:00.sqlite "2011-01-02" | tail -n +2 >>full_dump.txt
python dump.py 2011-04-03T00:00.sqlite "2011-04-03" | tail -n +2 >>full_dump.txt
python dump.py 2011-07-03T00:00.sqlite "2011-07-03" | tail -n +2 >>full_dump.txt
python dump.py 2011-10-02T00:00.sqlite "2011-10-02" | tail -n +2 >>full_dump.txt
python dump.py 2012-01-01T00:00.sqlite "2012-01-01" | tail -n +2 >>full_dump.txt
python dump.py 2012-07-20T00:00.sqlite "2012-07-20" | tail -n +2 >>full_dump.txt
