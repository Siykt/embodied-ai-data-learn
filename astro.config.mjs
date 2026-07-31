// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: '具身智能数据学习',
			sidebar: [
				{
					label: '数据技术整理',
					items: [
						{ label: '视觉惯性 SLAM 数据', slug: 'guides/visual-inertial-slam' },
						{ label: 'Ego 数据与 UMI 视频采集', slug: 'guides/ego-world-operation-umi-video' },
					],
				},
				{
					label: '参考',
					items: [{ label: '具身智能数据术语表', slug: 'reference/terms' }],
				},
			],
		}),
	],
});
