# Task 4 实施报告：模型条件化数据引擎专题

## 交付范围

本任务新增模型条件化数据引擎专题文档，并创建 brief 指定的两张 SVG 图示。内容围绕具身 AI 数据的采集、处理、对齐、质量控制、评估隔离、数据血缘和部署反馈展开；未修改共享导航、`terms.md`，未加入 Axis-specific case content。

## 文件变更

- `src/content/docs/guides/model-conditioned-data-engine.md`
  - 新增页面 frontmatter，生成 `/guides/model-conditioned-data-engine/`。
  - 说明策略评估日志、失败聚类、任务参数搜索、候选任务队列和仿真/人类采集的关系。
  - 使用成功率以外的失败价值、不确定性、分布漂移、物理违规、覆盖缺口和采集成本构建可解释的采样优先级。
  - 定义程序化任务、评估、质量和部署反馈四类标准化输入，以及任务实例和 episode 的版本、来源、授权、split、时间和空间对齐字段。
  - 描述任务生成、采集、验证、训练与评估、部署、反馈六阶段飞轮。
  - 覆盖版本化、数据血缘、分布监控、重加权、训练/评测隔离、重放验证和停止规则。
  - 引用 DAgGER、VLA 评估、程序化任务生成、仿真器、Open X-Embodiment 和 SIMPLER 资料。
- `public/images/docs/model-conditioned-task-selection.svg`
  - 展示策略评估日志 → 失败聚类 → 任务参数搜索 → 候选任务队列 → 仿真/人类采集 → 验证与入库。
- `public/images/docs/embodied-data-engine-flywheel.svg`
  - 展示任务生成、数据采集、验证、训练与评估、部署、反馈六阶段及版本/血缘要求。

页面仅使用上述两张指定 SVG，并在图示附近提供中文 alt 文本。

## 自审结果

- 文档风格与现有 VLA、仿真、程序化任务生成和 Human-gated DAgger 专题保持一致。
- 明确区分任务成功状态与数据质量状态，保留失败数据的分析和恢复训练价值。
- 明确区分原始观测、派生标签、策略动作、人类动作和安全控制器动作的来源。
- 明确记录观测、动作计划、动作生效的时间语义，以及世界、基座、末端、相机和物体坐标系。
- 明确要求评估集冻结、任务/场景/资产/机器人/操作者/时间隔离和新增数据的触发血缘。
- 检查页面无 `TODO`、`TBD` 或 Axis-specific 内容；未改 `astro.config.mjs` 与 `src/content/docs/reference/terms.md`。
- 两个 SVG 均通过 XML 语法检查。

## 验证

运行：

```bash
pnpm build
git diff --check
```

结果：

- `pnpm build` 成功，Astro 生成 `/guides/model-conditioned-data-engine/index.html`。
- Astro 共构建 20 个页面，Pagefind 搜索索引成功生成。
- `git diff --check` 通过，无空白错误。
- 构建输出提示 sitemap 因项目未设置 `site` 而跳过；这是既有配置提示，不影响本任务页面构建。

## 提交

提交 subject：`docs: 新增模型条件化数据引擎专题`
