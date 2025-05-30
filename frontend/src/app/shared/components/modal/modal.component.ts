import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

export interface ModalData {
  type: 'success' | 'error' | 'info' | 'warning';
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  showCancel?: boolean;
}

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss'],
  standalone: true,
  imports: [CommonModule, MatDialogModule, MatButtonModule, MatIconModule]
})
export class ModalComponent {
  constructor(
    public dialogRef: MatDialogRef<ModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ModalData
  ) {
    // Set defaults if not provided
    this.data.confirmText = this.data.confirmText || 'Aceptar';
    this.data.cancelText = this.data.cancelText || 'Cancelar';
    this.data.showCancel = this.data.showCancel !== undefined ? this.data.showCancel : false;
  }

  onConfirm(): void {
    this.dialogRef.close(true);
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }

  getIconForType(): string {
    switch (this.data.type) {
      case 'success':
        return 'check_circle_outline';
      case 'error':
        return 'error_outline';
      case 'warning':
        return 'warning_amber';
      case 'info':
        return 'info_outline';
      default:
        return 'info_outline';
    }
  }

  getButtonClass(): string {
    switch (this.data.type) {
      case 'success':
        return 'btn-success';
      case 'error':
        return 'btn-error';
      case 'warning':
        return 'btn-warning';
      case 'info':
        return 'btn-info';
      default:
        return 'btn-default';
    }
  }


}
