const drinkData = {
  'home-strawberry': {
    page: 'home',
    title: "The Rose Elixir",
    description: "A sweet, ruby-hued concoction of strawberries and ice, whipped into a delightful, frosty blend.",
    primaryColor: "#fce8f0",
    accentColor: "#e76f92",
    imagePath: "img/rose-elixir.jpg",
    glow: "radial-gradient(circle at 70% 50%, rgba(255, 182, 193, 0.6) 0%, transparent 70%)"
  },
  'home-matcha': {
    page: 'home',
    title: "The Jade Essence",
    description: "A vibrant, emerald-green potion crafted from the purest tea leaves.",
    primaryColor: "#EBF5E0",
    accentColor: "#6A8C3A",
    imagePath: "img/jade-essence.jpg",
    glow: "radial-gradient(circle at 70% 50%, rgba(144,238,144,0.6) 0%, transparent 70%)"
  },
  'home-coffee': {
    page: 'home',
    title: "The Midas Touch",
    description: "Coffee infused with rich caramel that turns every sip to gold.",
    primaryColor: "#F3E8DC",
    accentColor: "#964B00",
    imagePath: "img/midas-touch.jpg",
    glow: "radial-gradient(circle at 70% 50%, rgba(210,180,140,0.6) 0%, transparent 70%)"
  }
};

const pageBody = document.getElementById('page-body');
const heroTitle = document.getElementById('hero-title');
const heroDescription = document.getElementById('hero-description');
const heroDrinkImage = document.getElementById('hero-drink-image');
const previewLinks = document.querySelectorAll('.preview-link');
const navPageLinks = document.querySelectorAll('.nav-page-link');
const styleRoot = document.documentElement.style;

function updatePageState(pageKey) {
  const data = drinkData[pageKey];
  if (!data) return;

  styleRoot.setProperty('--primary-pink', data.primaryColor);
  styleRoot.setProperty('--secondary-pink', data.accentColor);
  pageBody.style.backgroundColor = data.primaryColor;
  heroTitle.textContent = data.title;
  heroDescription.textContent = data.description;
  heroDrinkImage.src = data.imagePath;
  document.querySelector('.hero-image-container').style.background = data.glow;

  previewLinks.forEach(link => {
    link.classList.remove('active');
    if (link.dataset.drink === pageKey.replace('home-', '')) link.classList.add('active');
  });
}

previewLinks.forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    updatePageState(`home-${link.dataset.drink}`);
  });
});

navPageLinks.forEach(link => {
  link.addEventListener('click', e => e.preventDefault());
});

const carouselTrack = document.getElementById('carousel-track');
let index = 0;

document.getElementById('next-arrow').addEventListener('click', () => {
  index++;
  if (index > carouselTrack.children.length - 3) index = 0;
  carouselTrack.style.transform = `translateX(-${index * 320}px)`;
});

document.getElementById('prev-arrow').addEventListener('click', () => {
  index--;
  if (index < 0) index = carouselTrack.children.length - 3;
  carouselTrack.style.transform = `translateX(-${index * 320}px)`;
});

window.onload = () => updatePageState('home-strawberry');
