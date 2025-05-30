import { Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';
import { HomeComponent } from './pages/app/home/home.component';
import { TransactsComponent } from './pages/app/transacts/transacts.component';
import { LayoutComponent } from './pages/layout/layout.component';
import { LoginComponent } from './pages/login/login.component';

export const routes: Routes = [
  {
    path: '',
    component: LoginComponent
  },
  {
    path: 'app',
    component: LayoutComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path: '',
        redirectTo: 'inicio',
        pathMatch: 'full'
      },
      {
        path: 'inicio',
        component: HomeComponent
      },
      {
        path: 'tramites',
        component: TransactsComponent
      },
      {
        path: '**',
        redirectTo: 'inicio'
      }
    ]
  },
  {
    path:'**',
    redirectTo: ''
  }
];
