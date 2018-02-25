import React from 'react';

let FormRow = (props) =>  {
  const { children } = props;
  return (
    <tr>
      <td></td>
      <td>
        { children }
      </td>
    </tr>
  );
};

export default FormRow;
