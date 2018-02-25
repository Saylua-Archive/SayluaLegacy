import React from 'react';
import PropTypes from 'prop-types';

import './FormTable.scss';


let FormTable = (props) =>  {
  const { handleSubmit, children } = props;

  return (
    <form onSubmit={ handleSubmit }>
      <table className="form-table">
        <tbody>
          { children }
        </tbody>
      </table>
    </form>
  );
};

FormTable.propTypes = {
  handleSubmit: PropTypes.func
};

export default FormTable;
