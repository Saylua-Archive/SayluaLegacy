import React from 'react';
import { Link } from 'react-router-dom';
import { Field, reduxForm } from 'redux-form';

let LoginForm = (props) =>  {
  const { handleSubmit, compact } = props;

  return (
    <form onSubmit={ handleSubmit }>
      <table className="form-table">
        <tbody>
          <tr>
            <td className="label">
              <label htmlFor="username">Username/Email</label>
            </td>
            <td>
              <Field name="username" component="input" placeholder="Username/Email" type="text" />
              <small className="form-tip"></small>
            </td>
          </tr>
          <tr>
            <td className="label">
              <label htmlFor="password">Password</label>
            </td>
            <td>
              <Field name="password" component="input" placeholder="Password" type="password" />
              <small className="form-tip"></small>
            </td>
          </tr>
          <tr>
            <td></td>
            <td>
              <button className={ compact ? 'small' : ''}
                  type="submit" name="login">Login!</button>
            </td>
          </tr>
          <tr>
            <td></td>
            <td>
              <p><Link to="/login/recover/">
                { compact ? 'Lost credentials?' : 'Lost username or password?'}
              </Link></p>
              <p><Link to="/register/">
                { compact ? 'Register!' : 'Register a new account!'}
              </Link></p>
            </td>
          </tr>
        </tbody>
      </table>
    </form>
  );
}

LoginForm = reduxForm({
  form: 'login'
})(LoginForm);

export default LoginForm;
