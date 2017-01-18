// engine
// --------------------------------------
// Primarily relates to app level functions outside of the logic of the game itself.


export function log(message) {
  function padZeroes(number, width=2) {
    width -= number.toString().length;
    if (width > 0) {
      return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
    }
    return number + ""; // always return a string
  }

  // Create global log queue if necessary.
  // This logQueue is automatically consumed by our GameReducer when the state is updated.
  window.logQueue = window.logQueue || [];

  let now = new Date();
  let timestamp = `${padZeroes(now.getUTCHours())}:${padZeroes(now.getUTCMinutes())}:${padZeroes(now.getUTCSeconds())}`;
  let output = `${timestamp} - ${message}`;

  console.log(`Logging: ${output}`);
  window.logQueue.push(output);
  return output;
}
