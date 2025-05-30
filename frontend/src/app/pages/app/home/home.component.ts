import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: false,
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  options = [
    { title: 'Seccion A', subtitle: 'Información A', route: '/app/tramites' },
    { title: 'Seccion B', subtitle: 'Información B', route: '/app/tramites' },
    { title: 'Seccion B', subtitle: 'Información B', route: '/app/tramites' }
  ];

  constructor(private router: Router) {}

  navigate(route: string) {
    this.router.navigate([route]);
  }
}
