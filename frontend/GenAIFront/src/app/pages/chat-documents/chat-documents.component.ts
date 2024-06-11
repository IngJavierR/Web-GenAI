import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { LangChainServiceService } from '../../services/lang-chain-service.service'
import { QueryResponse } from 'src/app/model/query-response';
import { VoiceRecognitionService } from 'src/app/services/voice-recognition.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

interface Message {
  text: string;
  isUser: boolean;
}

@Component({
  selector: 'app-chat-documents',
  templateUrl: './chat-documents.component.html',
  styleUrls: ['./chat-documents.component.css']
})
export class ChatDocumentsComponent implements OnInit {

  userInput: string = '';
  messages: Message[] = [];
  modeType = 0;
  btnIcon = 'mic';
  @ViewChild('scrollMe') private myScrollContainer: ElementRef | undefined;

  public isUserSpeaking: boolean = false;

  constructor(
    private fb: FormBuilder,
    private langService: LangChainServiceService,
    private voiceRecognition: VoiceRecognitionService
  ) { }

  ngOnInit(): void {
    this.initVoiceInput();
  }

  ngAfterViewInit() {
    // After the view initializes, we can safely access the myScrollContainer
    this.scrollToBottom();
  }

  initVoiceInput() {
    // Subscription for initializing and this will call when user stopped speaking.
    this.voiceRecognition.init().subscribe(() => {
      // User has stopped recording
      // Do whatever when mic finished listening
    });

    // Subscription to detect user input from voice to text.
    this.voiceRecognition.speechInput().subscribe((input) => {
      // Set voice text output to
      // Set voice text output to
      this.userInput = input;
      //this.searchForm.controls['searchText'].setValue(input);
    });
  }

  actionRecording() {
    if(this.btnIcon === 'stop'){
      this.btnIcon = 'mic';
      this.voiceRecognition.stop()
      this.isUserSpeaking = false;
      if(this.userInput) {
        this.sendMessage(true);
      }
    }else{
      this.btnIcon = 'stop';
      this.isUserSpeaking = true;
      this.voiceRecognition.start();
      this.userInput = '';
    }
  }

  sendMessage(isAudio: boolean) {
    if (this.userInput.trim()) {
      let query = this.userInput;
      this.messages.push({ text: this.userInput, isUser: true });
      this.userInput = '';
      setTimeout(() => {
        this.scrollToBottom();
      }, 100);
      
      console.log('ModeType:', this.modeType);

      if(this.modeType === 1){
        this.langService.queryDocuments(query).subscribe((response: QueryResponse) => {
          if(isAudio){
            this.voiceRecognition.speech(response.result);
          }
          this.messages.push({ text: response.result, isUser: false });
          setTimeout(() => {
            this.scrollToBottom();
          }, 100);
        })
      }

      else if(this.modeType === 0){ 
        this.langService.querySql(query).subscribe((response: QueryResponse) => {
          if(isAudio){
            this.voiceRecognition.speech(response.result);
          }
          this.messages.push({ text: response.result, isUser: false });
          setTimeout(() => {
            this.scrollToBottom();
          }, 100);
        })
      }

      //Simulación de respuesta del bot
      // setTimeout(() => {
      //   let text = 'Esta es una respuesta automática.';
      //   this.voiceRecognition.speech(text);
      //   this.messages.push({ text: text, isUser: false });
      //   setTimeout(() => {
      //     this.scrollToBottom();
      //   }, 100);
      // }, 1000);
    }
  }

  mode(type: number) {
    this.modeType = type
  }

  scrollToBottom(): void {
    if (this.myScrollContainer) {
      try {
        this.myScrollContainer.nativeElement.scrollTop = this.myScrollContainer.nativeElement.scrollHeight;
      } catch(err) { }
    }
  }

}
