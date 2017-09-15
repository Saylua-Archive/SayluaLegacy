import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Field, reduxForm } from 'redux-form';

let SidebarLoginForm = (props) =>  {
  const { handleSubmit } = props;

  return (
    <form id="sidebar-login-form" onSubmit={ handleSubmit }
        className="sidebar-login-form" action="/login/" method="post">
      <h3>Login to Saylua</h3>
      <table className="form-table center">
        <tr>
          <td>
            <label htmlFor="username">Username</label>
            <Field name="username" component="input" type="text" />
            <small className="form-tip"></small>
          </td>
        </tr>
        <tr>
          <td>
            <label htmlFor="password">Password</label>
            <Field name="password" component="input" type="password" />
            <small className="form-tip"></small>
          </td>
        </tr>
        <tr>
          <td>
            <button type="submit" className="small" name="login">Login!</button>
          </td>
        </tr>
        <tr>
          <td>
            <p><Link to="/login/recover/">Lost credentials?</Link></p>
            <p><Link to="/register/">Register!</Link></p>
          </td>
        </tr>
      </table>
    </form>
  );
}

SidebarLoginForm = reduxForm({
  form: 'sidebar-login'
})(SidebarLoginForm);

export default SidebarLoginForm;
