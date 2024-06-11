# Baseline

简体中文 | [English](README_en.md)

用法：
```bash
bash run.sh
```

docker: <br/>
Driver Version: 535.104.05<br/>
```bash
docker pull registry.cn-hangzhou.aliyuncs.com/clg_test/aigc_det:1.0
docker run -it -d --cpus=12 -m 24g -v /src:/tar registry.cn-hangzhou.aliyuncs.com/clg_test/aigc_det:1.0
docker exec -it [CONTAINER ID] bash
```


## 参赛规范 <br/>
1) 工程开发目录需要在/workspace/AIGCDetectBaseline/目录下, 启动脚本固定使用run.sh, 提交镜像中需使用baseline中的main.py. main.py需保持和baseline一致. <br/>
2) 提交方案中请合理安排日志打印输出内容.<br/>
3) 平台提供了基于镜像地址提交镜像的方式, 将本地镜像推送至阿里云容器镜像仓库或者Dockerhub后, 设置为公开镜像, 在比赛平台提交页面中输入镜像地址. 由比赛平台拉取镜像运行, 运行结束即可在成绩页面查询评测结果. 推送至阿里云容器镜像仓库或者Dockerhub时, 镜像仓库名称尽量不关联上比赛相关的词语, 以免被检索从而泄漏.<br/>
4) 运行镜像时，容器内任何网络不可用，请将依赖的软件、包在镜像中装好. <br/>
5) 为了合理分配资源单次提交运行时间不能超过1个小时，超出后程序自动停止，结果将不被接受.<br/>
6) 确保镜像中cp指令可用.<br/>
7) Docker镜像大小请尽量勿超过16G, 上传镜像中请勿包含数据集.<br/>
<br/>


## 部分公开数据链接
参赛者使用开源数据集训练模型。<br/>
开源训练数据集：<br/>
CNNDetection: https://github.com/peterwang512/CNNDetection <br/>
Sentry: https://github.com/Inf-imagine/Sentry <br/>
参赛者可以使用其它开源数据集或者组织自己的训练数据 <br/>


## 资源配置：<br/>
CPU: 12vCPU <br/>
内存: 24 GiB <br/>
GPU: Nvidia RTX 3090, Driver Version: 470.82.01, 显存开销在16G以内 <br/>
<br/>


## 阿里云镜像仓库使用方法:<br/>
1) 注册阿里云账户: https://cr.console.aliyun.com/cn-hangzhou/instances. <br/>
2) 在工作台搜索[容器镜像服务], 进入后选择[个人实例]. <br/>
3) 创建镜像仓库、命名空间, 设置仓库名称，选择公开或私有仓库(此处选择公开),  选择本地仓库. <br/>
4) 本地登录阿里云Docker Registry示例: <br/>
```bash
$ docker login --username=[阿里云id] registry.cn-hangzhou.aliyuncs.com
$ docker tag [ImageId] registry.cn-hangzhou.aliyuncs.com/xx1/xx2:[镜像版本号]
$ docker push registry.cn-hangzhou.aliyuncs.com/xx1/xx2:[镜像版本号]
请根据实际镜像信息替换示例中的[阿里云id], [ImageId]和[镜像版本号]参数.
```
5) 在比赛提交页面提交: registry.cn-hangzhou.aliyuncs.com/xx1/xx2:[镜像版本号].
<br/>

## Reference <br/>
This baseline is mainly inspired by [WisconsinAIVision/UniversalFakeDetect](https://github.com/WisconsinAIVision/UniversalFakeDetect).
<br/>