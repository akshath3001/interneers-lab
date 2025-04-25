import React from "react";
import "./App.css";
import Header from "components/Header";
import ProductList from "components/ProductList";
import { Route, Routes } from "react-router-dom";
import Home from "components/Home";
import Category from "components/Category";
import ProductForm from "components/ProductForm";

const App: React.FC = () => {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/">
          <Route index element={<Home />} />
          <Route path="/products" element={<ProductList />} />
          <Route path="/productform" element={<ProductForm />} />
          <Route path="/productform/:id" element={<ProductForm />} />
          <Route path="/category" element={<Category />} />
        </Route>
      </Routes>
    </>
  );
};
export default App;
