import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "./Category.css";

type CategoryType = {
  category_name: string;
  category_description: string;
};

const CategoryForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formState, setFormState] = useState<CategoryType>({
    category_name: "",
    category_description: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    let isCurrentRequest = true;
    const fetchCategory = async () => {
      if (id) {
        try {
          const response = await fetch(`http://127.0.0.1:8000/category/${id}`);
          const data = await response.json();
          if (isCurrentRequest) {
            setFormState(data);
          }
        } catch (error) {
          console.error("Error fetching category:", error);
        }
      }
    };

    fetchCategory();
    return () => {
      isCurrentRequest = false;
    };
  }, [id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormState((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    const method = id ? "PUT" : "POST";
    const url = id
      ? `http://127.0.0.1:8000/category/${id}`
      : `http://127.0.0.1:8000/category/`;

    try {
      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formState),
      });

      if (!response.ok) {
        const errorDetails = await response.json();
        console.error("Failed to save category", errorDetails);
        return;
      }

      navigate("/category");
    } catch (error) {
      console.error("Error during category save:", error);
    }
  };

  return (
    <form className="form_container" onSubmit={handleSubmit}>
      <h2 className="form-title">
        {id ? "Edit Category" : "Add New Category"}
      </h2>

      <div className="form-group">
        <label className="form-label">Name</label>
        <input
          className="form-field"
          type="text"
          name="category_name"
          value={formState.category_name}
          onChange={handleChange}
          placeholder="Category Name"
          required
        />
      </div>

      <div className="form-group">
        <label className="form-label">Description</label>
        <input
          className="form-field"
          type="text"
          name="category_description"
          value={formState.category_description}
          onChange={handleChange}
          placeholder="Description"
        />
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
          onClick={() => navigate("/category")}
        >
          Cancel
        </button>
      </div>
    </form>
  );
};

export default CategoryForm;
