export class ContentRequest {
    query: string;
    include_image: boolean;
    use_context: boolean
    constructor(){
        this.query = '';
        this.include_image = false;
        this.use_context = false;
    }
}