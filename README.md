# EasyDailyPicture
将后端生成的期货点位图片展示到前端

# 启动
nohup /home/stock/anaconda3/envs/stock/bin/uwsgi uwsgi_easy_daily_picture.ini > /dev/null 2>&1 &

# 启动报错
/home/stock/anaconda3/envs/stock/bin/uwsgi: error while loading shared libraries: libssl.so.1.1: cannot open shared object file: No such file or directory

编辑.bashrc
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/home/stock/anaconda3/envs/stock/lib

