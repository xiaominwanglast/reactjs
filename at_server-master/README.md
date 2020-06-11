### 概述
这是提测平台的项目

### 启动命令
docker run -d --name=tower --restart=always -p 7890:7890 -v /data/tower/files:/opt/app/files 172.17.1.10/testteam/tower
> 先执行下面删除命令

### 删除命令
docker rm -f tower

### 机器
172.17.1.54


```
windows
set CL=-FI"C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\include\stdint.h"


Problem is solved by editing string in crypto\Random\OSRNG\nt.py:

import winrandom
to
from . import winrandom


```