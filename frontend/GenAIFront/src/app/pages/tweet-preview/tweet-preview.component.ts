import { Component } from '@angular/core';
import { LangChainServiceService } from '../../services/lang-chain-service.service'
import { ContentResponse } from 'src/app/model/content-response';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { log } from 'console';

@Component({
  selector: 'app-tweet-preview',
  templateUrl: './tweet-preview.component.html',
  styleUrls: ['./tweet-preview.component.css']
})
export class TweetPreviewComponent {
  prompt: string = '';
  tweetText: string = '';
  postText: string = '';
  emailText: string = '';
  isImageRequired: boolean = false;
  isContextRequired: boolean = false;
  image: string | SafeResourceUrl | null = null;
  imageName: string = '';
  previewGenerated: boolean = false;

  selectedFile: any;
  fileName = '';
  formData = new FormData()

  constructor(
    private langService: LangChainServiceService,
    private _sanitizer: DomSanitizer
  ) { }

  onFileSelected(event: any) {
    this.selectedFile = (event.target as HTMLInputElement).files;
    
    console.log("Files", this.selectedFile[0].name);
    
    if(this.selectedFile) {
      const file = this.selectedFile[0];
      let fileBlob = new Blob([file], {type: this.selectedFile.type});
      
      this.formData = new FormData();
      this.formData.append("files[]", fileBlob, this.selectedFile[0].name);
      this.formData.append("catalog", "contentmanager");
      this.langService.fileUpload(this.formData).subscribe((response: any)=> {});
   }
  }

  uploadFile() {

  }

  generatePreview() {
    this.langService.contentPreview({
      query: this.prompt,
      include_image: this.isImageRequired,
      use_context: this.isContextRequired
    }).subscribe((response: ContentResponse) => {
      this.tweetText = response.tweet_content;
      this.postText = response.post_content;
      this.emailText = response.email_content;
      this.image = this._sanitizer.bypassSecurityTrustResourceUrl('data:image/jpg;base64,' 
        + response.image_base64);
      this.imageName = response.image_name;
      this.previewGenerated = true;
    });
  }

  publishTweet() {
    this.langService.contentPost({
      image_name: this.imageName,
      text: this.tweetText,
      type: 'twitter'
    }).subscribe((response: any) => {
      console.log('Tuit publicado:', this.tweetText, this.image);
    });
  }

  publishFacebook() {
    this.langService.contentPost({
      image_name: this.imageName,
      text: this.postText,
      type: 'facebook',
    }).subscribe((response: any) => {
      console.log('Post publicado:', this.tweetText, this.image);
    });
  }

  publishEmail() {
    this.langService.contentPost({
      image_name: this.imageName,
      text: this.postText,
      type: 'email',
    }).subscribe((response: any) => {
      console.log('Email enviado:', this.tweetText, this.image);
    });
  }
}
