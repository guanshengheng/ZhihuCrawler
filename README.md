# ZhihuCrawler
主要使用selenium实现的简单爬虫程序，可用于爬取知乎某个问题下的全部回答
# 知乎爬虫

一个简单的知乎问答页面爬虫，用于抓取指定问题的所有回答内容。

## 功能特点

- 自动滚动加载所有回答
- 支持Cookie登录
- 自动保存到文本文件
- 反爬虫检测绕过

## 环境要求

```bash
pip install -r requirements.txt
```

## 配置文件

创建 `config.json` 文件：

```json
{
    "User-Agent": "替换为你浏览器的User-Agent字符串",
    "Cookie": "替换为你的知乎Cookie字符串"
}
```

> 💡 **获取方式**：
> - User-Agent：在浏览器开发者工具的Network选项卡中查看请求头
> - Cookie：登录知乎后在开发者工具的Application选项卡中复制

## 使用方法

1. 修改代码中的目标URL
2. 配置Cookie信息
3. 运行脚本

```python
python zhihu_crawler.py
```

## 输出

爬取的内容将保存到 `zhihu_content.txt` 文件中，包含：
- 问题标题
- 所有回答内容
- 回答总数统计

## 注意事项

- 请遵守知乎服务条款
- 建议设置适当的爬取间隔
- Cookie可能需要定期更新

Readme.md由Claude Sonnet 4生成，请注意甄别。如有问题可联系QQ：3406702953
