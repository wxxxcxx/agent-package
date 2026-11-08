# GLOSSARY.md 格式

## 结构

```md
# {上下文名称}

{一两句话说明这个上下文是什么、为什么存在。}

## 语言

**Order**：
{一两句话定义该术语}
_避免_：Purchase、transaction

**Invoice**：
交付后向客户发出的付款请求。
_避免_：Bill、payment request

**Customer**：
下达订单的个人或组织。
_避免_：Client、buyer、account
```

## 规则

- **要有主张。** 同一概念存在多个说法时，选定最好的那个，其余列入 `_避免_`。
- **定义要短。** 最多一两句。定义它**是什么**，不是它做什么。
- **只收本项目上下文特有的术语。** 通用编程概念（超时、错误类型、工具模式）即使项目大量使用也不应写入。收词之前先问：这是本上下文独有的概念，还是通用编程概念？只有前者该收。
- **成簇时用子标题分组。** 若全部术语同属一个内聚领域，平铺即可。

## 单上下文与多上下文

**单上下文（多数仓库）**：仓库根目录一个 `GLOSSARY.md`。

**多上下文**：根目录的 `GLOSSARY-MAP.md` 列出各上下文、所在位置及其相互关系：

```md
# 上下文地图

## 上下文

- [Ordering](./src/ordering/GLOSSARY.md) —— 接收并跟踪客户订单
- [Billing](./src/billing/GLOSSARY.md) —— 生成发票、处理付款
- [Fulfillment](./src/fulfillment/GLOSSARY.md) —— 管理仓库拣货与发货

## 关系

- **Ordering → Fulfillment**：Ordering 发出 `OrderPlaced` 事件，Fulfillment 消费该事件开始拣货
- **Fulfillment → Billing**：Fulfillment 发出 `ShipmentDispatched` 事件，Billing 消费该事件生成发票
- **Ordering ↔ Billing**：共享 `CustomerId` 与 `Money` 类型
```

技能据此推断采用哪种结构：

- 存在 `GLOSSARY-MAP.md`，读它确定各上下文
- 只有根目录的 `GLOSSARY.md`，按单上下文处理
- 两者都不存在，在第一个术语确定时按需创建根目录的 `GLOSSARY.md`

存在多个上下文时，推断当前话题属于哪一个；判断不清就问。
