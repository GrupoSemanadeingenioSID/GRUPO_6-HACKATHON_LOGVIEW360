import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { LoginRequest, LoginResponse } from '../../models/users/auth.model';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly apiUrl = `${environment.apiUrl}/api/v1/auth`;

  constructor(private http: HttpClient) {}

login(credentials: LoginRequest): Observable<LoginResponse> {
  const fakeResponse: LoginResponse = {
    token: 'fake-jwt-token-12345',
    username: 'glud'
  }
  return of(fakeResponse);
}
  refreshToken(refreshToken: string): Observable<any> {
    const body = { refresh_token: refreshToken };
    return this.http.post<any>(`${this.apiUrl}/refresh`, body);
  }

  logout(refreshToken: string): Observable<any> {
    const body = { refresh_token: refreshToken };
    return this.http.post<any>(`${this.apiUrl}/logout`, body);
  }
}
