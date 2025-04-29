import React from "react";
import "./Product.css";
import { Link } from "react-router-dom";

interface Category {
  category_id: string;
  category_name: string;
  category_description: string;
}

export interface ProductType {
  product_id: string;
  product_name: string;
  category: Category[];
  product_description: string;
  product_price: number;
  product_brand: string;
  product_quantity: number;
}

interface ProductProps {
  product: ProductType;
  onDelete: () => void;
  onEdit: () => void;
}

const Product: React.FC<ProductProps> = ({ product, onDelete, onEdit }) => {
  return (
    <div className="product-card">
      <details>
        <summary>
          <h3>{product.product_name}</h3>
          <span className="bold-text">Price:</span> Rs. {product.product_price}
          <div className="product-actions">
            <button className="edit-btn" onClick={onEdit}>
              Edit
            </button>
            <button className="delete-btn" onClick={onDelete}>
              Delete
            </button>
          </div>
        </summary>
        <div className="product-details">
          <p>
            <span className="bold-text">Brand:</span> {product.product_brand}
          </p>
          <p>
            <span className="bold-text">Categories:</span>{" "}
            {product.category.map((category) => (
              <li key={category.category_id}>
                <Link to={`/categoryproducts/${category.category_id}`}>
                  {category.category_name}
                </Link>
              </li>
            ))}
          </p>
          <p>
            <span className="bold-text">Description:</span>{" "}
            {product.product_description}
          </p>
          <p>
            <span className="bold-text">In Stock:</span>{" "}
            {product.product_quantity}
          </p>
        </div>
      </details>
    </div>
  );
};
export default Product;
