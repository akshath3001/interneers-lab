import React from "react";
import "./Category.css";

export interface CategoryType {
  category_id: string;
  category_name: string;
  category_description: string;
}

interface CategoryProps {
  category: CategoryType;
  onDelete: (e: React.MouseEvent) => void;
  onEdit: (e: React.MouseEvent) => void;
  onClick: () => void;
}

const Category: React.FC<CategoryProps> = ({
  category,
  onDelete,
  onEdit,
  onClick,
}) => {
  return (
    <div className="category-card" onClick={onClick}>
      <h3>{category.category_name}</h3>
      <div className="category-details">
        <span className="bold-text">Description: </span>
        {category.category_description}
      </div>
      <div className="category-actions">
        <button className="edit-btn" onClick={onEdit}>
          Edit
        </button>
        <button className="delete-btn" onClick={onDelete}>
          Delete
        </button>
      </div>
    </div>
  );
};

export default Category;
