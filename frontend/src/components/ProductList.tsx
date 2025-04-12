import React, { useState } from "react";
import Product from "./Product";
import "./Product.css";

const ProductList: React.FC = () => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
  const dummyProducts = [
    {
      product_name: "Nikon Z8",
      product_category: ["Camera", "Electronics"],
      product_description: "Advanced mirrorless camera for professionals",
      product_price: 280000.0,
      product_brand: "Nikon",
      product_quantity: 2,
    },
    {
      product_name: "Sony WH-1000XM5",
      product_category: ["Audio", "Electronics"],
      product_description: "Industry-leading noise cancelling headphones",
      product_price: 29999.0,
      product_brand: "Sony",
      product_quantity: 10,
    },
    {
      product_name: "Apple MacBook Pro M2",
      product_category: ["Laptop", "Electronics"],
      product_description: "Powerful laptop with M2 chip and Retina display",
      product_price: 189900.0,
      product_brand: "Apple",
      product_quantity: 5,
    },
    {
      product_name: "Samsung Galaxy S24 Ultra",
      product_category: ["Smartphone", "Electronics"],
      product_description: "Flagship smartphone with pro-grade camera",
      product_price: 129999.0,
      product_brand: "Samsung",
      product_quantity: 8,
    },
    {
      product_name: "Canon RF 50mm f/1.2L",
      product_category: ["Lens", "Camera"],
      product_description: "Premium lens with excellent low-light performance",
      product_price: 185000.0,
      product_brand: "Canon",
      product_quantity: 3,
    },
  ];
  const handleToggle = (index: number) => {
    setExpandedIndex((prevIndex) => (prevIndex === index ? null : index));
  };
  return (
    <>
      <h1>Product List</h1>
      <div className="product-list">
        {dummyProducts.map((product, idx) => (
          <Product
            key={idx}
            product={product}
            isExpanded={expandedIndex === idx}
            onClick={() => handleToggle(idx)}
          />
        ))}
      </div>
    </>
  );
};
export default ProductList;
