// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: '具身智能数据',
			customCss: ['./src/styles/custom.css'],
			sidebar: [
				{
					label: '数据技术整理',
					items: [
						{ label: '相机内参数据要求', slug: 'guides/camera-intrinsics-data-requirements' },
						{ label: '视觉惯性 SLAM 数据', slug: 'guides/visual-inertial-slam' },
						{ label: '移动设备 IMU 数据采集', slug: 'guides/mobile-imu-data-collection' },
						{ label: 'YUV 算法与 Android 使用', slug: 'guides/yuv-algorithms-android' },
						{ label: 'Ego 数据与 UMI 视频采集', slug: 'guides/ego-world-operation-umi-video' },
						{ label: 'Episode 与 Trajectory 数据设计', slug: 'guides/episode-trajectory-design' },
						{ label: 'Aria、Ego4D 与 Ego-Exo4D 数据格式', slug: 'guides/aria-ego4d-egoexo4d-formats' },
						{ label: 'Meta VRS 多传感器数据规范', slug: 'guides/meta-vrs-data-standard' },
						{ label: 'TURN 与具身数据实时采集', slug: 'guides/turn-for-embodied-data' },
						{ label: '仿真器与具身数据', slug: 'guides/simulators-embodied-data' },
						{ label: 'MuJoCo 与具身数据', slug: 'guides/mujoco-embodied-data' },
						{ label: 'Isaac Lab 与具身数据', slug: 'guides/isaac-lab-embodied-data' },
						{ label: 'VLA 模型与主流验证方法', slug: 'guides/vla-models-and-evaluation' },
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