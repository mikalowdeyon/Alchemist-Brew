document.addEventListener("DOMContentLoaded", () => {
  // 🌙 Theme toggle
  const themeToggle = document.getElementById("themeToggle");
  themeToggle.addEventListener("click", () => {
    const body = document.body;
    body.classList.toggle("dark");
    const dark = body.classList.contains("dark");
    themeToggle.textContent = dark ? "☀️" : "🌙";
    themeToggle.setAttribute("aria-pressed", dark);
  });

  // 📱 Mobile nav toggle
  const mobileToggle = document.getElementById("mobileToggle");
  const nav = document.getElementById("mainNav");
  mobileToggle.addEventListener("click", () => {
    nav.classList.toggle("active");
    const expanded = nav.classList.contains("active");
    mobileToggle.setAttribute("aria-expanded", expanded);
  });

  // 🪄 Magical particles
  const canvas = document.getElementById("particleCanvas");
  const ctx = canvas.getContext("2d");
  let particles = [];

  const resize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };
  window.addEventListener("resize", resize);
  resize();

  for (let i = 0; i < 70; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 2 + 1,
      color: `hsl(${Math.random() * 360}, 70%, 80%)`,
      speedY: Math.random() * 0.5 + 0.2
    });
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, 2 * Math.PI);
      ctx.fillStyle = p.color;
      ctx.fill();
      p.y += p.speedY;
      if (p.y > canvas.height) p.y = 0;
    });
    requestAnimationFrame(animate);
  }
  animate();

  // 🪞 Hero Carousel (auto-rotating)
  const heroSlides = document.querySelectorAll(".hero-slide");
  const heroDots = document.getElementById("heroDots");
  let heroIndex = 0;

  heroSlides.forEach((_, i) => {
    const dot = document.createElement("button");
    dot.classList.add("dot");
    dot.setAttribute("aria-label", `Slide ${i + 1}`);
    dot.addEventListener("click", () => showHeroSlide(i));
    heroDots.appendChild(dot);
  });

  function showHeroSlide(index) {
    heroSlides.forEach((slide, i) => {
      slide.classList.toggle("active", i === index);
      heroDots.children[i].classList.toggle("active", i === index);
    });
    heroIndex = index;
  }

  function nextHeroSlide() {
    heroIndex = (heroIndex + 1) % heroSlides.length;
    showHeroSlide(heroIndex);
  }

  showHeroSlide(heroIndex);
  setInterval(nextHeroSlide, 6000);

  // 🧁 Best Sellers (auto-rotating, no arrows)
  const bestFrames = document.querySelectorAll(".best-frame");
  const bestDots = document.getElementById("bestDots");
  let bestIndex = 0;

  bestFrames.forEach((_, i) => {
    const dot = document.createElement("button");
    dot.classList.add("dot");
    dot.setAttribute("aria-label", `Best Seller ${i + 1}`);
    dot.addEventListener("click", () => showBestFrame(i));
    bestDots.appendChild(dot);
  });

  function showBestFrame(index) {
    bestFrames.forEach((frame, i) => {
      frame.classList.toggle("active", i === index);
      bestDots.children[i].classList.toggle("active", i === index);
    });
    bestIndex = index;
  }

  function nextBestFrame() {
    bestIndex = (bestIndex + 1) % bestFrames.length;
    showBestFrame(bestIndex);
  }

  showBestFrame(bestIndex);
  setInterval(nextBestFrame, 7000);
});

// Carousel rotation
const slides = document.querySelectorAll('.hero-slide');
const dotsContainer = document.getElementById('heroDots');
slides.forEach((_, i) => {
  const dot = document.createElement('button');
  dot.className = 'carousel-dot';
  dot.setAttribute('aria-label', `Slide ${i+1}`);
  dotsContainer.appendChild(dot);
});
const dots = dotsContainer.querySelectorAll('button');

let index = 0;
function showSlide(i) {
  slides.forEach((s, n) => {
    s.classList.toggle('active', n === i);
    s.setAttribute('aria-hidden', n !== i);
    dots[n].classList.toggle('active', n === i);
  });
}
dots.forEach((d, i) => d.addEventListener('click', () => showSlide(i)));
setInterval(() => {
  index = (index + 1) % slides.length;
  showSlide(index);
}, 5000);

// Theme toggle
const themeToggle = document.getElementById('themeToggle');
themeToggle?.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  themeToggle.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙';
});

// Mobile nav toggle
const mobileToggle = document.getElementById('mobileToggle');
const nav = document.getElementById('mainNav');
mobileToggle?.addEventListener('click', () => {
  nav.classList.toggle('open');
  mobileToggle.setAttribute('aria-expanded', nav.classList.contains('open'));
});
