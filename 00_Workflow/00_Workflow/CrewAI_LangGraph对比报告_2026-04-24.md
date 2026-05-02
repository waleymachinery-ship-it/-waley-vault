# CrewAI vs LangGraph 多Agent协作框架对比报告

**伟力机械三AI系统优化研究**  
**日期：** 2026-04-24  
**环境：** Python 3.13, CrewAI 1.14.2, LangGraph 1.1.9

---

## 1. 框架概述与核心概念

### CrewAI

CrewAI 是一个**以角色为中心**的多Agent编排框架，其设计理念源自"人类团队协作"的隐喻。

```
┌─────────────────────────────────────────────────────────┐
│                        Crew                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  Agent   │  │  Agent   │  │  Agent   │              │
│  │ (Role)   │  │ (Role)   │  │ (Role)   │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │             │             │                    │
│       └─────────────┼─────────────┘                    │
│                     ▼                                  │
│              Process (Sequential/Hierarchical)         │
└─────────────────────────────────────────────────────────┘
```

**核心概念：**
- **Crew（团队）：** 多个Agent的集合，协同完成复杂任务
- **Agent（智能体）：** 由Role/Goal/Backstory定义的角色
- **Task（任务）：** 具体的工作单元，分配给Agent执行
- **Process（流程）：** 定义Agent间协作方式（顺序/层级）
- **Tools（工具）：** Agent可调用的外部能力

### LangGraph

LangGraph 是 **以状态流为中心** 的图执行框架，源自LangChain生态，强调**有向状态机**的建模方式。

```
┌─────────────────────────────────────────────────────────┐
│                    StateGraph                           │
│                                                         │
│   ┌────────┐     ┌────────┐     ┌────────┐             │
│   │ Node_A │────▶│ Node_B │────▶│ Node_C │             │
│   └────────┘     └────────┘     └────────┘             │
│                      │                                 │
│                      ▼                                 │
│               [Conditional Edge]                       │
│                   根据状态跳转                          │
└─────────────────────────────────────────────────────────┘
```

**核心概念：**
- **StateGraph：** 有向状态图，节点是操作，边是状态转换
- **Node（节点）：** 一个具体的处理函数（Agent或工具）
- **Edge（边）：** 节点间的连接，可带条件判断
- **State（状态）：** 在图中流动的共享数据结构
- **Checkpoint（检查点）：** 状态快照，支持时间旅行和恢复

---

## 2. Agent定义方式对比

### CrewAI: Role/Goal/Backstory 范式

```python
from crewai import Agent

researcher = Agent(
    role="高级市场研究员",        # 角色名称
    goal="获取最新行业动态和竞品信息",  # 目标
    backstory="""
        你是一位资深市场研究员，在科技行业有15年经验。
        擅长通过多渠道收集信息，并能快速识别关键趋势。
        曾为多家世界500强企业提供市场洞察服务。
    """,                          # 背景故事
    tools=[search_engine, scraper],
    verbose=True
)
```

**特点：**
| 属性 | 说明 |
|------|------|
| `role` | 定义Agent的身份标签 |
| `goal` | Agent的个人目标（驱动决策） |
| `backstory` | 丰富上下文，影响LLM行为风格 |
| `allow_delegation` | 是否允许委托任务给他人 |

### LangGraph: StateGraph 范式

```python
from langgraph.graph import StateGraph
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    current_agent: str
    task_result: str

def researcher_node(state: AgentState) -> AgentState:
    """研究员节点 - 等同于一个Agent"""
    # 处理逻辑
    result = research_task(state["messages"])
    return {"task_result": result, "current_agent": "researcher"}

def analyst_node(state: AgentState) -> AgentState:
    """分析师节点"""
    result = analyze_task(state["task_result"])
    return {"task_result": result, "current_agent": "analyst"}

# 构建图
graph = StateGraph(AgentState)
graph.add_node("researcher", researcher_node)
graph.add_node("analyst", analyst_node)
graph.add_edge("researcher", "analyst")
```

**特点：**
- 状态是显式数据结构（TypedDict）
- Agent是图中的**节点函数**
- 状态在节点间流转和修改
- 边定义控制流

### 对比总结

| 维度 | CrewAI | LangGraph |
|------|--------|-----------|
| 定义方式 | 声明式角色描述 | 编程式图结构 |
| 状态管理 | 隐式（通过Crew的memory） | 显式（State对象） |
| 灵活性 | 中等（流程相对固定） | 高（完全自定义） |
| 学习曲线 | 低（贴近自然语言） | 中（需要图论概念） |
| Agent数量 | 适合5-10个 | 可扩展到数十个 |

---

## 3. 任务分派/流转机制对比

### CrewAI 流程控制

```python
# 方式1：顺序流程 (Sequential)
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.sequential  # 按定义顺序执行
)

# 方式2：层级流程 (Hierarchical)
crew = Crew(
    agents=[manager, researcher, analyst],
    process=Process.hierarchical,
    manager_agent=manager  # 管理员Agent决定任务分配
)
```

**特点：**
- `Process.sequential`：任务队列，按顺序执行
- `Process.hierarchical`：有一个管理员Agent动态分配任务
- 内置任务依赖管理
- 支持任务输出传递给下一个任务

### LangGraph 条件流转

```python
from langgraph.graph import END

graph = StateGraph(AgentState)
graph.add_node("researcher", researcher_node)
graph.add_node("analyst", analyst_node)
graph.add_node("classifier", classifier_node)

# 普通边
graph.add_edge("researcher", "classifier")

# 条件边 - 根据状态决定下一步
def should_analyze(state: AgentState) -> str:
    if state["task_result"].confidence > 0.8:
        return "analyst"
    return END

graph.add_conditional_edges(
    "classifier",
    should_analyze,
    {
        "analyst": "analyst",
        END: END
    }
)

app = graph.compile()
```

**特点：**
- `add_edge`：固定顺序连接
- `add_conditional_edges`：根据状态动态分支
- 支持循环（for 循环、while 循环）
- 支持并行分支（使用 `Send` API）
- 内置Checkpointing支持图暂停/恢复

### 流转机制对比

| 特性 | CrewAI | LangGraph |
|------|--------|-----------|
| 顺序执行 | ✅ 内置 | ✅ 手动连线 |
| 条件分支 | ⚠️ 有限 | ✅ 完整支持 |
| 并行执行 | ⚠️ 需配置 | ✅ 原生支持 |
| 循环支持 | ❌ | ✅ |
| 动态路由 | Hierarchical模式 | Conditional Edge |
| 执行追踪 | 内置verbose | LangSmith集成 |

---

## 4. 记忆管理方案

### CrewAI 记忆管理

```python
from crewai import Crew, Agent, Task
from crewai.memory import Memory, LongTermMemory, ShortTermMemory

# CrewAI 的记忆体系
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,  # 启用记忆
    memory_kwargs={
        "provider": "short-term"  # 或 "long-term"
    }
)

# LongTermMemory 使用向量数据库存储
from crewai.memory.storage import LongTermMemoryStorage

ltm_storage = LongTermMemoryStorage(
    vector_store provider="pgvector"  # 可选: chroma, pinecone, etc.
)
```

**CrewAI 记忆类型：**
| 类型 | 说明 | 持久化 |
|------|------|--------|
| ShortTermMemory | 当前对话上下文 | 内存 |
| LongTermMemory | 跨会话学习 | 向量数据库 |
| EntityMemory | 实体关系存储 | 向量数据库 |

### LangGraph 记忆管理

```python
from langgraph.checkpoint.memory import MemorySaver

# 检查点 - 图状态快照
checkpointer = MemorySaver()

app = graph.compile(checkpointer=checkpointer)

# 后续对话可以恢复状态
config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke(state, config=config)
```

**LangGraph 记忆机制：**
| 机制 | 说明 |
|------|------|
| Checkpoint | 状态快照，可恢复到任意点 |
| MemorySaver | 内存检查点存储 |
| PostgresSaver | PostgreSQL持久化（生产环境） |
| SqliteSaver | SQLite轻量级持久化 |

### 记忆管理对比

| 维度 | CrewAI | LangGraph |
|------|--------|-----------|
| 架构 | 分层记忆体系 | 检查点快照 |
| 向量搜索 | 内置集成 | 需配合LangChain |
| 状态持久化 | LTM via 向量DB | Checkpointers |
| 多轮对话 | Memory模块 | Thread ID + Checkpoint |
| 可控性 | 中等 | 高（完全自定义） |

---

## 5. 与伟力机械三AI系统的契合度分析

### 伟力机械三AI系统架构

根据背景信息，系统包含三个核心AI：
- **Jarvis** - 主控/规划Agent
- **Hermes** - 通信/协调Agent  
- **Claude** - 分析/决策Agent

```
┌─────────────────────────────────────────────────────┐
│                   三AI协作模式                       │
│                                                     │
│    ┌─────────┐                                     │
│    │ Jarvis  │◀────── 主控/规划                    │
│    │ (主控)  │                                     │
│    └────┬────┘                                     │
│         │ 分配任务                                  │
│    ┌────▼────┐    ┌─────────┐                      │
│    │ Hermes  │◀──▶│ Claude  │                     │
│    │ (通信)  │    │ (分析)  │                      │
│    └─────────┘    └─────────┘                      │
└─────────────────────────────────────────────────────┘
```

### 契合度评估

| 维度 | CrewAI | LangGraph | 权重 |
|------|--------|-----------|------|
| 现有架构匹配度 | ⭐⭐⭐⭐ (4) | ⭐⭐⭐⭐⭐ (5) | 高 |
| 层级协作支持 | ⭐⭐⭐⭐⭐ (Hierarchical) | ⭐⭐⭐⭐ (自定义) | 高 |
| 学习成本 | ⭐⭐⭐⭐ (低) | ⭐⭐⭐ (中) | 中 |
| 扩展性 | ⭐⭐⭐ (中等) | ⭐⭐⭐⭐⭐ (高) | 中 |
| 状态可控性 | ⭐⭐⭐ (隐式) | ⭐⭐⭐⭐⭐ (显式) | 高 |
| 现有Python生态 | 需适配 | LangChain全家桶 | - |

### 分析结论

**CrewAI 优势：**
- Role/Goal/Backstory与"角色定义"天然匹配
- 内置Hierarchical Process接近三AI层级结构
- 学习曲线平缓，易于团队掌握
- 快速原型开发

**LangGraph 优势：**
- 显式状态机更契合Jarvis/Hermes/Claude的精确控制需求
- 支持循环和多分支，复杂场景更强大
- Checkpoint机制便于调试和恢复
- 可与LangChain生态无缝集成

**推荐路径：**
1. **快速验证阶段**：使用CrewAI快速搭建原型
2. **生产优化阶段**：迁移到LangGraph获得更强控制力
3. **混合方案**：CrewAI负责高层编排，LangGraph负责细粒度执行

---

## 6. 具体集成建议

### 方案A: CrewAI优先集成

```python
# 映射现有三AI到CrewAI角色
from crewai import Agent, Crew, Task, Process

jarvis_agent = Agent(
    role="系统主控Agent",
    goal="协调各Agent工作，监控整体进度",
    backstory="你是伟力机械的核心控制中枢..."
)

hermes_agent = Agent(
    role="通信协调Agent", 
    goal="在各Agent间传递信息，确保通信畅通",
    backstory="你负责伟力机械系统内部通信..."
)

claude_agent = Agent(
    role="分析决策Agent",
    goal="提供深度分析和决策支持",
    backstory="你是伟力机械的智能分析引擎..."
)

# 构建层级流程
crew = Crew(
    agents=[jarvis_agent, hermes_agent, claude_agent],
    tasks=[plan_task, coordinate_task, analyze_task],
    process=Process.hierarchical,
    manager_agent=jarvis_agent
)
```

### 方案B: LangGraph精确集成

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class WeiliState(TypedDict):
    messages: list
    current_task: str
    jarvis_output: dict
    hermes_output: dict
    claude_output: dict
    task_status: str

def jarvis_node(state: WeiliState) -> WeiliState:
    """Jarvis: 任务规划与分配"""
    plan = plan_task(state["current_task"])
    return {"jarvis_output": plan, "task_status": "planned"}

def hermes_node(state: WeiliState) -> WeiliState:
    """Hermes: 协调与通信"""
    coordination = coordinate(state["jarvis_output"])
    return {"hermes_output": coordination, "task_status": "coordinated"}

def claude_node(state: WeiliState) -> WeiliState:
    """Claude: 分析与决策"""
    analysis = analyze(state["hermes_output"])
    return {"claude_output": analysis, "task_status": "completed"}

# 构建状态图
graph = StateGraph(WeiliState)
graph.add_node("jarvis", jarvis_node)
graph.add_node("hermes", hermes_node)
graph.add_node("claude", claude_node)

graph.add_edge("jarvis", "hermes")
graph.add_edge("hermes", "claude")
graph.add_edge("claude", END)

app = graph.compile()

# 执行
result = app.invoke({"current_task": "分析订单", "messages": []})
```

### 迁移路线图

```
Phase 1 (Week 1-2): CrewAI快速验证
├── 安装配置 crewai
├── 定义三Agent角色
├── 搭建Hierarchical流程
└── 原型演示

Phase 2 (Week 3-4): 评估与优化
├── 对比性能指标
├── 分析局限场景
└── 确定关键痛点

Phase 3 (Month 2): LangGraph深度集成
├── 重构为StateGraph架构
├── 实现条件分支和循环
├── 配置Checkpoint持久化
└── 集成LangChain生态
```

---

## 7. 核心代码示例汇总

### CrewAI 完整示例

```python
from crewai import Agent, Crew, Task, Process
from crewai.tools import SerpAPITool, DirectoryReadTool

# 定义工具
search_tool = SerpAPITool(api_key="your-key")

# 创建Agent
researcher = Agent(
    role="市场研究员",
    goal="获取最准确的市场分析",
    backstory="15年市场研究经验...",
    tools=[search_tool]
)

writer = Agent(
    role="报告撰写员", 
    goal="生成高质量分析报告",
    backstory="专业商业写作10年...",
    tools=[]
)

# 定义任务
research_task = Task(
    description="分析伟力机械目标市场趋势",
    agent=researcher,
    expected_output="市场分析数据摘要"
)

write_task = Task(
    description="撰写完整分析报告",
    agent=writer,
    expected_output="结构化报告文档"
)

# 组建团队
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True
)

# 启动
result = crew.kickoff()
```

### LangGraph 完整示例

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    task: str
    research: str
    analysis: str
    final_report: str

def research_node(state: AgentState) -> AgentState:
    return {"research": f"Research on: {state['task']}"}

def analysis_node(state: AgentState) -> AgentState:
    return {"analysis": f"Analysis: {state['research']}"}

def writing_node(state: AgentState) -> AgentState:
    return {"final_report": f"Report: {state['analysis']}"}

def should_continue(state: AgentState) -> str:
    if len(state.get("research", "")) > 10:
        return "continue"
    return "end"

graph = StateGraph(AgentState)
graph.add_node("research", research_node)
graph.add_node("analysis", analysis_node)
graph.add_node("writing", writing_node)

graph.set_entry_point("research")
graph.add_edge("research", "analysis")
graph.add_edge("analysis", "writing")
graph.add_edge("writing", END)

app = graph.compile()

# 执行
result = app.invoke({"task": "机械行业分析"})
```

---

## 8. 选型建议总结

| 场景 | 推荐框架 | 理由 |
|------|----------|------|
| 快速原型/MVP | **CrewAI** | Role/Goal模式直观，3分钟上手 |
| 复杂多分支流程 | **LangGraph** | 条件边+循环+并行，原生支持 |
| 需要精确状态控制 | **LangGraph** | 显式StateGraph，可调试可回溯 |
| 团队非技术背景强 | **CrewAI** | 自然语言风格，低学习曲线 |
| 生产级高并发 | **LangGraph** | Checkpoint+LangSmith监控 |
| 伟力机械三AI系统 | **LangGraph**优先 | 精确控制三Agent协作更适合 |

### 最终建议

**伟力机械三AI系统优化，推荐采用LangGraph作为核心框架：**

1. Jarvis作为主控节点（Entry Point）
2. Hermes和Claude作为执行节点
3. 使用Conditional Edge实现动态任务路由
4. 配置MemorySaver实现状态持久化
5. 预留CrewAI接口以便未来混合扩展

---

**报告生成时间：** 2026-04-24  
**框架版本：** CrewAI 1.14.2 | LangGraph 1.1.9  
**Python版本：** 3.13
