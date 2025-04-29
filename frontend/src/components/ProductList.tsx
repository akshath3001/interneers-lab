import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Product, { ProductType } from "./Product";
import "./Product.css";

const ProductList: React.FC = () => {
  const [products, setProducts] = useState<ProductType[]>([]);
  const navigate = useNavigate();
  const baseUrl = "http://127.0.0.1:8000/";

  const fetchProducts = async () => {
    try {
      const response = await fetch(`${baseUrl}products/`);
      if (!response.ok) throw new Error("Failed to fetch products");
      const data = await response.json();
      setProducts(data.product);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleDelete = async (id: string) => {
    try {
      const res = await fetch(`${baseUrl}products/${id}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Failed to delete");
      setProducts((prev) => prev.filter((p) => p.product_id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  const handleEdit = (id: string) => {
    navigate(`/productform/${id}`);
  };

  const handleAdd = () => {
    navigate("/productform");
  };

  return (
    <div>
      <h1>Product List</h1>
      <button className="add-btn" onClick={handleAdd}>
        Add New Product
      </button>
      <div className="product-list">
        {products.map((product) => (
          <Product
            key={product.product_id}
            product={product}
            onDelete={() => handleDelete(product.product_id)}
            onEdit={() => handleEdit(product.product_id)}
          />
        ))}
      </div>
    </div>
  );
};

export default ProductList;
