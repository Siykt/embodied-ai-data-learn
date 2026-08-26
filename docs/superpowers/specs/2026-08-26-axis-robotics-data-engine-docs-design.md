# Axis Robotics 数据引擎技术文档设计

## 目标

将 Axis Robotics 官网与技术文档中涉及的具身智能数据技术，整理为可独立阅读、可复用的中文专题页面；另新增一篇 Axis Robotics 案例分析，明确区分公司公开主张、已发布结果与未来路线图。

## 页面范围

在 `src/content/docs/guides/` 新增五篇 Markdown 页面：

1. `procedural-task-generation-embodied-data.md`：程序化任务生成、场景/资产随机化、任务分布设计与合成数据质量。
2. `browser-teleoperation-crowdsourced-data.md`：浏览器遥操作、分布式贡献者采集、动作/观测对齐和采集质量控制。
3. `human-gated-dagger-correction-data.md`：Human-gated DAgger、模型失败纠正、on-policy 数据、回放验证和训练/评测隔离。
4. `model-conditioned-data-engine.md`：模型条件化任务选择、失败挖掘、数据重加权，以及数据—模型—部署的闭环治理。
5. `axis-robotics-case-study.md`：Axis Robotics 的定位、技术链路、相关研究、官方路线图与数据视角下的可验证性边界。

每篇页面至少放置两张紧邻解释段落的本地 SVG 图。图仅表达概念、数据字段或处理关系，不将未验证的产品指标绘制为事实。

## 内容原则

- 技术页使用通用表述；Axis Robotics 仅作为资料来源或案例，不将其官方宣传直接当作行业事实。
- 每页均从具身数据的输入、输出、时间/空间对齐、质量控制、评估和下游数据集使用展开。
- 必要术语补充到 `src/content/docs/reference/terms.md`，并从正文链接术语页或相关专题。
- 页面末尾列出官方文档、经典论文或可信技术来源，并在案例页标注“官方披露”与“规划目标”的差异。

## 站点集成

在 `astro.config.mjs` 的“数据技术整理”侧边栏中，紧接现有仿真、MuJoCo、Isaac Lab 与 VLA 页面加入五个新条目。维持现有中文标题、slug 配置和 Starlight 内容集合模式。

## 图示资产

在 `public/images/docs/` 新增十个语义化 SVG：每篇两张，覆盖任务生成维度、数据契约、采集同步、质检、DAgger 人类接管、纠错样本、失败驱动任务选择、数据飞轮、Axis 技术栈和发展时间线。

## 验证与提交

使用项目既有 `pnpm` 脚本运行格式/构建校验。完成后检查变更清单，使用与既有历史一致的单个中文 `docs:` commit，包含页面、图示、术语表和导航更新。
