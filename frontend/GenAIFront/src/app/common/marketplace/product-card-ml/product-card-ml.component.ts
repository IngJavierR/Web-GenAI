import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-product-card-ml',
  templateUrl: './product-card-ml.component.html',
  styleUrls: ['./product-card-ml.component.css']
})
export class ProductCardMlComponent implements OnInit {
  @Input() product: any;

  constructor() { }

  ngOnInit(): void {
  }

}
