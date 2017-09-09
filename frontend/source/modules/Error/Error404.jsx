import React from 'react';

import { Link } from 'react-router-dom';

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
        <Link to="/">Go back home?</Link>
      </p>
    </SayluaView>
  );
}
