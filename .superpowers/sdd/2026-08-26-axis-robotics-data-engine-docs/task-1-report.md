# Task 1 实施报告：程序化任务生成专题与图示

## 变更文件

- `src/content/docs/guides/procedural-task-generation-embodied-data.md`
  - 新增程序化任务生成专题页面。
  - 定义任务 ID、场景与资产版本、机器人本体、随机种子、观察/动作、成功条件和数据集 split 等最小契约字段。
  - 说明场景、资产、空间布局、视觉和机器人本体如何形成可追溯任务变体。
  - 覆盖生成流程、时间与坐标对齐、质量检查、任务泄漏、资产重复、随机化失控、难例覆盖和下游评估。
  - 链接仿真器、MuJoCo、术语表、RoboGen、RoboVerse、Proc4Gem 及官方资料。
- `public/images/docs/procedural-task-generation-axes.svg`
  - 新增五类生成输入维度图，展示其汇入任务实例并导出场景配置、示范与质量元数据。
- `public/images/docs/procedural-task-data-contract.svg`
  - 新增任务规格、随机化配置、episode、验证结果和数据集 split 的绑定关系图。

未修改共享导航或 `src/content/docs/reference/terms.md`。

## 测试命令与输出

命令：

```text
pnpm build
```

结果：成功，Astro 输出 `17 page(s) built in 1.26s`，并生成：

- `/guides/procedural-task-generation-embodied-data/index.html`
- `/images/docs/procedural-task-generation-axes.svg`
- `/images/docs/procedural-task-data-contract.svg`

另运行 `git diff --check`，无空白错误；静态检查确认页面契约字段、必需链接和 SVG 中文语义文本均存在。构建保留一条既有 sitemap 警告：未配置 `site`，因此跳过 sitemap；不影响本任务页面构建。

## 自审

- 页面遵循现有 `guides/` 的中文技术文档结构与语气，未写成公司宣传内容。
- 两张 SVG 均包含 `title`、`desc`、清晰中文节点和箭头关系，并在页面对应章节附近引用。
- 内容覆盖输入、输出、时间/坐标对齐、质量控制、评估和数据集使用边界。
- 明确区分任务成功与数据质量状态，并说明仿真真值、观测和后处理标签的来源差异。
- 明确按场景、资产、布局或任务变体隔离 split，覆盖任务泄漏和只生成易成功样本的风险。
- 检查工作区时保留了已有未跟踪的 `docs/superpowers/plans/`，没有将其加入提交。

## 提交

- 提交主题：`docs: 添加程序化任务生成专题`
- 提交 SHA：`dd9d9970ea96aa56d6a533cf69f673a6ccac3d85`
