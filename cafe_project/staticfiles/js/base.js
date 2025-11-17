        const drinkData = {
            'home-strawberry': {
                page: 'home',
                title: "The Rose Elixir",
                description: "A sweet, ruby-hued concoction of strawberries and ice, whipped into a delightful, frosty blend. It's a charm to lift your spirits and enchant your senses.",
                primaryColor: "#fce8f0", 
                accentColor: "#e76f92",  
                imagePath: "path/to/large-strawberry-drink.png",
                orderBtnText: "Order Now",
                glow: "radial-gradient(circle at 70% 50%, rgba(255, 182, 193, 0.6) 0%, transparent 70%)"
            },
            'home-matcha': {
                page: 'home',
                title: "The Jade Essence",
                description: "A vibrant, emerald-green potion crafted from the purest, finely ground tea leaves. This earthy and revitalizing brew awakens the mind and nourishes the soul.",
                primaryColor: "#EBF5E0", 
                accentColor: "#6A8C3A",  
                imagePath: "path/to/large-matcha-drink.png",
                orderBtnText: "Order Now",
                glow: "radial-gradient(circle at 70% 50%, rgba(144, 238, 144, 0.6) 0%, transparent 70%)"
            },
            'home-coffee': {
                page: 'home',
                title: "The Midas Touch",
                description: "A truly magical concoction. This coffee is infused with a caramel so rich and luxurious, it feels as though everything it touches has been turned to gold.",
                primaryColor: "#F3E8DC", 
                accentColor: "#964B00",  
                imagePath: "path/to/large-coffee-drink.png",
                orderBtnText: "Order Now",
                glow: "radial-gradient(circle at 70% 50%, rgba(210, 180, 140, 0.6) 0%, transparent 70%)"
            },
            
            'menu': {
                page: 'alt',
                title: "Our Full Grimoire of Brews",
                text: "Explore all our enchanting elixirs, potions, and spell-binding coffee blends. Ready to order?",
                primaryColor: "#E0F7FA", 
                accentColor: "#00BCD4",  
            },
            'study-room': {
                page: 'alt',
                title: "The Alchemist's Study Room",
                text: "A quiet haven for deep contemplation and focused work. Find your nearest location and book a seat.",
                primaryColor: "#FBEFE8", 
                accentColor: "#FF9800",  
            },
            'contact-us': {
                page: 'alt',
                title: "Contact the Apothecary",
                text: "Have a query about your brew or need support? Send us a message!",
                primaryColor: "#F3E5F5", 
                accentColor: "#9C27B0",  
            },
            'cart': {
                page: 'alt',
                title: "Your Inventory",
                text: "Review the items you've gathered for your order.",
                primaryColor: "#E8F5E9", 
                accentColor: "#4CAF50",  
            },
            'profile': {
                page: 'alt',
                title: "The Apprentice Profile",
                text: "Manage your account, view past orders, and update your magical settings.",
                primaryColor: "#F8F8F8", 
                accentColor: "#757575",  
            }
        };

        // --- DOM ELEMENTS ---
        const pageBody = document.getElementById('page-body');
        const heroSection = document.getElementById('hero-section'); 
        const heroContent = document.querySelector('.hero-content');
        const heroImageContainer = document.getElementById('hero-image-container');
        const altContent = document.getElementById('alt-content');
        const previewLinks = document.querySelectorAll('.preview-link');
        const navPageLinks = document.querySelectorAll('.nav-page-link');
        const navItems = document.querySelectorAll('.nav-item');
        const styleRoot = document.documentElement.style;
        
        // Home page elements
        const heroTitle = document.getElementById('hero-title');
        const heroDescription = document.getElementById('hero-description');
        const primaryBtn = document.getElementById('primary-btn');
        const heroDrinkImage = document.getElementById('hero-drink-image');
        const viewMenuBtn = document.getElementById('view-menu-btn');
        
        // Carousel elements
        const menuPreviewSection = document.getElementById('menu-preview-section');
        const carouselTrack = document.getElementById('carousel-track');
        const prevArrow = document.getElementById('prev-arrow');
        const nextArrow = document.getElementById('next-arrow');
        // Select only the original (non-cloned) drink cards for counting
        const originalDrinkCards = document.querySelectorAll('.drink-card:not(.clone)'); 
        
        let currentCarouselIndex = 0; // Tracks the index of the first visible card
        const CARDS_PER_VIEW = 3; // The number of visible cards in the desktop view
        const NUM_ORIGINAL_CARDS = originalDrinkCards.length; // 5

        // --- CAROUSEL LOGIC (UPDATED FOR INFINITE LOOP) ---
        
        /**
         * Calculates the width of a single card plus its margin/gap.
         * @returns {number} The total width in pixels for one card increment.
         */
        function getCardWidth() {
            if (originalDrinkCards.length === 0) return 0;
            const card = originalDrinkCards[0];
            const computedStyle = window.getComputedStyle(card);
            const width = card.offsetWidth;
            const gap = parseFloat(window.getComputedStyle(carouselTrack).gap) || 20;
            
            return width + gap; 
        }

        /**
         * Scrolls the carousel track by a certain number of card positions, implementing a loop.
         * @param {number} direction - 1 for next, -1 for previous.
         */
        function scrollDrinks(direction) {
            const cardWidth = getCardWidth();
            
            // 1. Calculate the target index
            let newIndex = currentCarouselIndex + direction;
            
            // 2. Check for the reset condition (End of Loop)
            // If we move to the right (direction=1) and we land on the first clone (index 5)
            if (newIndex >= NUM_ORIGINAL_CARDS) {
                // First, scroll to the clone (to make it look seamless)
                currentCarouselIndex = newIndex;
                let translateDistance = -currentCarouselIndex * cardWidth;
                carouselTrack.style.transform = `translateX(${translateDistance}px)`;
                
                // Then, instantly jump back to the start (index 0) after the animation finishes
                setTimeout(() => {
                    carouselTrack.style.transition = 'none'; // Disable transition for instant jump
                    currentCarouselIndex = 0;
                    translateDistance = 0;
                    carouselTrack.style.transform = `translateX(${translateDistance}px)`;
                    
                    // Re-enable transition for next scroll
                    setTimeout(() => {
                        carouselTrack.style.transition = 'transform 0.5s cubic-bezier(0.25, 0.1, 0.25, 1)';
                    }, 50); // A very small delay to ensure transition property is removed before next scroll
                }, 500); // Must match the CSS transition duration (0.5s)
                return;
            }
            
            // 3. Check for the reset condition (Start of Loop)
            // If we move to the left (direction=-1) and are moving from the first card
            if (newIndex < 0) {
                // First, jump instantly to the 'cloned' end position (index = 5)
                carouselTrack.style.transition = 'none'; // Disable transition for instant jump
                currentCarouselIndex = NUM_ORIGINAL_CARDS; 
                let translateDistance = -currentCarouselIndex * cardWidth;
                carouselTrack.style.transform = `translateX(${translateDistance}px)`;
                
                // Then, enable transition and scroll to the second-to-last card (index 4)
                setTimeout(() => {
                    carouselTrack.style.transition = 'transform 0.5s cubic-bezier(0.25, 0.1, 0.25, 1)';
                    currentCarouselIndex = NUM_ORIGINAL_CARDS - 1; 
                    translateDistance = -currentCarouselIndex * cardWidth;
                    carouselTrack.style.transform = `translateX(${translateDistance}px)`;
                }, 50); // Small delay before applying the smooth scroll
                return;
            }
            
            // 4. Standard Scroll
            carouselTrack.style.transition = 'transform 0.5s cubic-bezier(0.25, 0.1, 0.25, 1)';
            currentCarouselIndex = newIndex;
            const translateDistance = -currentCarouselIndex * cardWidth;
            carouselTrack.style.transform = `translateX(${translateDistance}px)`;
        }
        
        // --- UI UPDATE FUNCTIONS ---

        /**
         * Updates the entire page state (content, colors, layout) based on the pageKey.
         * @param {string} pageKey - The key corresponding to the desired page state (e.g., 'home-strawberry', 'menu').
         */
        function updatePageState(pageKey) {
            const data = drinkData[pageKey];
            if (!data) return;

            // 1. Update Colors (CSS Variables and BODY Background)
            styleRoot.setProperty('--primary-pink', data.primaryColor);
            styleRoot.setProperty('--secondary-pink', data.accentColor);
            // Apply background directly to body for the entire page
            pageBody.style.backgroundColor = data.primaryColor;
            
            // 2. Manage Active Navigation Link (sets 'current' class on nav-item)
            navItems.forEach(item => item.classList.remove('current'));
            
            // Find the corresponding nav item to highlight.
            const navItemKey = pageKey.startsWith('home') ? 'home-strawberry' : pageKey;
            const navItemToHighlight = document.querySelector(`.nav-item[data-page="${navItemKey}"]`);
            if (navItemToHighlight) {
                navItemToHighlight.classList.add('current');
            }

            // 3. Switch between Home (Hero) content and Alternative content
            if (data.page === 'home') {
                // Show Home Content
                heroSection.style.display = 'flex'; 
                heroContent.style.display = 'flex';
                heroImageContainer.style.display = 'flex';
                altContent.style.display = 'none';
                menuPreviewSection.style.display = 'block'; // Show the new scrollable section

                // Home view updates (Drink Preview logic)
                heroTitle.textContent = data.title;
                heroDescription.textContent = data.description;
                heroDrinkImage.src = data.imagePath;
                primaryBtn.textContent = data.orderBtnText;
                heroImageContainer.style.background = data.glow;
                pageBody.dataset.activePage = pageKey;
                
                // Update active preview highlight
                const drinkName = pageKey.replace('home-', '');
                previewLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.dataset.drink === drinkName) {
                        link.classList.add('active');
                    }
                });
                
            } else {
                // Show Alternative Content
                heroSection.style.display = 'flex'; 
                heroContent.style.display = 'none';
                heroImageContainer.style.display = 'none';
                altContent.style.display = 'flex';
                menuPreviewSection.style.display = 'none'; // Hide the new scrollable section
                
                // Alt view updates
                document.getElementById('alt-title').textContent = data.title;
                document.getElementById('alt-text').textContent = data.text;
                pageBody.dataset.activePage = pageKey;
            }
        }

        // --- EVENT LISTENERS ---

        // 1. Navigation Links and Header Icons
        navPageLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault(); 
                const pageKey = link.dataset.page;
                updatePageState(pageKey);
            });
        });
        
        // 2. Drink Preview Clicks
        previewLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault(); 
                const drinkKey = link.dataset.drink;
                updatePageState(`home-${drinkKey}`);
            });
        });

        // 3. View Menu Button Click Handler
        if (viewMenuBtn) {
            viewMenuBtn.addEventListener('click', (e) => {
                e.preventDefault();
                updatePageState('menu'); 
            });
        }
        
        // 4. Handle Discover More button
        const discoverMoreBtn = document.querySelector('.discover-btn');
        if (discoverMoreBtn) {
            discoverMoreBtn.addEventListener('click', (e) => {
                e.preventDefault();
                updatePageState('menu'); 
            });
        }
        
        // 5. Carousel Arrow Clicks
        prevArrow.addEventListener('click', () => scrollDrinks(-1));
        nextArrow.addEventListener('click', () => scrollDrinks(1));

        // 6. Handle resizing to ensure the carousel position is correct
        window.addEventListener('resize', () => {
             // Reset the position when resizing to avoid awkward gaps, and always keep index 0
             carouselTrack.style.transition = 'none'; // Temporarily disable transition for instant reset
             currentCarouselIndex = 0; // Reset to the start of the original cards
            const translateDistance = 0;
            carouselTrack.style.transform = `translateX(${translateDistance}px)`;
            
             // Re-enable transition after a small delay
            setTimeout(() => {
                carouselTrack.style.transition = 'transform 0.5s cubic-bezier(0.25, 0.1, 0.25, 1)';
            }, 10);
        });

        // Initialize the page view on load
        window.onload = () => {
            updatePageState('home-strawberry');
        };