# 好测试与坏测试

## 好测试

**集成式**：穿过真实接口，而不是 mock 内部部件。

```typescript
// 好：验证可观察的行为
test("用户能用有效购物车结账", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

特征：

- 验证用户或调用方真正关心的行为
- 只用公开接口
- 内部重构后依然成立
- 描述**做什么**，而非**怎么做**
- 每个测试一个逻辑断言

## 坏测试

**测实现细节**：与内部结构耦合。

```typescript
// 坏：测的是实现细节
test("checkout 调用 paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

危险信号：

- mock 内部协作者
- 测试私有方法
- 断言调用次数或顺序
- 行为没变，重构后测试就挂
- 测试名描述**怎么做**，而非**做什么**
- 绕过接口，从外部手段验证

```typescript
// 坏：绕过接口去验证
test("createUser 写入数据库", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// 好：通过接口验证
test("createUser 之后能取回该用户", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

**同义反复的测试**：期望值复述了实现，测试按构造必然通过。

```typescript
// 坏：期望值按代码的算法重算了一遍
test("calculateTotal 汇总行项目", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// 好：期望值是一个独立的、已知的字面量
test("calculateTotal 汇总行项目", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```
