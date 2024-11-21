import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'marketplace',
  templateUrl: './marketplace.component.html',
  styleUrls: ['./marketplace.component.css']
})
export class MarketplaceComponent implements OnInit  {
  productData: any = null;
  isLoading: boolean = false;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {

  }

  fetchProductData() {
    this.isLoading = true;
    this.http.get('http://127.0.0.1:8095/marketplace').subscribe(
      (response) => {
        this.productData = response;
        this.isLoading = false;
      },
      (error) => {
        console.error('Error fetching product data', error);
        this.isLoading = false;
      }
    );
  }
}
