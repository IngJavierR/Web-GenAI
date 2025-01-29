import { Injectable } from '@angular/core';
import { Observable, Subscriber } from 'rxjs';
import { environment } from 'src/environments/environment';
import { HttpHeaders, HttpClient, HttpParams } from '@angular/common/http';
import { QueryResponse } from '../model/query-response';
import { ContentResponse } from '../model/content-response';
import { ContentRequest } from '../model/content-request';
import { ContentPostRequest } from '../model/content-post-request';
import { RecipeResponse } from '../model/recipe-response';
import { ResumeResponse } from '../model/resume-response';

@Injectable({
  providedIn: 'root'
})
export class LangChainServiceService {

  constructor(
    private http: HttpClient
  ) { }

  querySql(query: string, catalog: string): Observable<QueryResponse> {
    return new Observable<any>((observer) => {
        this.http.post<any>(environment.chat_sql, {
          query: query,
          catalog: catalog
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

  contentPreview(query: ContentRequest): Observable<ContentResponse> {
    let objParams = new HttpParams();
    objParams = objParams.append('query', query.query);
    objParams = objParams.append('image', query.include_image);
    objParams = objParams.append('context', query.use_context);
    return new Observable<any>((observer) => {
        this.http.get<any>(environment.content, {params: objParams}).subscribe((response) => {
          this.returnResponse(observer, response)
        }, (err)=>{
          this.returnError(observer, err)
        })
    }) 
  }

  contentPost(contentPost: ContentPostRequest): Observable<any> {
    return new Observable<any>((observer) => {
        this.http.post<any>(environment.content, contentPost).subscribe((response) => {
          this.returnResponse(observer, response)
        }, (err)=>{
          this.returnError(observer, err)
        })
    }) 
  }

  fileUpload(formData: FormData): Observable<any> {

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'multipart/form-data',
        'Accept': "*/*"
      })
    };

    return new Observable<any>((observer) => {
        this.http.post<any>(environment.files, formData).subscribe((response) => {
          this.returnResponse(observer, response)
        }, (err)=>{
          this.returnError(observer, err)
        })
    }) 
  }

  resumeUpload(formData: FormData): Observable<any> {

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'multipart/form-data',
        'Accept': "*/*"
      })
    };

    return new Observable<any>((observer) => {
        this.http.post<any>(environment.resumes, formData).subscribe((response) => {
          this.returnResponse(observer, response)
        }, (err)=>{
          this.returnError(observer, err)
        })
    }) 
  }

  resumeGet(): Observable<ResumeResponse[]> {
    return new Observable<any>((observer) => {
      let objParams = new HttpParams();
      objParams = objParams.append('catalog', 'people');
        this.http.get<any>(environment.resumes, {params: objParams}).subscribe((response) => {
          this.returnResponse(observer, response)
        }, (err)=>{
          this.returnError(observer, err)
        })
    }) 
  }

  recipeGet(query: string): Observable<RecipeResponse> {
    return new Observable<any>((observer) => {
      let objParams = new HttpParams();
      objParams = objParams.append('query', query);
        this.http.get<any>(environment.recipe, {params: objParams}).subscribe((response) => {
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
