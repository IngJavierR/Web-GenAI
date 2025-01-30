import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { Subject } from 'rxjs/internal/Subject';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  private isLoading = new Subject<boolean>();
  private generalNotificationMessage = new Subject<string>();

  setIsLoading(loading: boolean): void {
    this.isLoading.next(loading);
  }

  getIsLoading(): Observable<boolean> {
    return this.isLoading.asObservable();
  }

  getGeneralNotificationMessage(): Observable<string> {
    return this.generalNotificationMessage.asObservable();
  }

  setGeneralNotificationMessage(msg: string): void {
    this.generalNotificationMessage.next(msg);
  }
}
