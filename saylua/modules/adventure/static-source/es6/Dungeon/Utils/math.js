// math
// --------------------------------------
// Common useful math functions.
import BezierEasing from 'bezier-easing';

export function randomRange(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}


export function distance(A, B) {
  return Math.hypot(B.x - A.x, B.y - A.y);
}


export function snap(value, multiple, maximum) {
  let half = multiple / 2;
  let snapped = (value + half - (value + half) % multiple);

  return Math.max(0, Math.min(maximum, snapped));
}


export function easeInOut(percentage) {
  if (window.__easeInOut === undefined) {
    BezierEasing(0.42, 0.0, 0.58, 1.0);
  }

  return window.__easeInOut(percentage);
}


export function easeInOutExpo(percentage) {
  if (window.__easeInOutExpo === undefined) {
    window.__easeInOutExpo = BezierEasing(1.0, 0.0, 0.0, 1.0);
  }

  return window.__easeInOutExpo(percentage);
}


export function easeInOutSine(percentage) {
  if (window.__easeInOutSine === undefined) {
    window.__easeInOutSine = BezierEasing(0.445, 0.050, 0.550, 0.950);
  }

  return window.__easeInOutSine(percentage);
}


export function easeInOutBack(percentage) {
  if (window.__easeInOutBack === undefined) {
    window.__easeInOutBack = BezierEasing(0.68, -0.55, 0.27, 1.55);
  }

  return window.__easeInOutBack(percentage);
}
