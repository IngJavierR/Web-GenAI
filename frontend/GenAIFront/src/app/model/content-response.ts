export class ContentResponse {
    tweet_content: string;
    post_content: string;
    email_content: string;
    image_base64: string;
    image_name: string;
    constructor(){
        this.tweet_content = '';
        this.post_content = '';
        this.email_content = ''
        this.image_base64 = '';
        this.image_name = '';
    }
}