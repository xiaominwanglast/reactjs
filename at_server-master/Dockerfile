FROM dhub.2345intra.com/testteam/tower_base

COPY . .

ENV PYTHONUNBUFFERED 0

RUN pip install -r requestments.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    mv Tower/settings.online.py Tower/settings.py && \
    chmod a+x databaseapp/soar/* && \
	chmod +x entrypoint.sh

# 挂载附件
VOLUME /files

# 保留端口
EXPOSE 7890

ENTRYPOINT ["./entrypoint.sh"]