import { Component, OnInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { ResumeResponse } from 'src/app/model/resume-response';
import { LangChainServiceService } from 'src/app/services/lang-chain-service.service';
import { DataService } from '../../services/data.service';

interface Profile {
  id: number;
  nombre: string;
  apellido: string;
  fecha_nacimiento: Date;
  email: string;
}

@Component({
  selector: 'app-document-processing',
  templateUrl: './document-processing.component.html',
  styleUrls: ['./document-processing.component.css']
})
export class DocumentProcessingComponent implements OnInit {

  formData = new FormData()
  profile = new ResumeResponse();

  constructor(
      private langService: LangChainServiceService,
      private dataService: DataService
    ) { }

  displayedColumns: string[] = ['id', 'nombre', 'apellido', 'telefono', 'email'];

  dataSource = new MatTableDataSource<ResumeResponse>([]);

  uploadedFile: File | null = null;

  ngOnInit(): void {
    this.reloadResumes();
  }

  reloadResumes() {
    this.dataService.setIsLoading(true);
    this.langService.resumeGet().subscribe((response: ResumeResponse[])=> {
      this.dataSource.data = response
      console.log('Response', response);
      this.dataService.setIsLoading(false);
    }, (error: Error) => {
      this.dataService.setIsLoading(false);
      this.dataService.setGeneralNotificationMessage(error.message);
    });
  }

  onRowClicked(selectedProfile: ResumeResponse) : void {
    this.profile = selectedProfile;
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.uploadedFile = files[0];
      let fileBlob = new Blob([this.uploadedFile], {type: this.uploadedFile.type});

      this.formData = new FormData();
      this.formData.append("files[]", fileBlob, this.uploadedFile.name);
      this.formData.append("catalog", "people");
      this.dataService.setIsLoading(true);
      this.langService.resumeUpload(this.formData).subscribe((response: any)=> {
        this.reloadResumes();
        this.dataService.setIsLoading(false);
      }, (error: Error) => {
        this.dataService.setIsLoading(false);
        this.dataService.setGeneralNotificationMessage(error.message);
      });

      console.log('Uploaded file:', this.uploadedFile);
    }
  }
}
