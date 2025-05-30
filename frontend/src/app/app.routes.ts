import { Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';
import { CoreBanckComponent } from './pages/app/coreBanck/coreBanck.component';
import { HomeComponent } from './pages/app/home/home.component';
import { MidFlowComponent } from './pages/app/midFlow/midFlow.component';
import { SecuCheckComponent } from './pages/app/secuCheck/secuCheck.component';
import { TransactsComponent } from './pages/app/transacts/transacts.component';
import { UserComponent } from './pages/app/user/user.component';
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
        path: 'individual',
        component: TransactsComponent
      },
            {
        path: 'secuCheck',
        component: SecuCheckComponent
      },
                  {
        path: 'midFlow',
        component: MidFlowComponent
      },
                        {
        path: 'coreBank',
        component: CoreBanckComponent
      },
      {
        path: 'user',
        component: UserComponent
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
