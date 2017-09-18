import React, { Component } from 'react';

import SayluaView from 'shared/SayluaView';

import LoginForm from './forms/LoginForm';


export default class Login extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <SayluaView title="Login">
        <h1>Login to Saylua</h1>
        <LoginForm />
      </SayluaView>
    );
  }
}
