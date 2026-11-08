# 何时使用 mock

只在**系统边界**上 mock：

- 外部 API（支付、邮件等）
- 数据库（视情况，优先用测试库）
- 时间与随机数
- 文件系统（视情况）

不要 mock：

- 自己的类与模块
- 内部协作者
- 任何由你掌控的东西

## 为可 mock 而设计

系统边界上的接口，应按易于 mock 的方式设计：

**1. 使用依赖注入**

把外部依赖传进来，不要在内部自行创建：

```typescript
// 易于 mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// 难以 mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. 用 SDK 式接口，而非通用 fetcher**

每个外部操作对应一个专用函数，而不是一个带条件分支的通用函数：

```typescript
// 好：每个函数都能独立 mock
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// 坏：mock 时必须在 mock 内部写条件逻辑
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

SDK 式的好处：

- 每个 mock 只返回一种确定的形状
- 测试准备阶段无需条件逻辑
- 一眼看出该测试触及了哪些端点
- 每个端点各有类型安全
