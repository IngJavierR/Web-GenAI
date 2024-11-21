import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-product-detail-ml',
  templateUrl: './product-detail-ml.component.html',
  styleUrls: ['./product-detail-ml.component.css']
})
export class ProductDetailMlComponent implements OnInit {
  @Input() product: any;
  
  constructor() { }

  ngOnInit(): void {
  }

}
