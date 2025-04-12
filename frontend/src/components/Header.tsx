import React from "react";
import NavBar from "./Navbar";
import "./Header.css";

const Header: React.FC = () => {
  return (
    <header className="app-header">
      <h1>Product Store</h1>
      <NavBar />
    </header>
  );
};

export default Header;
