import { Injectable, signal } from '@angular/core';


@Injectable({
  providedIn: 'root'
})
export class UIStateService {
  // Signal for page title
  private titleSignal = signal<string>('Home');

private sidebarItemsSignal = signal<any[]>([
  {
    name: 'Analisis',
    isActive: true,
    subitems: [
  { name: 'General', url: '/individual', icon: 'dashboard' },
  { name: 'Secure',  url: '/secuCheck', icon: 'security' },
  { name: 'Mid',     url: '/midFlow', icon: 'swap_horiz' },
  { name: 'Core',    url: '/coreBank', icon: 'account_balance' }
  ]

  }
]);

  private searchboxVisibleSignal = signal<boolean>(true);
  private userProfileSignal = signal<any>({
    name: 'Gludcito',
    role: 'Revisor',
    email: 'glud@eglud.com',
    picture: '/assets/images/sample_avatar.png',
  });

  // Expose read-only signals
  public title = this.titleSignal.asReadonly();
  public sidebarItems = this.sidebarItemsSignal.asReadonly();
  public searchboxVisible = this.searchboxVisibleSignal.asReadonly();
  public userProfile = this.userProfileSignal.asReadonly();

  constructor() {}

  // Methods to update signals
  setTitle(title: string): void {
    this.titleSignal.set(title);
  }

  setSidebarItems(items: any[]): void {
    this.sidebarItemsSignal.set(items);
  }

  updateSidebarItem(index: number, item: any): void {
    const currentItems = this.sidebarItemsSignal();
    const newItems = [...currentItems];
    newItems[index] = item;
    this.sidebarItemsSignal.set(newItems);
  }

  toggleSidebarSubMenu(index: number): void {
    const currentItems = this.sidebarItemsSignal();
    const newItems = [...currentItems];
    newItems[index] = {
      ...newItems[index],
      isActive: !newItems[index].isActive
    };
    this.sidebarItemsSignal.set(newItems);
  }

  setSearchboxVisibility(visible: boolean): void {
    this.searchboxVisibleSignal.set(visible);
  }

  toggleSearchboxVisibility(): void {
    this.searchboxVisibleSignal.update(value => !value);
  }

  // User profile methods
  setUserProfile(profile: any): void {
    this.userProfileSignal.set(profile);
  }

  updateUserProfile(partialProfile: Partial<any>): void {
    this.userProfileSignal.update(profile => ({
      ...profile,
      ...partialProfile
    }));
  }

  clearUserProfile(): void {
    const currentProfile = this.userProfileSignal();
    if (currentProfile.refreshTokenTimeout) {
      clearTimeout(currentProfile.refreshTokenTimeout);
    }
    this.userProfileSignal.set({
      name: '',
      role: '',
    });
  }
}
