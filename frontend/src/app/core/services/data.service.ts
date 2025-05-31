import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

// Define una interfaz opcional para tipar la respuesta
export interface MetricsResponse {
  timestamp: string;
  latency_stats: { [key: string]: number };
  flow_stats: { [key: string]: number };
  anomaly_counts: { [key: string]: number };
}

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private readonly API_URL = 'http://127.0.0.1:8000/api/v1/metrics/latency';

  constructor(private http: HttpClient) {}

  /**
   * Obtiene las métricas de latencia desde el backend
   */
  getMetrics(): Observable<MetricsResponse> {
    return this.http.get<MetricsResponse>(this.API_URL);
  }
}
