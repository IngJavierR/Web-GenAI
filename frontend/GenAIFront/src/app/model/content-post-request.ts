export class ContentPostRequest {
    text: string;
    image_name: string;
    type: string;
    constructor(){
        this.text = '';
        this.image_name = '';
        this.type = '';
    }
}