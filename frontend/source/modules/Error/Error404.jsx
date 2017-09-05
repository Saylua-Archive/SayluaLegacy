import React from 'react';

import SayluaView from 'shared/SayluaView';

export default function() {
  return (
    <SayluaView title="404 Page Not Found">
      <h1>404 Page Not Found</h1>
      <img src="/static/img/pets/loxi/common.png" className="pet" alt="Random pet" title="Random pet" />
      <p>
        The page you are looking for has not been found!
      </p>
      <p>
        <a href="/">Go back home?</a>
      </p>
    </SayluaView>
  );
}
