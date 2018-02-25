import React, { Component } from 'react';

import SayluaView from 'shared/SayluaView';

import RegisterForm from './Forms/RegisterForm';


export default class Register extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <SayluaView title="Register">
        <h1>Register a New Account on Saylua</h1>
        <RegisterForm />
      </SayluaView>
    );
  }
}
