import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Observable } from 'rxjs';
import { ModalComponent, ModalData } from '../../../shared/components/modal/modal.component';

@Injectable({
  providedIn: 'root'
})
export class ModalService {
  constructor(private dialog: MatDialog) {}

  openModal(data: ModalData): Observable<boolean> {
    const dialogRef = this.dialog.open(ModalComponent, {
      data: data,
      disableClose: false
    });

    return dialogRef.afterClosed();
  }

  openSuccessModal(title: string, message: string): Observable<boolean> {
    return this.openModal({
      type: 'success',
      title,
      message,
      confirmText: 'Aceptar',
      showCancel: false
    });
  }

  openErrorModal(title: string, message: string): Observable<boolean> {
    return this.openModal({
      type: 'error',
      title,
      message,
      confirmText: 'Aceptar',
      showCancel: false
    });
  }

  openWarningModal(title: string, message: string): Observable<boolean> {
    return this.openModal({
      type: 'warning',
      title,
      message,
      confirmText: 'Aceptar',
      cancelText: 'Cancelar',
      showCancel: true,
    });
  }

  openInfoModal(title: string, message: string): Observable<boolean> {
    return this.openModal({
      type: 'info',
      title,
      message,
      confirmText: 'Aceptar',
      showCancel: false
    });
  }

  openConfirmationModal(title: string, message: string): Observable<boolean> {
    return this.openModal({
      type: 'info',
      title,
      message,
      confirmText: 'Confirmar',
      cancelText: 'Cancelar',
      showCancel: true
    });
  }
}
