# Reversible Data Hiding in Color Image With Grayscale Invariance
> An implement based Python 3.6+ about [RDH in Color Image With Grayscale Invariance](http://home.ustc.edu.cn/~houdd/PDF/Reversible%20Data%20Hiding%20in%20Color%20Image%20with%20Grayscale%20Invariance.pdf) by *Dongdong Hou , Weiming Zhang , Kejiang Chen, Sian-Jheng Lin, and Nenghai Yu*
### Basic Introduction
- 首先安装所依赖的库`python3 install -r requirements.txt`
- 其次执行`python3 start.py`对图像进行加密解密
- 下面是执行时控制台样例输出
```python
[[231 133 116]
  [230 142 111]
  [232 135 111]
  ...
  [226 110  93]
  [221  99  86]
  [212  97  83]]]
=> Finish reading image!
=> Finish calculating predication error!
=> Message: 314159265659314159265659
=> Finish embeding msg with the critical value of ⍴ being 2
=> Finish embeding parameters:
        rhoT: 2, lastEc: 1, La: 193, N: 193, tagsCode: 0000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
=> Finish reading embeded image and calculating predication error!
=> Ensure the grayscale invariant: True
=> Finish extractig parameters:
        rhoT: 2, lastEc: 1, La: 193, N: 193, tagsCode: 0000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
=> Finish extracting received msg: 314159265659314159265659
=> The msg is equal to received msg: True
```
- 程序会生成并保存灰度对比图`Grayscale.png`
![Grayscale](Grayscale.png)
- 下面是程序加密前后的图片对比，可以看到人眼是很难看出来变化
<center>
    <img src="lena.png" width="300">
    <img src="lena.modified.png" width="300"/>
</center>

### Implement Details
- ***Size***: 嵌入区域的高宽（左上角算起），默认为`None`即嵌入整张图片
- ***fig***: 图片地址或名称，默认为`'lena.png'`
- ***Dt***: 论文中的参数$D_t$，默认为`20`
- ***rhoT***: 论文中的参数$\rho_t$
- ***msg***: 嵌入的消息字符串，如`'314159265659314159265659'`

### Others
> Motivation: This is the final project of class **Information Security Foundation**
> Stars Wanted: If you it can run on your machine, please **star** this project!