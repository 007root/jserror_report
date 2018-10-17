# jserror
为了开发方便高效的查看错误日志,提取关键日志同步到到数据库,并用程序展示出来.

# 日志同步 
```
    python backend/rsync_log.py
```

# 服务启动 
使用supervisor或者forever启动 backend/server.py

# nginx配置 
```
server {
        listen  80;
        server_name example.com;

        location /report {
                alias /home/ubuntu/code/jserror/frontend/;
        }
        location /src {
                alias /home/ubuntu/code/jserror/frontend/src/;
        }
        location / {
                proxy_pass http://192.168.4.55:6666;
        }
}
```

# 界面显示

![_20181017091650](https://user-images.githubusercontent.com/20102314/47056158-a7f36280-d1ed-11e8-9cd4-ae8bc8eae1fe.png)
