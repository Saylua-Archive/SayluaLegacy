import { combineReducers, createStore } from 'redux';
import { reducer as reduxFormReducer } from 'redux-form';

import userReducer from './user/reducer';

const sayluaReducer = combineReducers({
  form: reduxFormReducer,
  userReducer
});

const sayluaStore = (window.devToolsExtension
  ? window.devToolsExtension()(createStore)
  : createStore)(sayluaReducer);

export default sayluaStore;
