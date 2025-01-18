/* wdd131/recipes/scr/html.mjs - Module for Unit 5's Recipe Book */

const tags = function(tags) {
  return tags.map(tag => `<div class="tag">${tag}</div>`).join("");
}

const stars = function(rating) {
  const stars = [];
  for (let i = 1; i <= 5; i++) {
    const star = {};
    if (i <= rating) {
      star.class = "icon-star";
      star.symbol = "⭐";
    }
    else {
      star.class = "icon-star-empty";
      star.symbol = "☆";
    }
    stars.push(star);
  }
  return stars.map(star => `
    <span aria-hidden="true" class="${star.class}">${star.symbol}</span>
  `).join("");
}

const html = function(recipe) {
  return `<section class="recipe">
    <div class="picture"><img alt="${recipe.name}" src="${recipe.image}"></div>
    <div class="text">
      <div class="tags">${tags(recipe.tags)}</div>
      <h2 class="label">${recipe.name}</h2>
      <span
        class="rating"
        role="img"
        aria-label="Rating: ${recipe.rating} out of 5 stars"
      >${stars(recipe.rating)}</span>
      <p class="description">${recipe.description}</p>
    </div>
  </section>`;
}

export default html;