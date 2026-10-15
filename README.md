```
# Python + AI 全栈学习项目

本仓库记录了从 Python 零基础到全栈 AI 应用开发的完整学习历程，包含 35+ 个练习文件和项目实战，涵盖 Python 基础、数据分析、大模型 API、LangChain Agent、RAG 知识库、Streamlit 前端、FastAPI 后端等完整技术栈。

## 🛠️ 技术栈

- **编程语言**：Python 3.12
- **数据处理**：Pandas、NumPy
- **数据可视化**：Matplotlib、Seaborn、Plotly
- **网络爬虫**：Requests、BeautifulSoup4
- **大模型**：智谱 AI、LangChain
- **AI 应用**：Agent 智能体、RAG 检索增强生成、工具调用
- **前端界面**：Streamlit
- **后端框架**：FastAPI、Uvicorn
- **版本控制**：Git、GitHub

## 📁 项目结构

## 🚀 核心项目

### 1. 电商销售数据分析系统
- 完整的数据分析流程：数据清洗 → 探索分析 → 可视化 → 业务洞察
- 涵盖销售趋势、地区对比、品类分析、用户画像等维度
- 输出完整分析报告和可视化图表

### 2. AI Agent 智能助手
- 基于 LangChain 的 ReAct 模式智能体
- 支持工具调用、多步推理、自主规划任务
- 具备数学计算、信息检索等能力

### 3. RAG 知识库问答系统
- 基于向量数据库的检索增强生成
- 支持上传文档，基于文档内容回答问题
- 结合 LangChain 和 Chroma 向量数据库

### 4. 全栈 AI 聊天应用
- **前后端分离架构**：Streamlit 前端 + FastAPI 后端
- 通过 HTTP 接口通信，标准 RESTful API
- 支持多轮对话记忆，无状态后端设计
- 自动生成 API 文档（Swagger UI）

## ⚡ 快速开始

### 环境准备

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的智谱 API Key
