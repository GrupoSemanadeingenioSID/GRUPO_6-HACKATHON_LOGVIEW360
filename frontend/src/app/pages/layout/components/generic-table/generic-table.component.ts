import { SelectionModel } from '@angular/cdk/collections';
import {
  AfterViewInit,
  Component,
  effect,
  EventEmitter,
  HostBinding,
  input,
  Input,
  OnChanges,
  OnInit,
  Output,
  signal,
  SimpleChanges,
  TemplateRef,
  ViewChild
} from '@angular/core';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';

export interface ColumnDefinition {
  key: string;
  sortable: boolean;
  header: string;
  width?: string;
  cellTemplate?: TemplateRef<any>;
  domain?: any;
  composeDomains?: any[];
  compose?: any;
  date?: boolean;
}

export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}

@Component({
  selector: 'app-generic-table',
  standalone: false,
  templateUrl: './generic-table.component.html',
  styleUrls: ['./generic-table.component.scss'],
})
export class GenericTableComponent implements OnInit, AfterViewInit, OnChanges {
  @HostBinding('style.--header-radius') headerRadiusStyle: string;
  @HostBinding('style.--cell-vertical-padding') cellPaddingStyle: string;

  @Input() columns: ColumnDefinition[] = [];
  @Input() data: any[] = [];
  @Input() pageSizeOptions: number[] = [5, 10, 20];
  @Input() totalItems: number = 0;
  @Input() pageSize: number = 10;
  @Input() pageIndex: number = 0;
  @Input() selectable: boolean = false;
  @Input() sizeSelectable: boolean = true;

  showEdit = input<boolean>(false);
  showDetails = input<boolean>(false);
  showDelete = input<boolean>(false);
  showPaginator = input<boolean>(true);
  headerRadius = input<string>('16px');
  cellPadding = input<string>('10px');

  showActions = signal(false);

  @Output() selectionChange: EventEmitter<any[]> = new EventEmitter<any[]>();
  @Output() pageChange: EventEmitter<{ pageIndex: number; pageSize: number }> =
    new EventEmitter();
  @Output() shortChange: EventEmitter<{
    shortOrder: String;
    shortColumn: String;
  }> = new EventEmitter();
  @Output() buttonEvent: EventEmitter<{
    row: any;
    actionPerformed: string;
  }> = new EventEmitter();

  displayedColumns: string[];
  dataSource: any;

  constructor() {
    effect(() => {
      this.showActions.set(
        this.showDelete() || this.showEdit() || this.showDetails()
      );
      this.updateDisplayedColumns();
    });

    effect(() => {
      this.headerRadiusStyle = this.headerRadius();
    });
    effect(() => {
      this.cellPaddingStyle = this.cellPadding();
    });
  }

  selection = new SelectionModel<any>(true, []);

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  ngOnInit() {
    this.dataSource = new MatTableDataSource<any>(this.data);
  }

  ngAfterViewInit() {}

  ngOnChanges(changes: SimpleChanges): void {
    this.dataSource = [...this.data];
  }

  updateDisplayedColumns() {
    this.displayedColumns = [...this.columns.map((col) => col.key)];
    if (this.showActions()) {
      this.displayedColumns.push('actions');
    }
    if (this.selectable) {
      this.displayedColumns.unshift('select');
    }
  }

  onPageChange(event: PageEvent) {
    this.pageIndex = event.pageIndex;
    this.pageSize = event.pageSize;
    this.pageChange.emit({
      pageIndex: this.pageIndex,
      pageSize: this.pageSize,
    });
  }

  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  toggleAllRows() {
    if (this.isAllSelected()) {
      this.selection.clear();
    } else {
      this.selection.select(...this.dataSource.data);
    }
    this.emitSelectionChange();
  }

  onHeaderCheckboxChange() {
    this.toggleAllRows();
  }

  onRowCheckboxChange(row: any) {
    this.selection.toggle(row);
    this.emitSelectionChange();
  }

  emitSelectionChange() {
    this.selectionChange.emit(this.selection.selected);
  }

  checkboxLabel(row?: any): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${
      row.key
    }`;
  }

  applyCustomOption(option: string, columnName: string) {
    this.shortChange.emit({ shortOrder: option, shortColumn: columnName });
  }

  buttonClick(row: any, actionPerformed: string) {
    this.buttonEvent.emit({
      row: row,
      actionPerformed: actionPerformed,
    });
  }

  refresh(): void {
    this.dataSource = new MatTableDataSource<any>(this.data);
  }

}
