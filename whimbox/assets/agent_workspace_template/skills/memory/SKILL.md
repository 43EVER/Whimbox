---
name: memory
description: 双层记忆系统，可以将重要事项立即写入长期记忆，也支持搜索历史事件。
always: true
---

# Memory

## 结构

- `memory/MEMORY.md`：长期事实（例如：用户偏好、固定的上下文、关系信息等）。该文件会被加载进上下文。
- `memory/HISTORY.md`：旧对话的追加式事件归档。该文件不会直接注入上下文。可使用`grep_history`工具搜索。每条记录以[YYYY-MM-DD HH:MM]开头。

## 检索旧事件

使用 `grep_history` 工具搜索 `memory/HISTORY.md`。

## 何时更新 MEMORY.md

当出现以下信息时，立即用 `edit_file` 或 `write_file` 写入 `MEMORY.md`：
- 用户的偏好
- 用户明确的要求
- 用户觉得重要的信息

## 自动压缩

会话变长后，旧对话会被自动总结到 `HISTORY.md`，长期事实也可能被合并进 `MEMORY.md`。你不需要管理这些。
