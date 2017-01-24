// math
// --------------------------------------
// Common useful math functions.

export function randomRange(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

export function distance(A, B) {
  return Math.hypot(B.x - A.x, B.y - A.y);
}
