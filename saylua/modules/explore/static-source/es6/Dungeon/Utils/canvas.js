export function calculateSize () {
  let ratio = 16 / 9;
  let width, height, baseWidth;

  baseWidth = document.body.offsetWidth;

  if (baseWidth < 1000) {
    width = Math.floor(Math.min(650, baseWidth));
  } else {
    width = Math.floor(Math.min(baseWidth * 0.65, 1400));
  }

  height = Math.floor(width / ratio);

  return [width, height];
}
