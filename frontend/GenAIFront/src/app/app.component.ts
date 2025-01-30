import { Component } from '@angular/core';
import { ChatDocumentsComponent } from './pages/chat-documents/chat-documents.component'
import { Observable } from 'rxjs/internal/Observable';
import { DataService } from './services/data.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  isLoading: Observable<boolean>;
  
  constructor(
    private dataService: DataService,
    private snackBar: MatSnackBar,
  ) {
    this.isLoading = this.dataService.getIsLoading();

    this.dataService.getGeneralNotificationMessage().subscribe((msg) => {
      this.snackBar.open(msg, 'OK', {
        duration: 3000,
      });
    });
  }

  
  
}
