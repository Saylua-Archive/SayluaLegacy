import React from 'react';
import { Link } from 'react-router-dom';
import { Field, reduxForm } from 'redux-form';

let RegisterForm = (props) =>  {
  const { handleSubmit } = props;

  return (
    <form onSubmit={ handleSubmit }>
      <table className="form-table">
        <tbody>
          <tr>
            <td className="label">
              <label htmlFor="username">Username</label>
            </td>
            <td>
              <Field name="username" component="input" placeholder="Username" type="text" />
              <small className="form-tip">
                Valid characters: letters, numbers, and +~._-
              </small>
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
            <td className="label">
              <label htmlFor="confirm_password">Confirm Password</label>
            </td>
            <td>
              <Field name="confirm_password" component="input" placeholder="Confirm Password" type="password" />
              <small className="form-tip"></small>
            </td>
          </tr>
          <tr>
            <td className="label">
              <label htmlFor="email">Email Address</label>
            </td>
            <td>
              <Field name="email" component="input" placeholder="Email Address" type="text" />
              <small className="form-tip"></small>
            </td>
          </tr>
          <tr>
            <td className="label">
              <label htmlFor="invite_code">Invite Code</label>
            </td>
            <td>
              <Field name="invite_code" component="input" placeholder="Invite Code" type="text" />
              <small className="form-tip"></small>
            </td>
          </tr>
          <tr>
            <td></td>
            <td>
              <Field name="over13" component="input" type="checkbox" />
              <label htmlFor="over13">
                I certify that I am at least 13 years old.
              </label>
              <small className="form-tip"></small>
            </td>
          </tr>
          <tr>
            <td></td>
            <td>
              <Field name="tos" component="input" type="checkbox" />
              <label htmlFor="tos">
                I agree to the <Link to="/page/terms/">Terms of Service</Link>.
              </label>
              <small className="form-tip"></small>
            </td>
          </tr>
          <tr>
            <td></td>
            <td>
              <button type="submit" name="register">Register!</button>
            </td>
          </tr>
          <tr>
            <td></td>
            <td>
              <p><Link to="/login/">
                Login to an existing account.
              </Link></p>
              <p><Link to="/login/recover/">
                Lost username or password?
              </Link></p>
            </td>
          </tr>
        </tbody>
      </table>
    </form>
  );
}

RegisterForm = reduxForm({
  form: 'register'
})(RegisterForm);

export default RegisterForm;
