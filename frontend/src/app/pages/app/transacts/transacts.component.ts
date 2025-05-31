import { Component, OnInit } from '@angular/core';
import { DataService } from '../../../core/services/data.service';

@Component({
  selector: 'app-transacts',
  standalone: false,
  templateUrl: './transacts.component.html',
  styleUrls: ['./transacts.component.scss']
})
export class TransactsComponent implements OnInit {
  data: any;
  latencyKeys: string[] = [];
  flowKeys: string[] = [];
  anomalyKeys: string[] = [];

  constructor(private transactsService: DataService) {}

  ngOnInit(): void {
    this.transactsService.getMetrics().subscribe({
      next: (response) => {
        this.data = response;
        this.latencyKeys = Object.keys(response.latency_stats);
        this.flowKeys = Object.keys(response.flow_stats);
        this.anomalyKeys = Object.keys(response.anomaly_counts);
      },
      error: (err) => {
        console.error('Error al cargar métricas:', err);
      }
    });
  }
}
