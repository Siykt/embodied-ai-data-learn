type State = { index: number; time: number; qpos: number; qvel: number; qacc: number; stateCtrl: number[]; action: number[] | null; sensors: number[] };
type Episode = { fps: number; frameStateIndex: number[]; frameTime: number[]; states: State[]; sensors: { offset: number; dimension: number }[] };

function initExplorer(root: HTMLElement) {
  if (root.dataset.ready) return;
  root.dataset.ready = 'true';
  const data: Episode = JSON.parse(root.querySelector('[data-episode-json]')!.textContent!);
  const video = root.querySelector<HTMLVideoElement>('[data-video]')!;
  const slider = root.querySelector<HTMLInputElement>('[data-frame]')!;
  const status = root.querySelector<HTMLElement>('[data-media-status]')!;
  let selected = 0;
  let desiredSeek: number | null = null;
  const fixed = (value: number) => Math.abs(value) < 0.0000005 ? '0.000000' : value.toFixed(6);
  const put = (name: string, value: string) => { root.querySelector<HTMLElement>(`[data-${name}]`)!.textContent = value; };

  function update(frame: number) {
    selected = Math.max(0, Math.min(data.frameStateIndex.length - 1, Math.trunc(frame)));
    const k = data.frameStateIndex[selected];
    const state = data.states[k];
    const next = data.states[k + 1];
    const action = state.action!;
    slider.value = String(selected);
    slider.setAttribute('aria-valuetext', `${state.time.toFixed(2)} 秒，第 ${selected} 帧，状态 ${k}`);
    put('time', `${state.time.toFixed(2)} s`);
    put('mapping', `视频帧 ${selected} → 状态 ${k}；下一动作作用于 ${state.time.toFixed(2)}–${next.time.toFixed(2)} s。`);
    put('state-label', `state[${k}] · ${state.time.toFixed(2)} s`);
    put('action-label', `action[${k}] · 保持 0.02 s`);
    put('next-label', `state[${k + 1}] · ${next.time.toFixed(2)} s`);
    put('qpos', fixed(state.qpos));
    put('degrees', `（${(state.qpos * 180 / Math.PI).toFixed(2)}°）`);
    put('qvel', fixed(state.qvel));
    put('state-ctrl', fixed(state.stateCtrl[1]));
    put('target', fixed(action[1]));
    put('motor', fixed(action[0]));
    put('next-qpos', fixed(next.qpos));
    put('next-qvel', fixed(next.qvel));
    data.sensors.forEach((sensor, i) => {
      root.querySelector<HTMLElement>(`[data-sensor="${i}"]`)!.textContent = state.sensors.slice(sensor.offset, sensor.offset + sensor.dimension).map(fixed).join(', ');
    });
    put('raw', JSON.stringify({ frame: selected, frame_time_s: data.frameTime[selected], state, nextState: next }, null, 2));
    root.querySelectorAll<SVGLineElement>('[data-cursor]').forEach(cursor => {
      const x = String(52 + state.time / 8 * 656);
      cursor.setAttribute('x1', x);
      cursor.setAttribute('x2', x);
    });
    root.querySelectorAll<HTMLButtonElement>('[data-preset]').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.preset) === selected)));
  }

  function seekToSelection() {
    if (video.readyState < 1 || desiredSeek === null) return;
    // Seek just inside the chosen frame to avoid decoder rounding at boundaries.
    video.currentTime = data.frameTime[desiredSeek] + 0.001;
  }

  function select(frame: number) {
    video.pause();
    update(frame);
    desiredSeek = selected;
    seekToSelection();
  }

  slider.addEventListener('input', () => select(Number(slider.value)));
  root.querySelectorAll<HTMLButtonElement>('[data-preset]').forEach(button => button.addEventListener('click', () => select(Number(button.dataset.preset))));
  video.addEventListener('loadedmetadata', seekToSelection);
  video.addEventListener('seeked', () => {
    if (desiredSeek !== null) {
      if (Math.abs(video.currentTime - (data.frameTime[desiredSeek] + 0.001)) > 0.015) {
        seekToSelection();
        return;
      }
      desiredSeek = null;
    }
    update(Math.floor(video.currentTime * data.fps + 1e-6));
  });
  video.addEventListener('timeupdate', () => {
    if (desiredSeek === null) update(Math.floor(video.currentTime * data.fps + 1e-6));
  });
  video.addEventListener('error', () => {
    status.hidden = false;
    status.textContent = '录像暂时无法播放；数值和曲线仍可查看，下方可下载原始 MP4。';
  });
  if ('requestVideoFrameCallback' in video) {
    const onFrame: VideoFrameRequestCallback = (_now, metadata) => {
      if (desiredSeek === null) update(Math.round(metadata.mediaTime * data.fps));
      video.requestVideoFrameCallback(onFrame);
    };
    video.requestVideoFrameCallback(onFrame);
  }
  update(0);
}

function initAll() {
  document.querySelectorAll<HTMLElement>('[data-episode-explorer]').forEach(initExplorer);
}
initAll();
document.addEventListener('astro:page-load', initAll);
