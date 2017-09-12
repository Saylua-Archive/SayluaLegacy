import React, { Component } from 'react';

import SayluaView from 'shared/SayluaView';


export default class Login extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <SayluaView title="Login">
        <h1>Login</h1>
      </SayluaView>
    );
  }
}
