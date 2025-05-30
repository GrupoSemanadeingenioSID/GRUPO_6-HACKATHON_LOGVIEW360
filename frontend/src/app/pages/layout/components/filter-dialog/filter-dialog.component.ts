import { CommonModule } from '@angular/common';
import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatNativeDateModule } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-filter-dialog',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule,
    CommonModule,
    ReactiveFormsModule,
    MatButtonModule,
  ],
  templateUrl: './filter-dialog.component.html',
  styleUrl: './filter-dialog.component.scss',
})
export class FilterDialogComponent implements OnInit {
  @Output() close = new EventEmitter<any>();
  @Output() filter = new EventEmitter<any>();

  filterForm!: FormGroup;

  private filterSubscription!: Subscription;

  constructor(
    private fb: FormBuilder,
  ) {}

  ngOnInit() {
  }

  closeFilterDialog() {
    this.close.emit();
  }

  searchFilter() {
  }
}
