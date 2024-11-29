document.addEventListener("DOMContentLoaded", () => {







// Create the container for the soft pulse cursor and particle effect
const container = document.createElement('div');
container.classList.add('cursor-container');
document.body.appendChild(container);

// Track cursor position
let cursorX = 0, cursorY = 0;

// Create the pulsing cursor element
const pulseCursor = document.createElement('div');
pulseCursor.classList.add('pulse-cursor');
container.appendChild(pulseCursor);

// Function to update the cursor position
function updateCursorPosition(x, y) {
    pulseCursor.style.left = `${x - pulseCursor.offsetWidth / 2}px`;
    pulseCursor.style.top = `${y - pulseCursor.offsetHeight / 2}px`;
}

// Function to create calming particles
function createCalmingParticles(x, y) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    particle.style.left = `${x - 5}px`;
    particle.style.top = `${y - 5}px`;
    container.appendChild(particle);

    // Particle Animation: Floating upwards slowly
    setTimeout(() => {
        particle.style.animation = 'floatUp 3s ease-in-out forwards';
    }, 0);

    // Fade out and disappear after animation
    setTimeout(() => {
        particle.remove();
    }, 3000); // Particle fades out after 3 seconds
}

// Handle cursor movement and trigger effects
document.addEventListener('mousemove', (e) => {
    cursorX = e.clientX;
    cursorY = e.clientY;

    // Update cursor position
    updateCursorPosition(cursorX, cursorY);

    // Create calming particles at the cursor position
    createCalmingParticles(cursorX, cursorY);
});






    // ===================== Scroll-to-top Button =====================
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.classList.add('scroll-top-btn');
    scrollTopBtn.innerHTML = '↑';
    document.body.appendChild(scrollTopBtn);

    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    window.addEventListener('scroll', () => {
        const showButton = document.documentElement.scrollTop > 200;
        scrollTopBtn.classList.toggle('show', showButton);
    });

    // ===================== Hero Section Animations =====================
    const heroText = document.querySelector('.hero h1');
    const heroParagraph = document.querySelector('.hero p');

    setTimeout(() => {
        heroText.classList.add('text-slide-in');
        heroParagraph.classList.add('text-fade-in');
    }, 500);

    // ===================== Section Cards Animation on Scroll =====================
    const sectionCards = document.querySelectorAll('.section-card');
    sectionCards.forEach(card => card.classList.add('animate-on-scroll'));

    const animateOnScroll = () => {
        sectionCards.forEach(card => {
            const isVisible = card.getBoundingClientRect().top < window.innerHeight;
            card.classList.toggle('fade-in', isVisible);
        });
    };
    window.addEventListener('scroll', animateOnScroll);

    // ===================== Handle Login State =====================
    const signUpBtn = document.getElementById('signUpBtn');
    const signInBtn = document.getElementById('signInBtn');
    const dashboardBtn = document.getElementById('dashboardBtn');
    const profileBtn = document.getElementById('profileBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    const loggedInState = JSON.parse(document.getElementById('loggedInState').textContent);

    const updateUI = (loggedIn) => {
        signUpBtn.style.display = loggedIn ? 'none' : 'inline-block';
        signInBtn.style.display = loggedIn ? 'none' : 'inline-block';
        dashboardBtn.style.display = loggedIn ? 'inline-block' : 'none';
        profileBtn.style.display = loggedIn ? 'inline-block' : 'none';
        logoutBtn.style.display = loggedIn ? 'inline-block' : 'none';
    };

    updateUI(loggedInState);

    logoutBtn.addEventListener('click', () => {
        fetch('/logout', { method: 'POST', credentials: 'include' })
            .then(response => {
                if (response.ok) updateUI(false);
            });
    });

    signInBtn.addEventListener('click', () => {
        fetch('/login', { method: 'POST', credentials: 'include' })
            .then(response => {
                if (response.ok) updateUI(true);
            });
    });

    // ===================== Service Cards Click Event =====================
    const services = {
        wellbeing: { id: "wellbeingService", url: "wellbeing.html" },
        talkToBushra: { id: "talkToBushraService", url: "chatbot.html" },
        guidedExercise: { id: "guidedExerciseService", url: "exercise.html" },
        relaxationMusic: { id: "relaxationMusicService", url: "music.html" },
        guidedMeditation: { id: "guidedMeditationService", url: "meditation.html" },
        selfJournaling: { id: "selfJournalingService", url: "journaling.html" }
    };

    const showLoginPrompt = () => {
        window.scrollTo({ top: 0, behavior: "smooth" });

        const message = document.createElement("div");
        message.classList.add("login-prompt");
        message.textContent = "You must log in to access this feature.";
        document.body.prepend(message);

        setTimeout(() => message.remove(), 3000);
    };

    Object.values(services).forEach(service => {
        const serviceCard = document.getElementById(service.id);
        serviceCard.addEventListener("click", () => {
            if (loggedInState) {
                window.location.href = service.url;
            } else {
                showLoginPrompt();
            }
        });
    });
});
