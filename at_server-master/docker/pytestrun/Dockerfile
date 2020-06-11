FROM python:3.7
USER root
#更新
COPY requestments.txt requestments.txt
#添加依赖
RUN pip install -r requestments.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["/bin/sh"]