import React from "react";
import "./App.css";
import Header from "components/Header";
import ProductList from "components/ProductList";

const App: React.FC = () => {
  return (
    <>
      <Header />
      <div style={{ padding: 15 }}>
        <ProductList />
      </div>
    </>
  );
};
export default App;
