# agent-package

本仓库是 [mattpocock/skills](https://github.com/mattpocock/skills) 的修改版，所有技能以 `woz-` 前缀重命名。使用 [APM](https://github.com/anomalyco/agent-package-manager) 管理打包和编译。

## 包结构

| 包                | 路径                  | 依赖                  |
| ----------------- | --------------------- | --------------------- |
| `woz` (根)        | `./apm.yml`           | general + engineering |
| `woz-general`     | `general/apm.yml`     | 无                    |
| `woz-engineering` | `engineering/apm.yml` | `../general`          |

- 根 `apm.yml` 为顶层编排，不直接包含技能
- `engineering` 依赖 `general`，所以 `.agents/skills/` 中通用和工程技能并存

## 技能组织

- `general/.apm/skills/woz-*/` — 通用技能
- `engineering/.apm/skills/woz-*/` — 工程技能
- `general/.apm/prompts/woz-*.prompt.md` — 通用 prompt（`disable-model-invocation: true` 的技能）
- `engineering/.apm/prompts/woz-*.prompt.md` — 工程 prompt （`disable-model-invocation: true` 的技能）

## 同步流程（关键步骤）

1. 将 `https://github.com/mattpocock/skills` clone 到临时目录
2. 只同步 MAPPING.md 中列出的技能
3. 重写内部引用：映射表中的特殊映射（如 `ask-matt` → `woz-help`），其余加 `woz-` 前缀
4. 写入全部文件，创建 prompt 文件
5. **必须检查 SKILL.md 的 `name:` frontmatter 是否与目录名一致**（上游的 `name:` 保留了原名，需要改为 `woz-` 前缀，如 `name: code-review` → `name: woz-code-review`）
6. 验证所有引用的 `/woz-*` 技能是否存在，缺失的输出警告

## 注意事项

- `engineering/MAPPING.md` 和 `general/MAPPING.md` 是真相来源，同步只处理映射表中的技能

