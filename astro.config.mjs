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
						{ label: '程序化任务生成与具身数据', slug: 'guides/procedural-task-generation-embodied-data' },
						{ label: '浏览器遥操作与众包数据采集', slug: 'guides/browser-teleoperation-crowdsourced-data' },
						{ label: 'Human-gated DAgger 与纠错数据', slug: 'guides/human-gated-dagger-correction-data' },
						{ label: '模型条件化数据引擎', slug: 'guides/model-conditioned-data-engine' },
						{ label: 'Axis Robotics：具身数据引擎案例', slug: 'guides/axis-robotics-case-study' },
					],
				},
				{
					label: '2026 年 9 月论文知识点',
					items: [
						{ label: '示教采集与动作重定向', slug: 'guides/demonstration-collection-retargeting' },
						{ label: '人体与人-物交互重建数据', slug: 'guides/human-object-interaction-reconstruction' },
						{ label: '合成数据与仿真到真实迁移', slug: 'guides/synthetic-data-sim-to-real' },
						{ label: '多模态时空对齐数据', slug: 'guides/multimodal-spatiotemporal-alignment' },
						{ label: '三维空间表征与部件数据', slug: 'guides/3d-spatial-representation-data' },
						{ label: '主动感知与任务化测量数据', slug: 'guides/active-perception-data' },
						{ label: '潜在动作与跨本体对齐', slug: 'guides/latent-action-cross-embodiment' },
						{ label: '示教数据筛选与再利用', slug: 'guides/demonstration-data-curation' },
						{ label: '模仿学习动作数据与轨迹表示', slug: 'guides/imitation-learning-action-data' },
						{ label: '世界模型训练数据与物理表征', slug: 'guides/world-model-training-data' },
						{ label: '世界模型规划与决策评估', slug: 'guides/world-model-planning-evaluation' },
						{ label: '具身记忆与经验检索数据', slug: 'guides/embodied-memory-experience-data' },
						{ label: '语言指令与机器人动作对齐数据', slug: 'guides/language-action-grounding-data' },
						{ label: '机器人技能组合与任务过程数据', slug: 'guides/robot-skill-composition-data' },
						{ label: 'VLA 实时执行与动作分块数据', slug: 'guides/vla-realtime-execution-data' },
						{ label: '闭环纠错与失败经验数据', slug: 'guides/closed-loop-correction-data' },
						{ label: '触觉、力觉与接触数据', slug: 'guides/tactile-force-contact-data' },
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
