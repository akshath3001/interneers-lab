import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ProductType } from "./Product";
import "./Product.css";

const ProductForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formState, setFormState] = useState<Omit<ProductType, "product_id">>({
    product_name: "",
    product_description: "",
    product_price: 0,
    product_brand: "",
    product_quantity: 0,
    category: [],
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    let isCurrentRequest = true;
    const fetchProduct = async () => {
      if (id) {
        try {
          const response = await fetch(`http://127.0.0.1:8000/products/${id}`);
          const data = await response.json();
          if (isCurrentRequest) {
            const { product_id, product_category, ...rest } = data;
            setFormState({
              ...rest,
              category: product_category || [],
            });
          }
        } catch (error) {
          console.error("Error fetching product:", error);
        }
      }
    };
    fetchProduct();

    return () => {
      isCurrentRequest = false;
    };
  }, [id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormState((prev) => ({
      ...prev,
      [name]:
        name === "product_price" || name === "product_quantity"
          ? Number(value)
          : value,
    }));
  };

  const handleCategoryChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    index: number,
  ) => {
    const updatedCategories = [...formState.category];
    updatedCategories[index].category_name = e.target.value;
    setFormState((prev) => ({
      ...prev,
      category: updatedCategories,
    }));
  };

  const addCategory = () => {
    setFormState((prev) => ({
      ...prev,
      category: [
        ...prev.category,
        { category_id: "", category_name: "", category_description: "" },
      ],
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    const formattedProduct = {
      ...formState,
      product_category: formState.category.map((cat) => cat.category_name),
    };

    const method = id ? "PUT" : "POST";
    const url = id
      ? `http://127.0.0.1:8000/products/${id}`
      : `http://127.0.0.1:8000/products/`;

    try {
      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formattedProduct),
      });

      if (!response.ok) {
        const errorDetails = await response.json();
        console.error("Failed to save product", errorDetails);
        return;
      }

      navigate("/products");
    } catch (error) {
      console.error("Error during product save:", error);
    }
  };

  return (
    <form className="form_container" onSubmit={handleSubmit}>
      <h2 className="form-title">{id ? "Edit Product" : "Add New Product"}</h2>

      <div className="form-group">
        <label className="form-label">Name</label>
        <input
          className="form-field"
          type="text"
          name="product_name"
          value={formState.product_name || ""}
          onChange={handleChange}
          placeholder="Product Name"
          required={!id}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Description</label>
        <input
          className="form-field"
          type="text"
          name="product_description"
          value={formState.product_description || ""}
          onChange={handleChange}
          placeholder="Description"
          required={!id}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Price</label>
        <input
          className="form-field"
          type="number"
          name="product_price"
          value={formState.product_price || 0}
          onChange={handleChange}
          placeholder="Price"
          required={!id}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Brand</label>
        <input
          className="form-field"
          type="text"
          name="product_brand"
          value={formState.product_brand || ""}
          onChange={handleChange}
          placeholder="Brand"
          required={!id}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Quantity</label>
        <input
          className="form-field"
          type="number"
          name="product_quantity"
          value={formState.product_quantity || 0}
          onChange={handleChange}
          placeholder="Quantity"
          required={!id}
        />
      </div>

      <div className="category-section">
        <label className="form-label">Categories:</label>
        {formState.category.map((cat, idx) => (
          <input
            className="form-field"
            key={idx}
            type="text"
            value={cat.category_name || ""}
            onChange={(e) => handleCategoryChange(e, idx)}
            placeholder={`Category ${idx + 1}`}
          />
        ))}
        <button type="button" className="form-button" onClick={addCategory}>
          + Add Category
        </button>
      </div>

      <div className="form-actions">
        <button className="form-button" type="submit" disabled={isSubmitting}>
          {isSubmitting
            ? id
              ? "Updating..."
              : "Creating..."
            : id
              ? "Update"
              : "Create"}
        </button>
        <button
          className="form-button"
          type="button"
          onClick={() => navigate("/products")}
        >
          Cancel
        </button>
      </div>
    </form>
  );
};

export default ProductForm;
