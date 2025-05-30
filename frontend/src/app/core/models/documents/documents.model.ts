export enum TypeData {
  BASE64 = 'base64',
  URL = 'url',
}
export interface DocumentViewerData {
  id_document: string;
  info: string;
  name: string;
  description: string;
  size: string;
  type: TypeData;
  date_upload: Date;
}
