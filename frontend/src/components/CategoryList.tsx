import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Category, { CategoryType } from "./Category";
import "./Category.css";

const CategoryList: React.FC = () => {
  const [categories, setCategories] = useState<CategoryType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const navigate = useNavigate();
  const baseUrl = "http://127.0.0.1:8000/";

  useEffect(() => {
    const fetchCategories = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(`${baseUrl}category/?page=${currentPage}`);
        if (!response.ok) throw new Error("Failed to fetch categories");
        const data = await response.json();
        setCategories(data.category);
        setTotalPages(data.num_pages);
      } catch (error) {
        console.error("Error fetching categories:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchCategories();
  }, [currentPage]);

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    try {
      const res = await fetch(`${baseUrl}category/${id}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Failed to delete category");
      setCategories((prev) => prev.filter((c) => c.category_id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  const handleEdit = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    navigate(`/categoryform/${id}`);
  };

  const handleClick = (id: string) => {
    navigate(`/categoryproducts/${id}`);
  };

  const handleAdd = () => {
    navigate("/categoryform");
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage((prev) => prev + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage((prev) => prev - 1);
    }
  };

  return (
    <div className="list-page">
      <h1>Category List</h1>
      <button className="add-btn" onClick={handleAdd}>
        Add New Category
      </button>
      {isLoading ? (
        <>
          <h2>Loading...</h2>
          <div className="spinner"></div>
        </>
      ) : (
        <>
          <div className="category-list">
            {categories.map((category) => (
              <Category
                key={category.category_id}
                category={category}
                onDelete={(e) => handleDelete(e, category.category_id)}
                onEdit={(e) => handleEdit(e, category.category_id)}
                onClick={() => handleClick(category.category_id)}
              />
            ))}
          </div>
          <div className="pagination">
            <button
              onClick={handlePrevPage}
              disabled={currentPage === 1}
              className="prev-btn"
            >
              Previous
            </button>
            <span>{`Page ${currentPage} of ${totalPages}`}</span>
            <button
              onClick={handleNextPage}
              disabled={currentPage === totalPages}
              className="next-btn"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default CategoryList;
