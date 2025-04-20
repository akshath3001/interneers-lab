import React, { useEffect, useState } from "react";
import Product, { ProductType } from "./Product";
import "./Product.css";

const ProductList: React.FC = () => {
  const [products, setProducts] = useState<ProductType[]>([]);
  const baseUrl = "http://127.0.0.1:8000/";
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch(`${baseUrl}products/`);
        if (!response.ok) {
          throw new Error("Failed to fetch products");
        }
        const data = await response.json();
        console.log(data.product);
        setProducts(data.product);
      } catch (error) {
        console.error("Error fetching current page data:", error);
      }
    };

    fetchProducts();
  }, []);
  return (
    <>
      <h1>Product List</h1>
      <div className="product-list">
        {products.map((product, idx) => (
          <Product key={product.product_id} product={product} />
        ))}
      </div>
    </>
  );
};
export default ProductList;
