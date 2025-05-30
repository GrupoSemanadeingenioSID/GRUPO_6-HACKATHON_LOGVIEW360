import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { LoginRequest, LoginResponse } from '../../models/users/auth.model';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly apiUrl = `${environment.apiUrl}/api/v1/auth`;

  constructor(private http: HttpClient) {}

  login(credentials: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, credentials);
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
