import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { environment } from '../../../environments/environment';
import { UIStateService } from '../../core/signals/ui-state.service';

@Component({
  selector: 'app-layout',
  standalone: false,
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.scss'
})
export class LayoutComponent implements OnInit {
  constructor(
    public uiStateService: UIStateService,
    private snackBar: MatSnackBar,
  ) {}

  ngOnInit() {
    // Log environment API URL to verify it's correct
    console.log('Environment API URL:', environment.apiUrl);
  }

  // openFilterDialog method removed
}
