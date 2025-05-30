import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatError, MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { ModalService } from '../../core/services/ui/modal.service';
import * as AuthActions from '../../core/store/auth/auth.actions';
import * as AuthSelectors from '../../core/store/auth/auth.selectors';

@Component({
  selector: 'app-login',
  imports: [
    CommonModule,
    MatInputModule,
    MatFormFieldModule,
    FormsModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatError
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  standalone: true
})
export class LoginComponent {
  loading$: Observable<boolean>;

  logInForm = new FormGroup({
    email: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required])
  });

  constructor(private store: Store, private modalService: ModalService) {
    this.loading$ = this.store.select(AuthSelectors.selectAuthLoading);
  }

  forgetPassword() {
    this.modalService.openErrorModal(
              'Lo sentimos',
              'No podemos hacer nada :c'
            );
  }

  submit() {
    if (this.logInForm.valid) {
      const credentials = {
        username: this.logInForm.value.email || '',
        password: this.logInForm.value.password || ''
      };

      this.store.dispatch(AuthActions.login({ credentials }));
    }
  }
}
