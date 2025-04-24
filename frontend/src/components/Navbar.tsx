import React from "react";
import "./Header.css";
import { Outlet, Link } from "react-router-dom";
const NavBar: React.FC = () => {
  return (
    <nav className="nav-bar">
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/products">Product List</Link>
        </li>
        <li>
          <Link to="/Category">Catgory</Link>
        </li>
      </ul>
      <Outlet />
    </nav>
  );
};

export default NavBar;
