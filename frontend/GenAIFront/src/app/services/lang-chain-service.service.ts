import { Injectable } from '@angular/core';
import { Observable, Subscriber } from 'rxjs';
import { environment } from 'src/environments/environment';
import { HttpHeaders, HttpClient, HttpParams } from '@angular/common/http';
import { QueryResponse } from '../model/query-response';

@Injectable({
  providedIn: 'root'
})
export class LangChainServiceService {

  constructor(
    private http: HttpClient
  ) { }

  querySql(query: string): Observable<QueryResponse> {
    return new Observable<any>((observer) => {
        this.http.post<any>(environment.chat_sql, {
          query: query
        }).subscribe((response) => {
          this.returnResponse(observer, response)
        }, (err)=>{
          this.returnError(observer, err)
        })
    }) 
  }

  queryDocuments(query: string): Observable<QueryResponse> {
    return new Observable<any>((observer) => {
        this.http.post<any>(environment.chat_documents, {
          query: query
        }).subscribe((response) => {
          this.returnResponse(observer, response)
        }, (err)=>{
          this.returnError(observer, err)
        })
    }) 
  }

  private returnResponse<T>(observer: Subscriber<T>, response: any): void {
    observer.next(response);
    observer.complete();
  }

  private returnError<T>(observer: Subscriber<T>, error: any): void {
    observer.error(error);
  }

}
