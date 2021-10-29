# securitytrails_crawler
securitytrails是一个非常全面好用的子域名收集网站，注册登录后，可免费获取其能查到的全部子域名，但API存在限制，所以使用Selenium写了一个爬虫脚本获取子域名。
### tips
- **40行和41行添加账号密码**
- 最好添加--gpu参数，不容易出错
- 如果报错最好重试两次，可能会因为网络波动原因报错。
- 重复报错可以添加gpu参数查看卡在哪一步。
- 环境配置可以看https://github.com/Jarcis-cy/Google-Hacking-Crawler
