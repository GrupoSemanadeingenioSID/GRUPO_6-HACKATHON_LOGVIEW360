import { DatePipe } from '@angular/common';
import { Component, Inject, Input } from '@angular/core';
import { MatButton } from '@angular/material/button';
import {
  MAT_DIALOG_DATA,
  MatDialogActions,
  MatDialogRef,
} from '@angular/material/dialog';
import { MatIcon } from '@angular/material/icon';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import {
  DocumentViewerData,
  TypeData,
} from '../../../core/models/documents/documents.model';
import { DocumentsService } from '../../../core/services/documents/documents.service';

@Component({
  selector: 'app-document-viewer',
  imports: [MatDialogActions, MatButton, MatIcon, DatePipe],
  templateUrl: './document-viewer.component.html',
  styleUrl: './document-viewer.component.scss',
})
export class DocumentViewerComponent {
  @Input() documentId: string = '';
  infoDocument: DocumentViewerData = {
    id_document: '',
    info: '',
    name: '',
    description: '',
    size: '',
    type: TypeData.URL,
    date_upload: new Date(),
  };

  sourceOrData: SafeResourceUrl | Base64URLString = '';
  fullScreen: boolean = false;

  constructor(
    public dialogRef: MatDialogRef<DocumentViewerComponent>,
    private sanitizer: DomSanitizer,
    private documentsService: DocumentsService,
    @Inject(MAT_DIALOG_DATA) public data: string
  ) {
    this.documentId = data;
    this.loadFile();
  }

  cerrar() {
    this.dialogRef.close();
  }

  toggleFullScreen() {
    this.fullScreen = !this.fullScreen;
    let elemento = document.querySelector(
      '.mat-mdc-dialog-surface.mdc-dialog__surface'
    )!;
    console.log(elemento);
    if (this.fullScreen) {
      this.dialogRef.updateSize('100vw', '100vh');
      elemento.classList.add('document-viewer__none_border');
    } else {
      this.dialogRef.updateSize('80vw', '80vh');
      elemento.classList.remove('document-viewer__none_border');
    }
  }

  downloadFile() {
    const link = document.createElement('a');
    link.href = this.infoDocument.info;
    link.download = this.infoDocument.name + '.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  loadFile() {
    this.documentsService.getDocument(this.documentId).subscribe({
      next: (data: DocumentViewerData) => {
        console.log(data.id_document);

        this.infoDocument = data;
        if (this.infoDocument.type === TypeData.BASE64) {
          this.sourceOrData = this.infoDocument.info.includes(
            'data:application/pdf;base64'
          )
            ? this.infoDocument.info
            : 'data:application/pdf;base64,' + this.infoDocument.info;
        }
        this.sourceOrData = this.sanitizer.bypassSecurityTrustResourceUrl(
          this.infoDocument.info
        );
      },
      error: (error) => {
        console.error('Error loading document:', error);
        this.infoDocument = {
          id_document: '',
          info: '/assets/files/documento_del_pei_IGAC.pdf',
          name: 'PEI IGAC',
          description: 'Plan Estratégico Institucional del IGAC',
          size: '30MB',
          type: TypeData.URL,
          date_upload: new Date('2023-10-01'),
        };
        this.sourceOrData = this.sanitizer.bypassSecurityTrustResourceUrl(
          this.infoDocument.info
        );
      },

    });

    if (
      this.infoDocument.type === TypeData.BASE64 &&
      this.infoDocument.info !== ''
    ) {
      this.sourceOrData = this.infoDocument.info.includes(
        'data:application/pdf;base64'
      )
        ? this.infoDocument.info
        : 'data:application/pdf;base64,' + this.infoDocument.info;
    }
    this.sourceOrData = this.sanitizer.bypassSecurityTrustResourceUrl(
      this.infoDocument.info
    );
  }
}
