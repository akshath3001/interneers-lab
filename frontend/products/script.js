let currentPage = 1;
const pageSize = 3;
const baseUrl = "http://127.0.0.1:8000/products/";

const container = document.getElementById("product-container");
const pageNumber = document.getElementById("page-number");
const prevBtn = document.getElementById("prev-btn");
const nextBtn = document.getElementById("next-btn");
const reloadBtn = document.getElementById("reload-btn");
let numPages;

function urlConstructor(page) {
  return `${baseUrl}?page=${page}&page_size=${pageSize}`;
}

async function fetchProductsData(page) {
  const productsData = await fetch(urlConstructor(page));
  console.log(productsData);
  return productsData.json();
}

async function updateProductsPage(products, page) {
  const data = products.product;
  numPages = products.num_pages;
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
  nextBtn.disabled = currentPage + 1 <= numPages ? false : true;
}

async function fetchProducts(page) {
  try {
    const products = await fetchProductsData(page);
    await updateProductsPage(products, page);
  } catch (error) {
    currentPage = page;
    container.innerHTML = "<p>Error loading products.</p>";
    reloadBtn.style.display = "inline-block";
    pageNumber.textContent = `Page ${currentPage}`;
    console.error("Error fetching current page data:", error);
    nextBtn.disabled = true;
  }
}

prevBtn.addEventListener("click", () => {
  reloadBtn.style.display = "none";
  if (currentPage > 1) {
    fetchProducts(currentPage - 1);
  }
});

nextBtn.addEventListener("click", () => {
  reloadBtn.style.display = "none";
  fetchProducts(currentPage + 1);
});

reloadBtn.addEventListener("click", () => {
  reloadBtn.style.display = "none";
  fetchProducts(currentPage);
});

fetchProducts(currentPage);
