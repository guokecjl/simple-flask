# simple-flask
a simple flask web server

### 拉取代码
```
git clone https://github.com/guokecjl/simple-flask.git
git submodule init  #初始化前端项目
git submodule update --remote #拉去前端最新代码
git submodule update #切换到当前位置对应的前端代码
```

### 创建运行环境
```
#创建虚拟环境
virtualenv venv

#启动虚拟环境
source venv/bin/activate

#安装包
pip3 install -r requirements.txt

#退出虚拟环境
deactivate venv/bin/activate
```

### 创建local_config.py
```
暂无
```

### 启动
```
python3 start.py
```

### demo
- 请求5000端口
