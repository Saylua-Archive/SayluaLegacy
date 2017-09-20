import React from 'react';
import PropTypes from 'prop-types';

import { Link } from 'react-router-dom';
import { Field, reduxForm } from 'redux-form';

import FormTable from 'shared/Forms/FormTable';
import InputRow from 'shared/Forms/FormTable/InputRow';
import FormRow from 'shared/Forms/FormTable/FormRow';

import { Required, NotBlank } from 'shared/Forms/Validators';


let LoginForm = (props) =>  {
  const { handleSubmit, submitting, compact, identifier } = props;

  let idSuffix = '-login';
  if (identifier) {
    idSuffix += identifier;
  }

  return (
    <FormTable handleSubmit={ handleSubmit }>
      <Field name="username" fieldId={ "username" + idSuffix }
        component={ InputRow } label="Username/Email" type="text"
        validate={[Required('Username/Email'), NotBlank('Username/Email')]} />
      <Field name="password" fieldId={ "password" + idSuffix }
        component={ InputRow } label="Password" type="password"
        validate={[Required('Password')]} />
      <FormRow>
        <button className={ compact ? 'small' : ''} disabled={submitting}
            type="submit" name="login">Login!</button>
      </FormRow>
      <FormRow>
        <p>
          <Link to="/login/recover/">
            { compact ? 'Lost credentials?' : 'Lost username or password?'}
          </Link>
        </p>
        <p>
          <Link to="/register/">
            { compact ? 'Register!' : 'Register a new account!'}
          </Link>
        </p>
      </FormRow>
    </FormTable>
  );
};

LoginForm.propTypes = {
  handleSubmit: PropTypes.func,
  compact: PropTypes.bool,
  identifier: PropTypes.string
};

LoginForm = reduxForm({
  form: 'login'
})(LoginForm);

export default LoginForm;
