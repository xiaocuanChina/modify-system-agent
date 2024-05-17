# 免责声明

本程序服务器的地理位置获取所采用的GeoLite2-City.mmdb数据集由第三方提供，其对台湾及香港的划分可能与某些政治立场或观点不符。

该数据集仅供参考，不代表本程序或开发者对某种政治立场的支持或认可。

用户在使用本程序提供的地理位置信息时，应自行判断其准确性并承担相应风险。

尽管我们已经尽力确保数据集的准确性，但地理位置的划分可能存在误差或不完整。



# GeoLite2-City.mmdb更新

> 当前使用的版本：GeoLite2-City_20240507.tar.gz（周二）
>
> 需要下载的为：GeoLite2 City

这个依赖于GeoLite2-City.mmdb数据集，GeoLite2-City.mmdb数据集的更新比较频繁（每周二、周五更新），需要保持最新的请点击下方的下载地址下载最新的数据集

## 方法1

[数据库下载地址，需要登录](https://www.maxmind.com/en/accounts/current/geoip/downloads)

## 方法2

1. 登录获取自己的[许可证](https://www.maxmind.com/en/accounts/current/license-key)
2. 创建自己的许可证，并获取GeoIP.conf文件
3. 点击[永久下载地址](https://download.maxmind.com/geoip/databases/GeoLite2-City/download?suffix=tar.gz)
4. 输入GeoIP.conf中的AccountID和LicenseKey
5. 即可下载最新的文件了



## 如何替换

通过上方的方式下载GeoLite2-City_*.tar.gz文件，解压缩获取GeoLite2-City.mmdb文件，将该文件替换到data目录下即可





# 页面
![PixPin_2024-05-10_09-38-57](https://github.com/xiaocuanChina/modify-system-agent/assets/113506112/97dbf4c7-8bba-4f3e-9a7f-916c2506e031)


- 本机IPv4地址

    这个一般在需要获取自己的局域网IP时可以使用

- 代理服务器信息

    > 部分代理软件会将本机代理端口和局域网代理端口设置为不同的，所以这里复制的仅限于本机使用，局域网的端口需要见自己代理软件配置的端口

    在其他软件中如果需要知道自己的代理服务器的话可以通过复制该IP来直接获取自己本机使用的代理服务器

    - 调整代理服务器

        点击之后会切换为文本框，并且刷新按钮会变成保存按钮，在输入完需要配置的IP地址以及端口之后，点击【刷新】位置的保存就可以修改本机的代理服务器信息了

- 当前代理状态（故事的开始）

    > 当初就是为了快速设置这个才编写的程序,其实你win+i键然后搜索【代理】，点击之后右侧菜单会有一个【使用代理服务器】，你改他一样的

    顾名思义，就是你系统代理服务器是否启用，如果是关的话你就访不了外网了

- 当前测试的URL

    - 这个URL适用于【检测延时】和【连接时长】

    - 如果使用的代理软件为[v2rayN](https://github.com/2dust/v2rayN)，可使用方法二，其他的话只要代理软件的配置文件是json文件也可以配置

    - 如何配置？
        - 方法一
            - 前提是localJsonConfigurationFileURL为空

            - 修改config.json文件的testConnectionTimeUrl值即可

        - 方法二
            - 配置config.json的localJsonConfigurationFileURL和localJsonConfigurationItem

            - localJsonConfigurationFileURL就是你本地配置文件（json）的路径

            - localJsonConfigurationItem就是你代理软件的配置文件（json）中延时检测地址的层级

- 服务器IP

    ***从这里开始，下方的所有按钮在点击之后都会隐藏，并且整个程序在按钮显示之前无法进行点击<br/>这样设计为了防止请求多次导致程序卡死而关闭程序<br/>这个问题我会想办法解决的***
    
    > 以前老版本的时候没有显示这个IP，每次获取地址的时候都要通过网络访问一次，会比较慢
    >
    > 点击刷新IP地址即可获取最新的地址
    
    这里的服务器IP指的是你的代理服务器所在的ip
    
- 检测平均延时

    - 默认检测2次延时，取平均值
    - 检测次数可在config.json中修改

- 服务器地理位置

    > 这个虽然可以查看节点位置，但是因为要请求网络，所以说你在点击按钮之后我会将按钮隐藏，并且这个时候因为处于请求状态，窗口是不能动的（也点不了），隐藏按钮也是为了防止用户多次点击导致窗口卡死
    >
    > 因为要走网络请求，所以如果节点很差的话，请求会很慢，我这边到时候设置个超时，防止卡死

    这个适用于当你的节点属于野生的节点的时候，但是你又想知道你的这个节点是哪个国家的时候可以使用这个

- 欺诈分值

    申请API是可选操作，只要目前scamalytics还未对我发出警告，就可以不使用API

    > 目前使用的是[scamalytics](https://scamalytics.com/)
    >
    > - ***通过py截取https://scamalytics.com/ip/{ip}页面的Fraud Score元素来获取分数***
    > - ***如通过py直接获取网页的信息不符合网站条款的话的请联系我，我会删除相关代码***
    >
    > ![](https://scamalytics.com/wp-content/uploads/2016/06/Scamalytics-Logo-No-Strapline-Transparent-738x150.png)
    >
    > 
    >
    > - 现在我已经拥有了官方API了，每月5000的额度
    >     - 因为官方API的每月额度有限，目前不考虑提供我自己的API，需要的可以自己上官网[申请使用](https://scamalytics.com/ip/api/enquiry?monthly_api_calls=5000)
    >
    > - 在申请成功之后查看自己的连接
    >
    >     - 先阅读官方发的邮箱内容，其中带API文档附件，官方的免费服务不提供技术支持
    >
    >     - api请求格式如下
    >
    >         - https://<hostname>/<username>/?ip=<ip>&key=<key>
    >
    >         - 仅需复制username和key到config.json文件即（详情配置见【config.json】，就在这个README文件下面有解释）
    >
    > ---
    >
    > - ***Get the score by intercepting the Fraud Score element of the https://scamalytics.com/ip/{ip} page via py***
    >
    > - ***If you do not comply with the terms and conditions of the website, please contact me, I will remove the code.***
    >
    > 
    >
    > - Now I have the official API, the monthly quota of 5000
    >     - Because of the limited monthly quota of the official API, I don't consider providing my own API at the moment, if you need it, you can go to the official website [apply for use](https://scamalytics.com/ip/api/enquiry?monthly_api_calls=5000).
    >
    > - Check your connection after successful application
    >
    >     - First read the official email content, which is attached with the API document, the official free service does not provide technical support
    >
    >     - The api request format is as follows
    >
    >         - https://<hostname>/<username>/?ip=<ip>&key=<key>
    >
    >         - just copy the username and key to the config.json file that is (details of the configuration see [config.json], in this README file below the explanation)
    >
    > 
    >

评估节点安全状态的一种指标
如果你需要输入一些隐私的内容，你可以通过这个检测该节点是否安全，分数越低越安全

- 批量替换节点名称

    按照页面提示输入对应信息可实现批量替换服务器节点名称

    替换后的内容会保存至粘贴板以及同级目录下的nodeMsgs目录中

    可通过numberOfReservedNodeFiles来设置保存文件的数量（见config.json）



- ~~连接时长~~

    > ~~同样，因为这个也是请求了网络，所以这个按钮在点击了之后我也做了隐藏~~

    ~~这个不是网络延时，是你连接到目标地址所需要花费的时长（就是你在浏览器输入网址，从回车到你可以点击网址的大致时间）~~

    

# config.json

-  testConnectionTimeUrl

    - 测试连接时长的路径

- timeout

    - 连接时长超时时长设置

- default_proxy_server

    -  默认服务器地址

- default_proxy_proxy

    -  默认的服务器端口

- number_of_test_delays

    -  延时检测次数

- localJsonConfigurationFileURL

    > 读取配置文件的作用是使代理检测地址和测试连接时长的路径一致，

    - 如果本地存在代理的配置文件（限json格式），可以选择直接读取本地文件这里填本地代理配置文件的路径

- localJsonConfigurationItem

    - json文件的key路径（如果localJsonConfigurationFileURL配置了，这个也需要配置）

- scamalyticsuUserName

    -  用于检测欺诈分值API（详情见【页面】-【欺诈分值】）的用户名

- scamalyticsuKey

    -  用于检测欺诈分值API（详情见【页面】-【欺诈分值】）的key
    
- numberOfReservedNodeFiles

    > 使用批量替换之后会将数据自动存入到系统粘贴板，也会在本地生成一个服务器节点的txt文件，便于二次修改
    
    -  保留批量替换服务器名称的文件数量



# 我看别人加了我也加一个 Star History

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xiaocuanChina/modify-system-agent&type=Date&theme=dark" />
  <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xiaocuanChina/modify-system-agent&type=Date" />
  <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xiaocuanChina/modify-system-agent&type=Date" />
</picture>

