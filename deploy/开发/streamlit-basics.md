---
title: Streamlit 基础入门
slug: streamlit-basics
description: Streamlit 数据应用框架的入门指南，包含安装、基本组件和简单应用示例
excerpt: 快速上手 Streamlit 构建数据应用
categories:
  - 开发
  - Python
  - 数据科学
tags:
  - streamlit
  - python
  - 数据应用
  - 快速入门
---

## Streamlit 简介

Streamlit 是一个开源 Python 框架，用于快速构建和分享数据应用。

### 特点
- 无需前端知识，纯 Python 编写
- 自动实时更新
- 丰富的组件库
- 易于部署和分享

### 适用场景
- 数据可视化
- 机器学习模型演示
- 数据分析工具
- 自动化报告

---

## 安装和配置

### 安装
```bash
# 使用 pip 安装
pip install streamlit

# 验证安装
streamlit --version

# 运行示例应用
streamlit hello
```

### 创建第一个应用
```bash
# 创建 Python 文件
echo 'import streamlit as st\nst.write("Hello, Streamlit!")' > app.py

# 运行应用
streamlit run app.py

# 在浏览器中打开
# http://localhost:8501
```

---

## 基础组件

### 文本显示
```python
import streamlit as st

# 标题
st.title("我的应用标题")
st.header("二级标题")
st.subheader("三级标题")

# 文本
st.text("普通文本")
st.markdown("**Markdown** 文本")
st.write("智能文本，支持多种数据类型")

# 代码
st.code("""
import streamlit as st
st.write("Hello")
""", language='python')

# Latex 公式
st.latex(r"e^{i\pi} + 1 = 0")
```

### 数据展示
```python
import pandas as pd
import numpy as np

# DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})
st.dataframe(df)

# 静态表格
st.table(df)

# 静态数据
st.json({"name": "John", "age": 30})

# 指标
st.metric("Total", "100", "+10%")
st.metric("Average", "50", "-5%")
```

### 图表
```python
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 折线图
x = np.linspace(0, 10, 100)
y = np.sin(x)
st.line_chart(y)

# 面积图
st.area_chart(y)

# 柱状图
st.bar_chart(y)

# Matplotlib 图表
fig, ax = plt.subplots()
ax.plot(x, y)
st.pyplot(fig)
```

---

## 输入组件

### 基本输入
```python
import streamlit as st

# 文本输入
name = st.text_input("输入你的名字")
st.write(f"你好, {name}!")

# 文本区域
text = st.text_area("输入多行文本")
st.write(text)

# 数字输入
age = st.number_input("输入年龄", min_value=0, max_value=120)
st.write(f"年龄: {age}")

# 日期输入
date = st.date_input("选择日期")
st.write(date)

# 时间输入
time = st.time_input("选择时间")
st.write(time)
```

### 选择组件
```python
# 下拉选择
option = st.selectbox(
    "选择你喜欢的语言",
    ["Python", "JavaScript", "Java"]
)
st.write(f"你选择了: {option}")

# 多选
languages = st.multiselect(
    "选择你掌握的语言",
    ["Python", "JavaScript", "Java", "Go"]
)
st.write(languages)

# 单选框
color = st.radio(
    "选择颜色",
    ("红色", "绿色", "蓝色")
)
st.write(f"你选择了: {color}")

# 复选框
agree = st.checkbox("我同意条款")
if agree:
    st.write("感谢同意!")
```

### 滑块和按钮
```python
# 滑块
value = st.slider("选择数值", 0, 100, 50)
st.write(f"数值: {value}")

# 范围滑块
range_values = st.slider("选择范围", 0, 100, (25, 75))
st.write(f"范围: {range_values}")

# 按钮
if st.button("点击我"):
    st.write("按钮被点击了!")

# 下载按钮
st.download_button(
    label="下载文件",
    data="文件内容",
    file_name="example.txt",
    mime="text/plain"
)
```

---

## 文件操作

### 文件上传
```python
import streamlit as st

# 上传单个文件
uploaded_file = st.file_uploader("上传文件", type=['csv', 'txt'])
if uploaded_file is not None:
    # 读取文件
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
    else:
        text = uploaded_file.getvalue().decode("utf-8")
        st.text(text)

# 上传多个文件
files = st.file_uploader("上传多个文件", accept_multiple_files=True)
for file in files:
    st.write(f"文件名: {file.name}")
```

### 下载文件
```python
import streamlit as st
import pandas as pd

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

# 下载 CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="下载 CSV",
    data=csv,
    file_name='data.csv',
    mime='text/csv'
)
```

---

## 布局

### 侧边栏
```python
import streamlit as st

# 添加侧边栏
st.sidebar.title("侧边栏")
st.sidebar.write("这里是侧边栏内容")

# 侧边栏输入
option = st.sidebar.selectbox("选择页面", ["主页", "关于", "联系"])
st.sidebar.write(f"当前页面: {option}")

# 根据选择显示内容
if option == "主页":
    st.title("欢迎来到主页")
elif option == "关于":
    st.title("关于我们")
elif option == "联系":
    st.title("联系我们")
```

### 分栏
```python
import streamlit as st

# 创建两列
col1, col2 = st.columns(2)

with col1:
    st.header("第一列")
    st.write("这里是第一列的内容")

with col2:
    st.header("第二列")
    st.write("这里是第二列的内容")

# 创建不等宽列
col1, col2, col3 = st.columns([3, 1, 1])
```

### 标签页
```python
import streamlit as st

tab1, tab2, tab3 = st.tabs(["数据", "图表", "设置"])

with tab1:
    st.title("数据")
    st.write("这里是数据内容")

with tab2:
    st.title("图表")
    st.write("这里是图表内容")

with tab3:
    st.title("设置")
    st.write("这里是设置内容")
```

---

## 进阶功能

### 缓存
```python
import streamlit as st
import pandas as pd
import time

@st.cache_data
def load_data():
    time.sleep(2)  # 模拟耗时操作
    return pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

data = load_data()
st.dataframe(data)

@st.cache_resource
def load_model():
    # 加载机器学习模型
    return model

model = load_model()
```

### 会话状态
```python
import streamlit as st

# 初始化会话状态
if "counter" not in st.session_state:
    st.session_state.counter = 0

# 使用会话状态
if st.button("增加计数"):
    st.session_state.counter += 1

st.write(f"计数: {st.session_state.counter}")

# 保存表单状态
if "form_key" not in st.session_state:
    st.session_state.form_key = ""

form = st.form("my_form")
input_text = form.text_input("输入文本")
submitted = form.form_submit_button("提交")
if submitted:
    st.session_state.form_key = input_text
    st.write(f"已保存: {st.session_state.form_key}")
```

### 进度条
```python
import streamlit as st
import time

# 进度条
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)
    time.sleep(0.01)

# 文本进度
status_text = st.empty()
for i in range(100):
    status_text.text(f"进度: {i}%")
    time.sleep(0.1)

# 旋转器
with st.spinner("正在处理..."):
    time.sleep(2)
st.success("完成!")
```

---

## 简单应用示例

### 数据分析仪表板
```python
import streamlit as st
import pandas as pd
import numpy as np

st.title("数据分析仪表板")

# 加载示例数据
@st.cache_data
def load_data():
    return pd.DataFrame({
        '产品': ['A', 'B', 'C', 'D'],
        '销售': [100, 150, 120, 180],
        '成本': [80, 120, 100, 150]
    })

df = load_data()

# 显示数据
st.subheader("原始数据")
st.dataframe(df)

# 计算利润
df['利润'] = df['销售'] - df['成本']
st.subheader("利润分析")
st.dataframe(df)

# 图表
st.subheader("销售图表")
st.bar_chart(df.set_index('产品')['销售'])

# 统计
st.subheader("统计信息")
st.metric("总销售额", df['销售'].sum())
st.metric("总利润", df['利润'].sum())
```

### 机器学习演示
```python
import streamlit as st
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

st.title("鸢尾花分类器")

# 加载数据
iris = load_iris()
X, y = iris.data, iris.target

# 侧边栏
st.sidebar.title("参数设置")
n_estimators = st.sidebar.slider("树的数量", 10, 100, 50)
max_depth = st.sidebar.slider("最大深度", 1, 10, 5)

# 训练模型
@st.cache_resource
def train_model(n_estimators, max_depth):
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth
    )
    model.fit(X, y)
    return model

model = train_model(n_estimators, max_depth)

# 预测界面
st.subheader("预测新样本")
sepal_length = st.number_input("花萼长度", 4.0, 8.0, 5.1)
sepal_width = st.number_input("花萼宽度", 2.0, 4.5, 3.5)
petal_length = st.number_input("花瓣长度", 1.0, 7.0, 1.4)
petal_width = st.number_input("花瓣宽度", 0.1, 2.5, 0.2)

# 预测
if st.button("预测"):
    prediction = model.predict([[
        sepal_length, sepal_width, petal_length, petal_width
    ]])[0]
    species = iris.target_names[prediction]
    st.success(f"预测结果: {species}")
```

---

## 部署

### 本地部署
```bash
# 运行应用
streamlit run app.py

# 指定端口
streamlit run app.py --server.port 8080

# 允许外部访问
streamlit run app.py --server.address 0.0.0.0
```

### Streamlit Cloud 部署
```bash
# 1. 将代码推送到 GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/yourapp.git
git push -u origin main

# 2. 访问 Streamlit Cloud
# https://share.streamlit.io

# 3. 连接 GitHub 仓库并部署
```

### Docker 部署
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

```bash
# 构建镜像
docker build -t streamlit-app .

# 运行容器
docker run -p 8501:8501 streamlit-app
```

---

## 最佳实践

### 1. 代码组织
```python
# main.py
import streamlit as st
from modules import data_loader, visualization

st.title("我的应用")
data = data_loader.load()
visualization.display(data)
```

### 2. 性能优化
```python
# 使用缓存
@st.cache_data
def expensive_function():
    # 耗时操作
    pass

# 减少重新渲染
st.form("my_form")
```

### 3. 用户体验
```python
# 添加说明
st.info("请按照步骤操作")

# 处理错误
try:
    # 你的代码
except Exception as e:
    st.error(f"发生错误: {e}")
```

---

## 常用组件速查

| 组件 | 用途 |
|------|------|
| `st.title()` | 主标题 |
| `st.header()` | 二级标题 |
| `st.write()` | 智能文本 |
| `st.dataframe()` | 数据表格 |
| `st.line_chart()` | 折线图 |
| `st.text_input()` | 文本输入 |
| `st.selectbox()` | 下拉选择 |
| `st.button()` | 按钮 |
| `st.sidebar()` | 侧边栏 |
| `st.columns()` | 分栏 |
| `st.tabs()` | 标签页 |
| `st.cache_data()` | 数据缓存 |
| `st.session_state` | 会话状态 |

---

## 总结

Streamlit 是构建数据应用的强大工具，主要优势：

- **简单快速**: 纯 Python，无需前端知识
- **实时更新**: 代码修改立即生效
- **丰富组件**: 满足各种需求
- **易于部署**: 一键部署到云端

开始使用 Streamlit，快速构建你的数据应用！
