import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UIStateService } from '../../../../core/signals/ui-state.service';

@Component({
  selector: 'app-sidebar',
  standalone: false,
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {
  constructor(
    private route: Router,
    public uiStateService: UIStateService
  ) {}

  toggleSubMenu(index: number) {
    this.uiStateService.toggleSidebarSubMenu(index);
  }

  navigateToUrl(url: string) {
    this.route.navigate(['app' + url]);
  }
}
