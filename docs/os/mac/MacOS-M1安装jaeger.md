# MacOS-M1安装jaeger

直接采用docker的方式进行安装，简单快捷。

1、打开命令行，下载镜像，执行：docker pull jaegertracing/all-in-one:latest

2、执行以下命令启动docker：

```
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14250:14250 \
  -p 14268:14268 \
  -p 14269:14269 \
  -p 9411:9411 \
  jaegertracing/all-in-one:latest
```

3、通过以下链接打开Web界面：http://localhost:16686

