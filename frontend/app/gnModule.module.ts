import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { Routes, RouterModule } from "@angular/router";
import { HttpClientXsrfModule } from "@angular/common/http";
import { GN2CommonModule } from "@geonature_common/GN2Common.module";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
import { ConfigModule } from "@geonature/utils/configModule/core";

import { ExportListComponent } from "./export-list/export-list.component";

import { ExportService } from "./services/export.service";

const routes: Routes = [{ path: "", component: ExportListComponent }];

@NgModule({
  imports: [
    HttpClientXsrfModule.withOptions({
      cookieName: "token",
      headerName: "token"
    }),
    CommonModule,
    GN2CommonModule,
    NgbModule.forRoot(),
    RouterModule.forChild(routes),
    ConfigModule.forChild()
  ],
  declarations: [ExportListComponent],
  providers: [ExportService],
  bootstrap: []
})
export class GeonatureModule {}
