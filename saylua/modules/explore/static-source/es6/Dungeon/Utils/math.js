// math
// --------------------------------------
// Common useful math functions.

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
