# 校园资料智能问答助手

基于 RAG（检索增强生成）技术的校园资料问答系统。用户通过网页提问，系统先从校园资料文档中检索相关内容，再交给大模型生成准确回答，解决大模型"知识缺失、答非所问、胡说八道（幻觉）"的问题。

## 一、技术栈

| 部分 | 技术 |
|---|---|
| 语言 | Python 3.12 |
| 后端框架 | FastAPI |
| AI 框架 | LangChain |
| 大模型 | DeepSeek API |
| 嵌入模型 | 硅基流动（免费 embedding） |
| 向量数据库 | Chroma（本地） |
| 前端 | 原生 HTML + CSS + JavaScript |

## 二、目录结构

```
campus_rag/
├── main.py            # FastAPI 入口（谭存林）
├── requirements.txt   # 依赖列表
├── .env.example       # 密钥模板（复制成 .env 使用）
├── static/
│   └── index.html     # 前端聊天页（高星晨）
├── data/
│   └── *.txt           # 校园资料文档（高星晨收集，共5份：图书馆/校园卡/选课/学费/宿舍报修）
└── app/
    ├── rag/           # RAG 核心链路（组长）
    ├── llm/           # 模型接入+提示词+记忆（王皓阳）
    ├── api/           # 接口路由（谭存林）
    └── models/        # 数据模型（谭存林）
```

## 三、开发环境搭建（PyCharm）

### 1. 用 conda 创建虚拟环境

打开 Anaconda Prompt（或 PyCharm 终端），执行：

```bash
# 创建名为 campus_rag 的 Python 3.12 环境
conda create -n campus_rag python=3.12 -y

# 激活环境
conda activate campus_rag
```

### 2. 安装依赖

先配置国内镜像源（加速下载）：

```bash
pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/
```

然后在本项目目录下执行：

```bash
pip install -r requirements.txt
```

### 3. 配置密钥

1. 把 `.env.example` 复制一份，改名为 `.env`
2. 填入你的密钥：
   - DeepSeek：到 https://platform.deepseek.com/ 注册并申请 API Key（需少量充值）
   - 硅基流动：到 https://siliconflow.cn/ 注册，有免费额度

### 4. 用 PyCharm 打开项目

1. 打开 PyCharm → `File → Open` → 选择本项目文件夹 `campus_rag`
2. 配置解释器：`File → Settings → Project → Python Interpreter → Add Interpreter → Conda Environment → 选择刚创建的 campus_rag 环境`
3. 等待 PyCharm 识别完环境

### 5. 启动后端

在 PyCharm 里右键 `main.py` → `Run`，或终端执行：

```bash
python main.py
```

看到启动成功后，浏览器打开 http://127.0.0.1:8000/docs 能看到自动生成的接口文档。

### 6. 打开前端

直接双击 `static/index.html` 用浏览器打开，输入问题点击发送即可（后端必须已启动）。

## 四、Git 协作规范

1. 每个人在自己的分支上开发，不要直接在 main/master 上改
2. 提交前先 `git pull` 拉取最新代码
3. 提交说明写清楚改了什么（如"新增文档加载功能"）
4. 不要提交 `.env`（含密钥）、`__pycache__`、`.idea`、`chroma_db/`（已在 .gitignore 里排除）

## 五、分工速览

| 成员 | 负责 |
|---|---|
| 组长 | RAG 核心链路 + 项目文档 + Git 管理 + 答辩 |
| 谭存林 | FastAPI 后端接口 + 数据模型 + 接口联调测试 |
| 王皓阳 | 大模型接入 + 提示词 + 多轮记忆 |
| 高星晨 | 前端页面 + 校园资料收集 |
