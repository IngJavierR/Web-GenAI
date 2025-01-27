import { Component, OnInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';

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

  displayedColumns: string[] = ['id', 'nombre', 'apellido', 'fecha_nacimiento', 'email'];
  
  dataSource = new MatTableDataSource<Profile>([
    { id: 1, nombre: 'Juan', apellido: 'Perez', fecha_nacimiento: new Date('1990-01-01'), email: 'juan.perez@example.com' },
    { id: 2, nombre: 'Ana', apellido: 'Gomez', fecha_nacimiento: new Date('1985-05-15'), email: 'ana.gomez@example.com' },
    { id: 3, nombre: 'Luis', apellido: 'Martinez', fecha_nacimiento: new Date('1978-11-30'), email: 'luis.martinez@example.com' }
  ]);

  workExperience = [
    '2020-2023: Senior Designer at Company A',
    '2018-2020: Junior Designer at Company B',
    '2016-2018: Intern at Company C'
  ];

  education = [
    '2006-2010: Bachelor of Design, University A',
    '2010-2012: Master of Design, University B'
  ];

  skills = [
    { name: 'Graphic Design', level: 80 },
    { name: 'Web Design', level: 70 },
    { name: 'Logo Design', level: 60 }
  ];

  uploadedFile: File | null = null;

  ngOnInit(): void {
    this.dataSource.filterPredicate = (data: Profile, filter: string) => {
      const dataStr = Object.values(data).join(' ').toLowerCase();
      return dataStr.includes(filter);
    };
  }

  onRowClicked(selectedProfile: Profile) : void {
    
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.uploadedFile = files[0];
      console.log('Uploaded file:', this.uploadedFile);
    }
  }
}
