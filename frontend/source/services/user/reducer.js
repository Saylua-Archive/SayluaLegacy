import { createStore, combineReducers } from 'redux';

const userReducer = (state=1, {type}) => {
  return state + 1;
}

export default userReducer;
