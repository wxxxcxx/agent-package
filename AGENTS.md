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

1. 将 `https://github.com/mattpocock/skills` clone 到 `.sync-tmp/`（每次覆盖，保证从干净上游开始）
2. 清理 MAPPING.md 中列出的**所有**技能文件夹（整棵移除）
3. 将 MAPPING.md 中列出的技能复制到对应的位置，并参考 MAPPING.md 映射修改技能名称
4. 重写 markdown 正文中的技能引用：映射表中的特殊映射（如 `ask-matt` → `woz-help`），其余加 `woz-` 前缀（此步不处理 YAML frontmatter）
5. **必须检查 SKILL.md 的 `name:` frontmatter 是否与目录名一致**（上游的 `name:` 保留了原名，需要改为 `woz-` 前缀，如 `name: code-review` → `name: woz-code-review`）
6. 验证所有引用的 `/woz-*` 技能是否在 `.agents/skills/` 下真实存在，缺失的输出警告（不中止同步）
7. 进行 git diff，输出变化报告（包含：变更技能清单 + 缺失引用警告，不输出 `name:` 修复清单）
8. 更新 `apm.yml` 的 `version` 字段 （更新修订号）

## 注意事项

- `engineering/MAPPING.md` 和 `general/MAPPING.md` 是真相来源，同步只处理映射表中的技能
