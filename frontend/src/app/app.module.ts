import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
// app.module.ts
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule, MatIconButton } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIcon, MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSelectModule } from '@angular/material/select';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatTreeModule } from '@angular/material/tree';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { routes } from './app.routes';
import { HomeComponent } from './pages/app/home/home.component';


import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatChipsModule } from '@angular/material/chips';
import { MatMenuModule } from '@angular/material/menu';
import {
  MatColumnDef,
  MatTable,
  MatTableModule,
} from '@angular/material/table';
import { TransactsComponent } from './pages/app/transacts/transacts.component';
import { SidebarComponent } from './pages/layout/components/sidebar/sidebar.component';
import { TopbarComponent } from './pages/layout/components/topbar/topbar.component';
import { LayoutComponent } from './pages/layout/layout.component';

import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';

import { environment } from '../environments/environment';
import { AppComponent } from './app.component';

// NgRx
import { AuthEffects } from './core/store/auth/auth.effects';
import { authReducer } from './core/store/auth/auth.reducer';

// Material
import { MatDialogModule } from '@angular/material/dialog';
import { MatSortModule } from '@angular/material/sort';
import { AuthInterceptor } from './core/interceptors/auth.interceptor';
import { GenericTableComponent } from './pages/layout/components/generic-table/generic-table.component';

@NgModule({
  declarations: [
    AppComponent,
    SidebarComponent,
    TopbarComponent,
    LayoutComponent,
    HomeComponent,
    TransactsComponent,
    GenericTableComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    MatDialogModule,
    MatDividerModule,
    MatButtonModule,
    MatListModule,
    MatIconModule,
    RouterModule,
    MatIconButton,
    MatIcon,
    MatFormFieldModule,
    MatInputModule,
    MatAutocompleteModule,
    MatSelectModule,
    MatSidenavModule,
    MatDividerModule,
    MatTreeModule,
    ReactiveFormsModule,
    MatPaginatorModule,
    MatTable,
    MatColumnDef,
    MatTableModule,
    MatCheckboxModule,
    MatMenuModule,
    MatChipsModule,
    MatCardModule,
    MatSortModule,
    RouterModule.forRoot(routes),
    StoreModule.forRoot({ "auth": authReducer }),
    EffectsModule.forRoot([AuthEffects]),
    StoreDevtoolsModule.instrument({
      maxAge: 25,
      logOnly: environment.production }),
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
