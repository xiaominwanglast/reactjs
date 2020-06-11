FROM alpine:3.8
USER root
#更新
COPY requestments.txt requestments.txt
RUN echo 'https://mirrors.aliyun.com/alpine/v3.8/main/' > /etc/apk/repositories && \
    echo '@community https://mirrors.aliyun.com/alpine/v3.8/community/' >> /etc/apk/repositories && \
    echo '@testing http://mirrors.aliyun.com/alpine/edge/testing' >> /etc/apk/repositories && \
    apk update && apk upgrade && \
    apk add tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone
#添加依赖
RUN apk add py2-pip && pip install -r requestments.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
CMD ["/bin/sh"]

#docker run -d -it -v $PWD/data:/var/data testimages2