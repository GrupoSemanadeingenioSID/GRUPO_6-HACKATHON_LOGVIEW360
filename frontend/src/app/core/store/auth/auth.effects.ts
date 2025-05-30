import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of } from 'rxjs';
import { catchError, map, switchMap, tap } from 'rxjs/operators';
import { ModalService } from '../../services/ui/modal.service';
import { AuthService } from '../../services/users/auth.service';
import * as AuthActions from './auth.actions';

@Injectable()
export class AuthEffects {
  constructor(
    private actions$: Actions,
    private authService: AuthService,
    private router: Router,
    private modalService: ModalService
  ) {}

  login$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.login),
      switchMap(({ credentials }) =>
        this.authService.login(credentials).pipe(
          map((response) => AuthActions.loginSuccess({ response })),
          catchError((error) => {
            this.modalService.openErrorModal(
              'Error de autenticación',
              'No se pudo iniciar sesión. Por favor, verifique sus credenciales.'
            );
            return of(AuthActions.loginFailure({ error }));
          })
        )
      )
    )
  );

  loginSuccess$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.loginSuccess),
      tap(() => {
        this.router.navigate(['/app']);
        this.modalService.openSuccessModal(
          'Inicio de sesión exitoso',
          '¡Bienvenido al sistema!'
        );
      })
    ),
    { dispatch: false }
  );

  logout$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.logout),
      tap(() => {
        this.router.navigate(['/login']);
        this.modalService.openInfoModal(
          'Sesión cerrada',
          'Has cerrado sesión correctamente.'
        );
      })
    ),
    { dispatch: false }
  );
}
