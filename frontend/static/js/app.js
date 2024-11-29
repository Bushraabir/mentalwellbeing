// Wait for the DOM to be fully loaded before executing scripts
document.addEventListener("DOMContentLoaded", () => {
  
    // 1. Custom Cursor
    const cursor = document.createElement('div');
    cursor.classList.add('cursor');
    document.body.appendChild(cursor);

    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.pageX + 'px';
        cursor.style.top = e.pageY + 'px';
    });

    const cursorElements = document.querySelectorAll('a, .cta-btn, .nav-link, .service-card, .testimonial-card');
    cursorElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            cursor.classList.add('hovered');
        });
        element.addEventListener('mouseleave', () => {
            cursor.classList.remove('hovered');
        });
    });

    // 2. Scroll-triggered Animations
    const elementsToAnimate = document.querySelectorAll('.animate-on-scroll');

    const scrollAnimation = () => {
        elementsToAnimate.forEach(el => {
            const elementPosition = el.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.5;

            if (elementPosition < screenPosition) {
                el.classList.add('fade-in');
            } else {
                el.classList.remove('fade-in');
            }
        });
    };

    window.addEventListener('scroll', scrollAnimation);
    scrollAnimation(); // Run on load for elements already in view

    // 3. Particle Background Animation (Basic Implementation)
    const particles = document.querySelector('.particles');
    let particleArray = [];
    const numberOfParticles = 50;

    function createParticle(e) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        particles.appendChild(particle);
        
        let x = e.clientX;
        let y = e.clientY;
        
        let particleStyle = {
            position: 'absolute',
            left: `${x}px`,
            top: `${y}px`,
            backgroundColor: 'var(--highlight-color)',
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            opacity: 1,
            animation: 'particleAnimation 1s ease-out forwards'
        };

        for (let prop in particleStyle) {
            particle.style[prop] = particleStyle[prop];
        }

        setTimeout(() => {
            particle.remove();
        }, 1000);
    }

    window.addEventListener('mousemove', (e) => {
        createParticle(e);
    });

    // 4. Smooth Scroll Effect
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            document.getElementById(targetId).scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    });

    // 5. Sticky Navbar Effect
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;

    window.addEventListener('scroll', () => {
        let scrollTop = window.scrollY;

        if (scrollTop > lastScrollTop) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }

        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });

    // 6. Service Card Hover Animations
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('hovered');
        });
        card.addEventListener('mouseleave', () => {
            card.classList.remove('hovered');
        });
    });

    // 7. Text Animation in Hero Section
    const heroText = document.querySelector('.hero h1');
    const heroParagraph = document.querySelector('.hero p');

    setTimeout(() => {
        heroText.classList.add('text-slide-in');
        heroParagraph.classList.add('text-fade-in');
    }, 500);

    // 8. Scroll-to-top Button
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.classList.add('scroll-top-btn');
    scrollTopBtn.innerHTML = '↑';
    document.body.appendChild(scrollTopBtn);

    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    window.addEventListener('scroll', () => {
        if (document.documentElement.scrollTop > 200) {
            scrollTopBtn.classList.add('show');
        } else {
            scrollTopBtn.classList.remove('show');
        }
    });

});

// CSS for additional JS functionality
const style = document.createElement('style');
style.innerHTML = `
    /* Custom Cursor */
    .cursor {
        position: absolute;
        border: 3px solid var(--highlight-color);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        pointer-events: none;
        transition: width 0.3s, height 0.3s, transform 0.3s;
    }
    .cursor.hovered {
        width: 50px;
        height: 50px;
        transform: scale(1.5);
    }

    /* Particle Animation */
    .particle {
        position: absolute;
        background-color: var(--highlight-color);
        border-radius: 50%;
        opacity: 0;
        animation: particleAnimation 1s ease-out forwards;
    }

    @keyframes particleAnimation {
        0% {
            transform: scale(1);
            opacity: 1;
        }
        100% {
            transform: scale(3);
            opacity: 0;
        }
    }

    /* Scroll Animations */
    .animate-on-scroll {
        opacity: 0;
        transform: translateY(50px);
        transition: opacity 0.5s, transform 0.5s;
    }

    .fade-in {
        opacity: 1;
        transform: translateY(0);
    }

    /* Navbar Sticky Effect */
    .navbar-scrolled {
        background-color: var(--dark-green);
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
    }

    /* Scroll-to-top Button */
    .scroll-top-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        padding: 10px 15px;
        background-color: var(--highlight-color);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 1.5rem;
        cursor: pointer;
        transition: transform 0.3s;
        opacity: 0;
        visibility: hidden;
    }

    .scroll-top-btn.show {
        opacity: 1;
        visibility: visible;
        transform: scale(1.2);
    }

    .scroll-top-btn:hover {
        transform: scale(1.5);
    }

    /* Hero Section Text Animations */
    .text-slide-in {
        animation: slideIn 1s ease-out;
    }

    .text-fade-in {
        animation: fadeIn 1.5s ease-out;
    }

    @keyframes slideIn {
        0% {
            transform: translateY(-50px);
            opacity: 0;
        }
        100% {
            transform: translateY(0);
            opacity: 1;
        }
    }

    @keyframes fadeIn {
        0% {
            opacity: 0;
        }
        100% {
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
