# Spider

## Requests

```python
import requests
r = requests.get('url')
r.text  # html源代码
```

解析页面的方式

1. 正则表达式：适用于简单数据的匹配，如果匹配内容较复杂，正则表达式写起来会很绕，同时页面内容稍微变化，正则就会失效。
2. Lxml：专门用来解析XML格式文件的库，该模块用C语言编写，解析速度很快，和正则表达式速度差不多，但是提供了XPath和CSS选择器等定位元素的方法。
3. Beautiful Soup：一个 Python 实现的解析库，相比较于前两种来说，语法会更简单明了一点，文档也比较详细。唯一的一点就是运行速度比前两种方式慢几倍，当数据量非常大时相差会更多。

## Beautiful Soup

example.html

```html
<head>
   <meta charset="utf-8" />
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <title>Page Title</title>
</head>
<body>
   <div class='main-page'>
       <ul class='menu-list'>
               <li>首页</li>
               <li>新闻</li>
               <li>影视</li>
       </ul>
   </div>
</body>
</html>
```

```bash
>>>from bs4 import BeautifulSoup
>>>soup = BeautifulSoup('example.html', 'html.parser')  # 加载html文件
>>>soup.find('div')  # 找到div标签
'<div class="main-page">
<ul class="menu-list">
<li>首页</li>
<li>新闻</li>
<li>影视</li>
</ul>
</div>'

>>>soup.find_all('li') # 找到所有 li 标签
'[<li>首页</li>, <li>新闻</li>, <li>影视</li>]'

>>>for i in li:
   print(i.text)    #获取每个 li 标签的内容
'
首页
新闻
影视
'
```

https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/

