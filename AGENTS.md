# AGENTS.md —— AI 代理协作规范

> 本文件约束所有协助本项目开发的 AI（包括 Claude Code、Cursor 等）的行为。
> 项目：校园资料智能问答助手（基于 RAG，LangChain + FastAPI）。
> 团队：4 名大三学生（代码初学者），本文件中的规则都是为了**让代码能被讲清楚、能对上老师 PPT、能顺利通过答辩**。

---

## 一、项目简介

一个基于 RAG（检索增强生成）的校园资料问答网页应用：

- 前端：原生 HTML/CSS/JS（`static/index.html`）
- 后端：Python + FastAPI（`main.py`）
- RAG 链路：`app/rag/`（加载→切分→向量化→存储→检索）
- 模型层：`app/llm/`（大模型接入 + 提示词 + 多轮记忆）

**核心原则：本项目是课程实训，代码要"简单、能讲、对上老师教的写法"。**

---

## 二、最高优先级规则（违反即重写）

1. **代码必须简单易懂**。团队成员和组长都是代码初学者，答辩时老师会逐行问代码。
2. **严格按老师 PPT 的 LangChain 写法来**（主要是 Part 6-LangChain.pdf）。导入路径、参数名、调用顺序都要和老师示例一致，不能自创"更高级"的写法。
3. **用中文注释**，分步标注每个环节（`# 1. 导包` `# 2. 创建对象` `# 3. 执行` `# 4. 输出`）。
4. **只做需求范围内的事**，不过度设计、不引入非必要功能。

---

## 三、技术约束（禁止事项）

以下内容**明确不做**，不要主动引入：

- ❌ 不引入 MySQL / PostgreSQL 等关系型数据库（多轮记忆用内存列表，见 `app/llm/memory.py`）
- ❌ 不引入工具调用型 Agent（ReAct）、LangGraph 工作流、Chains
- ❌ 不引入 Rerank 重排
- ❌ 不引入前端框架（Vue / React），只用原生 HTML/CSS/JS
- ❌ 不引入新的第三方库（除非用户明确要求，且要在 `requirements.txt` 里登记版本）
- ❌ 不写 lambda 嵌套、复杂列表推导、装饰器、元类、生成器高级用法
- ❌ 不过度使用类型注解、不用抽象基类/工厂模式等"工程化"设计

---

## 四、代码风格规范

### 4.1 Python

- 优先 `for` 循环 + `if/else`，显式声明变量，别炫技。
- 每个环节配一条中文注释，说明"这一步在干什么"。
- 函数名用 `snake_case`，类名用 `PascalCase`，和现有代码保持一致。
- 每个文件开头加 `# -*- coding: utf-8 -*-` 和一句模块说明 docstring。

### 4.2 LangChain API 清单（写代码照这个来，已验证）

| 用途 | 正确写法 |
|---|---|
| 文档加载 | `from langchain_community.document_loaders import TextLoader`；`TextLoader(path, encoding="utf-8").load()` |
| 文本切分 | `from langchain_text_splitters import RecursiveCharacterTextSplitter`；参数 `separators=["\n\n","\n","。","！","？","，"," ",""]`、`chunk_size`、`chunk_overlap`；用 `split_documents(docs)` |
| 嵌入 | `from langchain_openai import OpenAIEmbeddings`；参数 `model` / `api_key` / `base_url` / `check_embedding_ctx_length=False`（bge 模型必须加 False） |
| 写入向量库 | `Chroma.from_documents(documents=, embedding=, persist_directory=)`（参数名是 **embedding**） |
| 读取向量库 | `Chroma(persist_directory=, embedding_function=)`（参数名是 **embedding_function**，两处不同！） |
| 检索 | `db.similarity_search(query, k=k)` 返回 Document 列表，取 `.page_content` |
| 大模型 | `from langchain_openai import ChatOpenAI` |

> 注意：不要用旧版 LangChain 的 `openai_api_key` 参数名，老师教的是 `api_key`/`base_url`。

### 4.3 前端

- 保持原生 HTML/CSS/JS 风格，和现有 `static/index.html` 一致。
- 变量/函数命名清晰，关键函数加中文注释。

---

## 五、目录与分工约定

| 目录/文件 | 负责人 | 说明 |
|---|---|---|
| `app/rag/` | 组长 李政达 | RAG 核心链路 |
| `app/llm/` | 王皓阳 | 大模型接入 + 提示词 + 多轮记忆 |
| `main.py` + `app/api/` + `app/models/` | 谭存林 | FastAPI 入口、接口路由、数据模型 |
| `static/` + `data/` | 高星晨 | 前端页面、校园资料收集 |

改代码时**先读一遍对应目录现有代码**，保持命名和风格一致，不要另起炉灶。

---

## 六、安全与 Git 规范

1. **绝不把密钥写进代码**：API Key 一律读环境变量（`os.getenv(...)`），配置放 `.env`。
2. **绝不提交敏感文件**：`.env`、`__pycache__/`、`.idea/`、`chroma_db/` 已在 `.gitignore`，不要强行 `git add` 它们。
3. 不要主动执行 `git commit` / `git push`，除非用户明确要求。

---

## 七、当前已知待办（AI 应优先协助解决）

1. `main.py` 的 `/chat` 仍是占位代码，需接入 `app/rag.retriever.retrieve()` + `app/llm.generator.generate()`。
2. `app/llm/llm.py` 的 `get_llm()` 走的是硅基流动接口，需统一为 DeepSeek 官方接口（与 `.env.example` 一致），详见 `docs/SPEC.md` 第五节。
3. 前端 `index.html` 未传 `session_id`，多轮记忆尚未打通。
4. `app/rag/embedding.py` 与 `app/llm/embeddings.py` 有重复的 `get_embeddings()`，建议合并。

---

## 八、沟通要求

- 对用户（学生）解释时，用通俗语言，给出**具体操作步骤**而非只讲原理。
- 每次改动后，用一两句话说明"改了什么、为什么、怎么验证"。
- 不要一次塞给用户过多新概念，循序渐进。
