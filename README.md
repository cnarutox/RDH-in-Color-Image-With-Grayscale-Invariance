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
<div class="half" align="center">
    <img src="lena.png" width="300">
    <img src="lena.modified.png" width="300"/>
</div>

### Implement Details
- ***Size***: 嵌入区域的高宽（左上角算起），默认为`None`即嵌入整张图片
- ***fig***: 图片地址或名称，默认为`'lena.png'`
- ***Dt***: 论文中的参数$D_t$，默认为`20`
- ***rhoT***: 论文中的参数$\rho_t$
- ***msg***: 嵌入的消息字符串，如`'314159265659314159265659'`

### Presentation
![img](img/幻灯片1.png)
![img](img/幻灯片5.png)
![img](img/幻灯片6.png)
![img](img/幻灯片7.png)
![img](img/幻灯片8.png)
![img](img/幻灯片9.png)
![img](img/幻灯片10.png)
![img](img/幻灯片11.png)
![img](img/幻灯片12.png)
![img](img/幻灯片13.png)
![img](img/幻灯片14.png)
![img](img/幻灯片15.png)
![img](img/幻灯片16.png)
![img](img/幻灯片17.png)
![img](img/幻灯片18.png)
![img](img/幻灯片19.png)
![img](img/幻灯片20.png)
![img](img/幻灯片21.png)
![img](img/幻灯片22.png)
![img](img/幻灯片23.png)
![img](img/幻灯片24.png)
![img](img/幻灯片25.png)
![img](img/幻灯片26.png)
![img](img/幻灯片27.png)
![img](img/幻灯片28.png)
![img](img/幻灯片29.png)
![img](img/幻灯片30.png)
![img](img/幻灯片31.png)
![img](img/幻灯片32.png)
![img](img/幻灯片33.png)
![img](img/幻灯片34.png)
![img](img/幻灯片35.png)
![img](img/幻灯片36.png)
![img](img/幻灯片37.png)
![img](img/幻灯片38.png)
![img](img/幻灯片39.png)
![img](img/幻灯片40.png)
![img](img/幻灯片41.png)
![img](img/幻灯片42.png)
![img](img/幻灯片43.png)
![img](img/幻灯片44.png)
![img](img/幻灯片45.png)
![img](img/幻灯片46.png)
![img](img/幻灯片47.png)
![img](img/幻灯片48.png)
![img](img/幻灯片49.png)
![img](img/幻灯片50.png)
![img](img/幻灯片51.png)
![img](img/幻灯片52.png)
![img](img/幻灯片53.png)
![img](img/幻灯片54.png)
![img](img/幻灯片55.png)
![img](img/幻灯片56.png)
![img](img/幻灯片57.png)
![img](img/幻灯片58.png)
![img](img/幻灯片59.png)
![img](img/幻灯片60.png)
![img](img/幻灯片61.png)
![img](img/幻灯片62.png)
![img](img/幻灯片63.png)
![img](img/幻灯片64.png)
![img](img/幻灯片65.png)
![img](img/幻灯片66.png)
![img](img/幻灯片67.png)
![img](img/幻灯片68.png)
![img](img/幻灯片69.png)
![img](img/幻灯片70.png)
![img](img/幻灯片71.png)
![img](img/幻灯片72.png)
![img](img/幻灯片73.png)
![img](img/幻灯片74.png)
![img](img/幻灯片75.png)
![img](img/幻灯片76.png)
![img](img/幻灯片77.png)
![img](img/幻灯片78.png)
![img](img/幻灯片79.png)
![img](img/幻灯片80.png)
![img](img/幻灯片81.png)
![img](img/幻灯片82.png)
![img](img/幻灯片83.png)
![img](img/幻灯片84.png)
![img](img/幻灯片85.png)
![img](img/幻灯片86.png)
![img](img/幻灯片87.png)
![img](img/幻灯片88.png)
![img](img/幻灯片89.png)
![img](img/幻灯片90.png)
![img](img/幻灯片91.png)
![img](img/幻灯片92.png)
![img](img/幻灯片93.png)
![img](img/幻灯片94.png)
![img](img/幻灯片95.png)
![img](img/幻灯片96.png)
![img](img/幻灯片97.png)

### Others
> Motivation: This is the final project of class **Information Security Foundation**
>
> Stars Wanted: If it can run on your machine, please **star** this project!
> 
> And there are some other related collected resources you may need, if you like you can buy me a coffee (>= 0.1￥) 😁 Thanks!
```shell
├─展示幻灯片.pptx
├─data-hiding-Lsb
├─data-hiding_1MSB
├─data-hiding_2MSB
├─data-hiding_histogram
│  ├─img
│  └─JPEG_Toolbox
├─High-capacity RDHEI based on extended run-length coding and block-based MSB plane rearrangement
│  └─测试图像
├─Kuo, W. C., & Kuo, S. H. (2012). Proceedings of the 2012 Seventh Asia Joint Conference on Information Security
│  ├─img
│  └─JPEG_Toolbox
├─Reversible Data Hiding in JPEG Image Based on DCT Frequency and Block Selection
│  ├─jpegread
│  ├─testimage
│  └─utils
├─Reversible Data Hiding Based on histogram shifting (4-8-16-32-internal correlation)
│  ├─imgs
│  ├─JPEG_Toolbox
│  └─result
├─Reversible Data Hiding Based on Two-Dimensional Histograms Modification
│  ├─代码（cheng's)
│  │  ├─imgs
│  │  └─JPEG_Toolbox
│  └─测容量（cheng's）
│      ├─imgs
│      └─JPEG_Toolbox
├─Reversible Data Hiding Based on Two-Dimensional Histograms Modification--improved by setting flag
│  ├─Jpeg_toolbox
│  └─具体代码
│      ├─代码
│      │  ├─imgs
│      │  └─JPEG_Toolbox
│      └─测容量
│          ├─imgs
│          └─JPEG_Toolbox
├─Reversible Data Hiding in Color Image with Grayscale Invariance
│  ├─Matlab implementation
│  │  ├─img
│  │  ├─old_version
│  └─readme
├─Reversible data hiding under inconsistent distortion metrics
├─signal processing
│  └─signal processing
├─书籍资料
└─多直方图
    └─多直方图
```
<div align="center"><img src="https://github.com/cnarutox/RDH-in-Color-Image-With-Grayscale-Invariance/blob/master/img/ailpay.png?raw=true" height=300</img></div>
