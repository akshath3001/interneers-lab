import React from "react";
import "./Product.css";

interface ProductProps {
  product: {
    product_name: string;
    product_category: string[];
    product_description: string;
    product_price: number;
    product_brand: string;
    product_quantity: number;
  };
  isExpanded: boolean;
  onClick: () => void;
}

const Product: React.FC<ProductProps> = ({ product, isExpanded, onClick }) => {
  return (
    <div
      className={`product-card ${isExpanded ? "expanded" : ""}`}
      onClick={onClick}
    >
      <h2>{product.product_name}</h2>
      <p>
        <strong>Price:</strong> Rs. {product.product_price}
      </p>
      {isExpanded && (
        <div className="product-details">
          <p>
            <strong>Brand:</strong> {product.product_brand}
          </p>
          <p>
            <strong>Categories:</strong> {product.product_category.join(", ")}
          </p>
          <p>
            <strong>Description:</strong> {product.product_description}
          </p>
          <p>
            <strong>In Stock:</strong> {product.product_quantity}
          </p>
        </div>
      )}
    </div>
  );
};
export default Product;
