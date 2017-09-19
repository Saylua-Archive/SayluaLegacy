import React from 'react';
import PropTypes from 'prop-types';

import { Field } from 'redux-form';


let InputRow = (props) =>  {
  const { input, label, type, placeholder, fieldId, tip, meta: { touched, error } } = props;
  let id = fieldId || ('form-' + name);
  return (
    <tr>
      <td className="label">
        <label htmlFor={ id }>{ label }</label>
      </td>
      <td>
        <input {...input} id={ id } placeholder={ placeholder || label } type={type} />
        <small className={ "form-tip" + (error ? " error" : "") }>
          { error || tip }
        </small>
      </td>
    </tr>
  );
};

export default InputRow;
