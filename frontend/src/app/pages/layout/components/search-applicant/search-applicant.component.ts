import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-search-applicant',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule,
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './search-applicant.component.html',
  styleUrl: './search-applicant.component.scss'
})
export class SearchApplicantComponent  {
  filterForm!: FormGroup;
   fields = [
    { name: 'tipo_persona', label: 'Tipo de persona', type: 'select', options: ['Persona natural', 'Persona jurídica'] },
    { name: 'tipo_documento', label: 'Tipo de documento', type: 'select', options: ['DNI', 'Pasaporte', 'Cédula'] },
    { name: 'numero_identificacion', label: 'Número de identificación', type: 'text' },
    { name: 'primer_nombre', label: 'Primer nombre', type: 'text' },
    { name: 'segundo_nombre', label: 'Segundo nombre', type: 'text' },
    { name: 'primer_apellido', label: 'Primer apellido', type: 'text' },
    { name: 'segundo_apellido', label: 'Segundo apellido', type: 'text' },
    { name: 'sexo', label: 'Sexo', type: 'select', options: ['Masculino', 'Femenino', 'Otro'] },
    { name: 'grupo_etnico', label: 'Grupo étnico', type: 'select', options: ['Indígena', 'Afrodescendiente', 'Mestizo'] },
  ];

  razonSocialField = { name: 'razon_social', label: 'Razón social', type: 'text' };
  fieldsToShow = [...this.fields];
  constructor(private fb: FormBuilder,
    private dialogRef: MatDialogRef<SearchApplicantComponent>
  ) {}

  ngOnInit() {
    this.filterForm = this.fb.group({
      tipo_persona: [''],
      tipo_documento: [''],
      numero_identificacion: [''],
      primer_nombre: [''],
      segundo_nombre: [''],
      primer_apellido: [''],
      segundo_apellido: [''],
      sexo: [''],
      grupo_etnico: [''],
      razon_social: [''],
    });

    // Escucha cambios en el tipo de persona
    this.filterForm.get('tipo_persona')?.valueChanges.subscribe(value => {
      if (value === 'Persona jurídica') {
        this.showOnlyRazonSocial();
      } else {
        this.showAllFields();
      }
    });
  }

  showOnlyRazonSocial() {
    this.fieldsToShow = this.fields.filter(field => field.name === 'tipo_persona');
    this.fieldsToShow.push(this.razonSocialField);
  }

  showAllFields() {
    this.fieldsToShow = [...this.fields]; // Restaura todos los campos
  }

  closeFilterDialog() {
    this.dialogRef.close();
  }
}
