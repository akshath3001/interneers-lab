let currentPage = 1;
const pageSize = 3;
const baseUrl = "http://127.0.0.1:8000/products/";

const container = document.getElementById("product-container");
const pageNumber = document.getElementById("page-number");
const prevBtn = document.getElementById("prev-btn");
const nextBtn = document.getElementById("next-btn");
let num_pages;

function url_constructor(page) {
  return `${baseUrl}?page=${page}&page_size=${pageSize}`;
}

async function fetch_products(page) {
  try {
    const response = await fetch(url_constructor(page));
    const products = await response.json();
    const data = products.product;
    num_pages = products.num_pages;
    console.log("Products fetched:", data);
    container.innerHTML = "";

    if (!data || data.length === 0) {
      container.innerHTML = "<p>No more products to display.</p>";
      pageNumber.textContent = `Page ${page}`;
      nextBtn.disabled = true;
      return;
    }

    data.forEach((product, index) => {
      const tile = document.createElement("div");
      tile.className = "product-tile";
      tile.style.animationDelay = `${index * 100}ms`;

      tile.innerHTML = `
        <div class="product-name">${product.product_name}</div>
        <div class="product-category">
          Categories: ${product.category.map((category) => category.category_name).join(", ")}
        </div>
        <div class="product-price">Price: Rs. ${product.product_price}</div>
        <div class="product-description">${product.product_description}</div>
        <div class="product-brand">Brand: ${product.product_brand}</div>
        <div class="product-quantity">Quantity(in stock): ${product.product_quantity}</div>
      `;
      container.appendChild(tile);
    });
    currentPage = page;
    pageNumber.textContent = `Page ${currentPage}`;
    prevBtn.disabled = currentPage <= 1;
    nextBtn.disabled = currentPage + 1 <= num_pages ? false : true;
  } catch (error) {
    console.error("Error fetching current page data:", error);
    container.innerHTML = "<p>Error loading products.</p>";
    pageNumber.textContent = `Page ${currentPage}`;
    nextBtn.disabled = true;
  }
}

prevBtn.addEventListener("click", () => {
  if (currentPage > 1) {
    fetch_products(currentPage - 1);
  }
});

nextBtn.addEventListener("click", () => {
  fetch_products(currentPage + 1);
});

fetch_products(currentPage);
