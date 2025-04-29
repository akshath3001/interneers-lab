import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Product, { ProductType } from "./Product";
import "./Product.css";

interface ProductListProps {
  categoryId?: string | null;
}
const ProductList: React.FC<ProductListProps> = () => {
  const { id } = useParams<{ id?: string }>();
  const categoryId = id ?? null;
  const [products, setProducts] = useState<ProductType[]>([]);
  const navigate = useNavigate();
  const baseUrl = "http://127.0.0.1:8000/";

  const [isLoading, setIsLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true);
      try {
        let url = categoryId
          ? `${baseUrl}category/${categoryId}?products=true&page=${currentPage}`
          : `${baseUrl}products/?page=${currentPage}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch products");
        const data = await response.json();
        if (categoryId) {
          setProducts(data.category_products ?? []);
          setTotalPages(data.num_pages ?? 1);
        } else {
          setProducts(data.product ?? []);
          setTotalPages(data.num_pages ?? 1);
        }
      } catch (error) {
        console.error("Error fetching products:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchProducts();
  }, [categoryId, currentPage]);

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
      <h1>{id ? "Category Product List" : "Product List"}</h1>
      <button className="add-btn" onClick={handleAdd}>
        Add New Product
      </button>
      {isLoading ? (
        <>
          <h2>Loading...</h2>
          <div className="spinner"></div>
        </>
      ) : (
        <>
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

export default ProductList;
