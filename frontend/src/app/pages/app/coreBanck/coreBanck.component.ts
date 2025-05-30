import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-coreBanck',
  templateUrl: './coreBanck.component.html',
  styleUrl: './coreBanck.component.scss',
  standalone: false
})
export class CoreBanckComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {
  }

    pageSize = 10;
totalItems = 3;


tableColumns: any[] = [
  {
    key: 'id',
    header: 'ID',
    sortable: true,
    width: '50px'
  },
  {
    key: 'name',
    header: 'Nombre',
    sortable: true
  },
  {
    key: 'email',
    header: 'Correo electrónico',
    sortable: true
  },
  {
    key: 'position',
    header: 'Posición',
    sortable: true
  },
  {
    key: 'appliedDate',
    header: 'Fecha de Aplicación',
    sortable: true,
    date: true
  }
];


applicants: any[] = [
  {
    id: 1,
    name: 'Juan Pérez',
    email: 'juan.perez@example.com',
    position: 'Desarrollador Frontend',
    appliedDate: new Date('2025-05-01')
  },
  {
    id: 2,
    name: 'María García',
    email: 'maria.garcia@example.com',
    position: 'Diseñadora UX/UI',
    appliedDate: new Date('2025-05-03')
  },
  {
    id: 3,
    name: 'Carlos López',
    email: 'carlos.lopez@example.com',
    position: 'Ingeniero DevOps',
    appliedDate: new Date('2025-05-04')
  }
];


handlePageChange(event: any) {
  this.pageSize = event.pageSize;
  console.log('Página cambiada:', event);
}

}
