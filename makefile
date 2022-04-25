
main:
	python main.py -m=1


i:
	python main.py -m=2

# ssh -i "td.pem" ubuntu@ec2-18-222-146-46.us-east-2.compute.amazonaws.com

# scp -i "~/.ssh/td.pem" -r /Users/chenxinma/anaconda3/envs/td/lib/python3.7/site-packages/tdameritrade/ ubuntu@ec2-18-222-146-46.us-east-2.compute.amazonaws.com:/home/ubuntu/miniconda3/envs/td/lib/python3.8/site-packages

# scp -i "~/.ssh/td.pem" -r /Users/chenxinma/Documents/projects/td/code/ ubuntu@ec2-18-222-146-46.us-east-2.compute.amazonaws.com:/home/ubuntu/td/
# scp -i "~/.ssh/td.pem" -r /Users/chenxinma/Documents/projects/td/token/ ubuntu@ec2-18-222-146-46.us-east-2.compute.amazonaws.com:/home/ubuntu/td/
# scp -i "~/.ssh/td.pem" -r /Users/chenxinma/Documents/projects/td/data/fundamental ubuntu@ec2-18-222-146-46.us-east-2.compute.amazonaws.com:/home/ubuntu/td/data/
# scp -i "~/.ssh/td.pem" -r /Users/chenxinma/Documents/projects/td/data/symbols ubuntu@ec2-18-222-146-46.us-east-2.compute.amazonaws.com:/home/ubuntu/td/data/

# scp -i "~/.ssh/td.pem" -r /Users/chenxinma/Documents/projects/td/data/historical_daily/single ubuntu@ec2-18-222-146-46.us-east-2.compute.amazonaws.com:/home/ubuntu/td/data/historical_daily/

# scp -i "~/.ssh/td.pem" -r ubuntu@ec2-18-222-146-46.us-east-2.compute.amazonaws.com:/home/ubuntu/td/data/historical_daily/single/ /Users/chenxinma/Documents/projects/td/data/historical_daily/ 
# scp -i "~/.ssh/td.pem" -r ubuntu@ec2-18-222-146-46.us-east-2.compute.amazonaws.com:/home/ubuntu/td/data/historical_option_daily/single/ /Users/chenxinma/Documents/projects/td/data/historical_option_daily/
# scp -i "~/.ssh/td.pem" -r ubuntu@ec2-18-222-146-46.us-east-2.compute.amazonaws.com:/home/ubuntu/td/data/historical_option_daily/merge/ /Users/chenxinma/Documents/projects/td/data/historical_option_daily/
# scp -i "~/.ssh/td.pem" -r ubuntu@ec2-18-222-146-46.us-east-2.compute.amazonaws.com:/home/ubuntu/data.tar.bz2 /Users/chenxinma/Desktop/

# rsync -av — progress -e "ssh -i /Users/chenxinma/.ssh/td.pem" /Users/chenxinma/Documents/projects/td/code/ ubuntu@ec2-18-222-146-46.us-east-2.compute.amazonaws.com:/home/ubuntu/td/code/

# tar cfj data.tar.bz2 td/data/

# tar cfj data2.tar.bz2 td/data/historical_daily/single
# tar cfj data.tar.bz2 td/data/historical_option_daily/