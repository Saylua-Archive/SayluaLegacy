export const scriptWorker = (message) => {
  self.__func = self.__func || {};

  // On new script receival, compile and store.
  if (message.data.type === 'newScript') {
    let id = message.data.vars.ID;
    let functionBody = message.data.vars.functionString;

    eval(`self.__func[${id}] = ${functionBody};`);
  } else if (message.data.type === 'runScript') {
    let runnerID = message.data.vars.runnerID;
    let scriptID = message.data.vars.scriptID;

    // Complex chain of events to make sure we don't gaff somewhere.
    if (scriptID !== undefined && runnerID !== undefined) {
      if (self.__func[scriptID] !== undefined) {
        let args = message.data.vars.args;

        if (args !== undefined) {
          // Actual script running time

          let response = self.__func[scriptID].apply(this, args);
          if (response) {
            postMessage({
              runnerID,
              response
            });
          }
        }
      }
    }
  }
};
