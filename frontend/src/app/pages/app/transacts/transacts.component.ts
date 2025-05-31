import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-transacts',
  templateUrl: './transacts.component.html',
  styleUrls: ['./transacts.component.scss'],
  standalone: false
})
export class TransactsComponent implements OnInit {
  data = {
    timestamp: '2025-05-30T17:28:17.742250',
    latency_stats: {
      mean: 0.17652691867124856,
      median: 0.173,
      std: 0.07367858552470405,
      min: 0.05,
      max: 0.3,
      p95: 0.289,
      p99: 0.29728
    },
    flow_stats: {
      complete_flow_pct: 87.3,
      avg_stages: 3.619,
      avg_duration: 8.73,
      min_duration: 0,
      max_duration: 10
    },
    anomaly_counts: {
      pattern: 127,
      sequence: 0,
      bottlenecks: 43
    }
  };

  latencyKeys: string[] = [];
  flowKeys: string[] = [];
  anomalyKeys: string[] = [];

  constructor() {}

  ngOnInit(): void {
    this.latencyKeys = Object.keys(this.data.latency_stats);
    this.flowKeys = Object.keys(this.data.flow_stats);
    this.anomalyKeys = Object.keys(this.data.anomaly_counts);
  }
}
