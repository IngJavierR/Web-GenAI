import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-image-viewer',
  templateUrl: './image-viewer.component.html',
  styleUrls: ['./image-viewer.component.css']
})
export class ImageViewerComponent implements OnInit {

  @Input() images: string[] = []; // Arreglo de imágenes en Base64
  @Input() orientation: 'horizontal' | 'vertical' = 'horizontal'; // Orientación del carrusel
  mainImage: string = ''; // Imagen principal

  constructor() { }

  ngOnInit(): void {
    // Establecer la primera imagen como principal por defecto
    if (this.images.length > 0) {
      this.mainImage = this.images[0];
    }
  }

  changeMainImage(image: string) {
    this.mainImage = image;
  }
}
