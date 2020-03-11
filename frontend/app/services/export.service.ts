import { Injectable } from "@angular/core";
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { ConfigService } from "@geonature/utils/configModule/core";

export interface Export {
  id: number;
  label: string;
  schema: string;
  view: string;
  desc: string;
  geometry_field: string;
  geometry_srid: number;
}

export interface ApiErrorResponse extends HttpErrorResponse {
  error: any | null;
  message: string;
}

@Injectable()
export class ExportService {
  public ABSOLUTE_MODULE_URL: string;
  private _configService: ConfigService;
  constructor(private _api: HttpClient) {
    this.ABSOLUTE_MODULE_URL =
      this._configService.getSettings("API_ENDPOINT") +
      "/" +
      this._configService.getSettings("EXPORTS.MODULE_URL");
  }

  getExports() {
    return this._api.get(this.ABSOLUTE_MODULE_URL);
  }

  downloadExport(x: Export, format: string, data: any) {
    return this._api.post<any>(
      `${this.ABSOLUTE_MODULE_URL}}/${x.id}/${format}`,
      data
    );
  }
}
