import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-product-detail',
  templateUrl: './product-detail.component.html',
  styleUrls: ['./product-detail.component.css']
})
export class ProductDetailComponent implements OnInit {
  @Input() product: any;
  @Input() orientation: 'horizontal' | 'vertical' = 'horizontal'; // Orientación del carrusel
  
  constructor() { }

  ngOnInit(): void {
  }

}
