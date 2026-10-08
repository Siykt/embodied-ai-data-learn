# 具身智能数据与仿真文档

本仓库使用 Astro Starlight 构建文档站点，按并列专题组织内容：

- **数据技术整理**：真实设备上的数据采集、处理、对齐、标注与评估。
- **仿真器**：从仿真技术发展路径到场景、物理、传感器、任务、数据生成和真实迁移。入口位于 `/simulation/`。
- **论文知识点与参考资料**：专题延伸、术语和来源索引。

页面位于 `src/content/docs/`。仿真器专题的页面集中在 `src/content/docs/simulation/`，站点目录在 `astro.config.mjs` 中维护；图片放在 `public/images/docs/`。

## 本地使用

```sh
npm install
npm run build
npx astro dev --background
```

开发服务器使用 `npx astro dev status` 查看状态、`npx astro dev logs` 查看日志、`npx astro dev stop` 停止。Astro 相关用法见[官方文档](https://docs.astro.build)。
