import { createReducer, on } from '@ngrx/store';
import * as AuthActions from './auth.actions';

export interface AuthState {
  username: string | null;
  token: string | null;
  loading: boolean;
  error: any | null;
}

export const initialState: AuthState = {
  username: null,
  token: null,
  loading: false,
  error: null
};

export const authReducer = createReducer(
  initialState,
  on(AuthActions.login, (state) => ({
    ...state,
    loading: true,
    error: null
  })),
  on(AuthActions.loginSuccess, (state, { response }) => ({
    ...state,
    username: typeof response.username === 'string' ? response.username : String(response.username),
    token: typeof response.token === 'string' ? response.token : String(response.token),
    loading: false,
    error: null
  })),
  on(AuthActions.loginFailure, (state, { error }) => ({
    ...state,
    loading: false,
    error
  })),
  on(AuthActions.logout, AuthActions.logoutSuccess, () => initialState)
);
