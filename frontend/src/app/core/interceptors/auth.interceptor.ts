import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { switchMap, take } from 'rxjs/operators';
import * as AuthSelectors from '../store/auth/auth.selectors';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private store: Store) {}

  intercept(
    req: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<unknown>> {
    return this.store.select(AuthSelectors.selectToken).pipe(
      take(1),
      switchMap((token) => {
        // console.log('Token from store:', token);
        if (!token) return next.handle(req);
        const headers = req.headers.set('Authorization', `Bearer ${token}`);
        const cloned = req.clone({ headers });
        return next.handle(cloned);
      })
    );
  }
}
