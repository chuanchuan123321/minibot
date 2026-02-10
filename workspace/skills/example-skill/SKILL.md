---
name: example-skill
description: "示例 skill - 展示如何创建自定义 skill"
always: false
requires_bins:
requires_env:
---

# 示例 Skill

这是一个示例 skill，展示了如何创建自定义 skill。

## 这个 Skill 的用途

这个 skill 教导如何：
1. 创建新的 skill
2. 编写 SKILL.md 文件
3. 使用 YAML frontmatter
4. 组织 skill 内容

## 基本结构

每个 skill 都包含：

### 1. YAML Frontmatter（元数据）

```yaml
---
name: skill-name              # 唯一标识符
description: "简短描述"        # 一行描述
always: false                 # 是否总是加载
requires_bins: tool1,tool2    # 需要的工具
requires_env: VAR1,VAR2       # 需要的环境变量
---
```

### 2. Markdown 内容

在 frontmatter 后面写详细的 Markdown 内容。

## 编写好的 Skill 的技巧

### ✅ 包含具体示例

不要只说理论，要给出代码示例：

```bash
# 好的例子
docker run -d -p 8080:8080 myapp:1.0

# 不好的例子
使用 docker 运行容器
```

### ✅ 列出前置条件

```
## 前置条件

- Node.js 16+
- npm 或 yarn
- Git
```

### ✅ 包含常见错误

```
## 常见错误

### 错误：端口已被占用

**原因**：另一个进程已经使用了该端口

**解决方案**：
```bash
# 查找占用端口的进程
lsof -i :8080

# 杀死进程
kill -9 <PID>
```
```

### ✅ 标记依赖

```yaml
requires_bins: docker,git
requires_env: API_KEY,DATABASE_URL
```

## Skill 的位置

### 内置 Skills
```
agent/skills/
├── github/
├── web/
├── python/
└── skill-creator/
```

### 工作区 Skills（推荐）
```
workspace/skills/
├── project-setup/
├── example-skill/  ← 这个文件
└── [你的自定义 skills]
```

## 如何让 AI 使用你的 Skill

1. **AI 看到摘要**：
   ```xml
   <skill>
     <name>example-skill</name>
     <description>示例 skill - 展示如何创建自定义 skill</description>
     <location>workspace</location>
     <status>available</status>
   </skill>
   ```

2. **AI 主动加载**：
   当 AI 需要相关指导时，会调用：
   ```json
   {"action": "execute_tool", "tool": "load_skill", "params": {"skill_name": "example-skill"}}
   ```

3. **AI 获得完整内容**：
   AI 读取这个 SKILL.md 文件的全部内容

4. **AI 根据指导完成任务**：
   AI 使用 skill 中的最佳实践和示例来完成任务

## 创建你自己的 Skill

### 步骤 1：创建目录

```bash
mkdir -p /Users/a1-6/Desktop/AI智能体/workspace/skills/my-skill
```

### 步骤 2：创建 SKILL.md

```bash
touch /Users/a1-6/Desktop/AI智能体/workspace/skills/my-skill/SKILL.md
```

### 步骤 3：编写内容

复制这个文件的结构，修改 frontmatter 和内容。

### 步骤 4：测试

启动 Minibot 并让 AI 使用你的 skill：

```bash
python chat.py
```

## 最佳实践总结

| 做 ✅ | 不做 ❌ |
|------|--------|
| 包含代码示例 | 只有理论 |
| 清晰的结构 | 混乱的内容 |
| 具体的步骤 | 模糊的说明 |
| 常见错误处理 | 没有故障排除 |
| 标记依赖 | 隐藏依赖 |
| 参考资源 | 没有参考 |

## 下一步

1. 查看其他 skills：
   - `agent/skills/web/SKILL.md` - Web 搜索 skill
   - `agent/skills/github/SKILL.md` - GitHub skill
   - `agent/skills/python/SKILL.md` - Python skill

2. 创建你自己的 skill

3. 让 AI 使用你的 skill 来完成任务

祝你创建 skill 愉快！
