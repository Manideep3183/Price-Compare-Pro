export interface Product {
  product_name: string;
  price: number;
  rating: number;
  product_url: string;
  image_url: string;
  retailer: string;
  final_score: number;
  recommendation: string;
  discount?: string;
}
