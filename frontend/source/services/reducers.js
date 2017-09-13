import { combineReducers } from 'redux'
import userReducer from './user/reducer';

const sayluaApp = combineReducers({
  userReducer
});

export default sayluaApp;
