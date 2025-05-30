import { Overlay, OverlayPositionBuilder, OverlayRef } from '@angular/cdk/overlay';
import { DOCUMENT } from '@angular/common';
import { Component, ElementRef, Inject, Renderer2, ViewContainerRef } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { UIStateService } from '../../../../core/signals/ui-state.service';

/**
 * Component representing the top bar of the application.
 *
 * This component provides functionality for toggling between dark mode and light mode,
 * as well as opening a filter overlay. It uses Angular's `Renderer2` to dynamically
 * manipulate the root HTML element's CSS classes for theme switching.
 *
 * @selector app-topbar
 * @templateUrl ./topbar.component.html
 * @styleUrl ./topbar.component.scss
 */
@Component({
  selector: 'app-topbar',
  standalone: false,
  templateUrl: './topbar.component.html',
  styleUrl: './topbar.component.scss'
})
export class TopbarComponent {
    darkMode = false;
    private overlayRef: OverlayRef | null = null;
    searchControl = new FormControl('');

    constructor(
      private renderer: Renderer2,
      @Inject(DOCUMENT) private document: Document,
      private snackBar: MatSnackBar,
      public uiStateService: UIStateService,
      private overlay: Overlay,
      private overlayPositionBuilder: OverlayPositionBuilder,
      private elementRef: ElementRef,
      private viewContainerRef: ViewContainerRef
    ) {}

    ngOnInit() {
      const root = this.document.documentElement;
      this.renderer.addClass(root, 'light-theme');
    }

    performSearch(event: Event) {
      event.preventDefault();
      const searchValue = this.searchControl.value?.trim();

      if (!searchValue) {
        this.snackBar.open('Ingresa un término de búsqueda', 'Cerrar', {
          duration: 3000
        });
        return;
      }

      console.log('Performing search with:', searchValue);

    }


    private closeOverlay() {
      if (this.overlayRef) {
        this.overlayRef.dispose();
        this.overlayRef = null;
      }
    }

    openFilterDialog(event){
      console.log('Opening filter dialog', event);

    }
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      const root = this.document.documentElement;
      if (this.darkMode) {
        this.renderer.addClass(root, 'dark-theme');
        this.renderer.removeClass(root, 'light-theme');
      } else {
        this.renderer.addClass(root, 'light-theme');
        this.renderer.removeClass(root, 'dark-theme');
      }
    }

    toggleSearchVisibility() {
      this.uiStateService.toggleSearchboxVisibility();
    }
}
