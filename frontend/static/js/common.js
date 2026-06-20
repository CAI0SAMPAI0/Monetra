let BACKEND_URL = '';

async function loadConfig() {
    try {
        const response = await fetch('config.json');
        if (response.ok) {
            const config = await response.json();
            if (config && config.BACKEND_URL) {
                return config.BACKEND_URL;
            }
        }
    } catch (e) {
        // config.json not found
    }
    return '';
}

function showToast(text, type = 'success') {
    let background = '#2EC47D';
    if (type === 'error') background = '#EF3823';
    else if (type === 'info') background = '#667eea';

    if (window.Toastify) {
        Toastify({
            text: text,
            duration: 4000,
            close: true,
            gravity: "top",
            position: "right",
            style: {
                background: background,
                color: "#white",
                fontWeight: "bold"
            }
        }).showToast();
    } else {
        alert(text);
    }
}

async function checkAuthAndSetup(isProtectedRoute = false) {
    if (!BACKEND_URL) {
        // Try to load config.json first
        let url = await loadConfig();
        if (!url) {
            // Check global config object
            if (window.MONETRA_CONFIG && window.MONETRA_CONFIG.BACKEND_URL) {
                url = window.MONETRA_CONFIG.BACKEND_URL;
            } else {
                // Check localStorage
                url = localStorage.getItem('BACKEND_URL') || '';
            }
        }
        if (!url) {
            // Default to localhost if applicable
            url = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.hostname === '5500' || window.location.port === '8000' || window.location.port === '5500'
                ? 'http://127.0.0.1:8000'
                : '';
        }

        if (url) {
            BACKEND_URL = url.trim().replace(/\/$/, "");
        } else {
            // Prompt the user for the backend URL if not set
            const userUrl = prompt("Por favor, configure a URL do seu backend do Monetra no Hugging Face (ex: https://caiosampaio-monetra.hf.space):");
            if (userUrl) {
                BACKEND_URL = userUrl.trim().replace(/\/$/, "");
                localStorage.setItem('BACKEND_URL', BACKEND_URL);
                window.location.reload();
                return null;
            } else {
                showToast("A URL do backend é obrigatória para o funcionamento da plataforma.", "error");
                return null;
            }
        }
    }

    try {
        const response = await fetch(`${BACKEND_URL}/api/auth/status/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            // Include credentials (cookies) for cross-domain requests
            credentials: 'include'
        });

        const data = await response.json();

        if (data.authenticated) {
            if (!isProtectedRoute && (window.location.pathname.endsWith('login.html') || window.location.pathname.endsWith('signup.html'))) {
                window.location.href = 'dashboard.html';
                return;
            }
            renderNavbar(true, data.user.email);
            renderFooter();
            return data.user;
        } else {
            if (isProtectedRoute) {
                window.location.href = 'login.html';
                return null;
            }
            renderNavbar(false);
            renderFooter();
            return null;
        }
    } catch (error) {
        console.error('Erro ao verificar status de autenticação:', error);
        if (isProtectedRoute) {
            showToast('Erro de conexão com o servidor. Faça o login.', 'error');
            setTimeout(() => { window.location.href = 'login.html'; }, 2000);
        } else {
            renderNavbar(false);
            renderFooter();
        }
        return null;
    }
}

// Fetch CSRF Token from Backend
async function fetchCSRFToken() {
    try {
        const res = await fetch(`${BACKEND_URL}/api/auth/csrf/`, { credentials: 'include' });
        const data = await res.json();
        return data.csrfToken;
    } catch (e) {
        console.error('Falha ao buscar token CSRF:', e);
        return '';
    }
}

// Render dynamic HTML Navbar
function renderNavbar(authenticated, email = '') {
    const placeholder = document.getElementById('navbar-placeholder');
    if (!placeholder) return;

    let menuItems = '';
    if (authenticated) {
        menuItems = `
            <a href="dashboard.html" class="text-text-secondary hover:text-text-primary transition-colors duration-200">Dashboard</a>
            <a href="chat.html" class="text-accent-500 font-bold hover:text-accent-600 transition-colors duration-200">MonetraBot (IA)</a>
            <a href="accounts.html" class="text-text-secondary hover:text-text-primary transition-colors duration-200">Contas</a>
            <a href="categories.html" class="text-text-secondary hover:text-text-primary transition-colors duration-200">Categorias</a>
            <a href="transactions.html" class="text-text-secondary hover:text-text-primary transition-colors duration-200">Transações</a>
            <div class="h-6 w-px bg-bg-tertiary"></div>
            <a href="profile.html" class="text-text-secondary hover:text-text-primary transition-colors duration-200">Perfil</a>
            <button id="config-api-btn" class="text-text-secondary hover:text-text-primary transition-colors duration-200 text-sm">Configuração</button>
            <button id="logout-btn" class="px-4 py-2 bg-error/10 text-error rounded-lg text-sm font-medium hover:bg-error hover:text-white transition-all duration-200 border border-error/20">
                Sair
            </button>
        `;
    } else {
        menuItems = `
            <a href="login.html" class="text-text-secondary hover:text-text-primary transition-colors duration-200">Login</a>
            <button id="config-api-btn" class="text-text-secondary hover:text-text-primary transition-colors duration-200 text-sm">Configurar API</button>
            <a href="signup.html" class="px-6 py-2 bg-accent-500 text-[#080808] rounded-lg font-bold hover:bg-accent-600 transition-all duration-200 shadow-lg">
                Cadastrar
            </a>
        `;
    }

    placeholder.innerHTML = `
        <nav class="bg-bg-secondary border-b border-bg-tertiary shadow-lg sticky top-0 z-50">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex items-center justify-between h-16">
                    <div class="flex items-center">
                        <a href="index.html" class="flex items-center space-x-2 text-2xl font-bold text-accent-500 tracking-tight">
                            <img src="static/images/logo1.png" alt="Monetra" class="h-8 w-auto onerror-fallback">
                            <span>Monetra</span>
                        </a>
                    </div>
                    
                    <!-- Desktop Menu -->
                    <div class="hidden md:flex items-center space-x-6">
                        ${menuItems}
                    </div>

                    <!-- Mobile Menu Button -->
                    <div class="md:hidden flex items-center">
                        <button id="mobile-menu-button" class="text-text-secondary hover:text-text-primary focus:outline-none">
                            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Mobile Menu -->
            <div id="mobile-menu" class="hidden md:hidden bg-bg-secondary border-t border-bg-tertiary px-4 pt-2 pb-4 space-y-2">
                ${authenticated ? `
                    <a href="dashboard.html" class="block px-4 py-2 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-colors">Dashboard</a>
                    <a href="chat.html" class="block px-4 py-2 text-accent-500 font-bold hover:bg-bg-tertiary rounded-lg transition-colors">MonetraBot (IA)</a>
                    <a href="accounts.html" class="block px-4 py-2 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-colors">Contas</a>
                    <a href="categories.html" class="block px-4 py-2 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-colors">Categorias</a>
                    <a href="transactions.html" class="block px-4 py-2 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-colors">Transações</a>
                    <a href="profile.html" class="block px-4 py-2 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-colors">Perfil</a>
                    <button id="config-api-btn-mobile" class="w-full text-left block px-4 py-2 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-colors">Configurar API</button>
                    <button id="logout-btn-mobile" class="w-full text-left px-4 py-2 text-error hover:bg-error hover:text-white rounded-lg transition-colors">
                        Sair
                    </button>
                ` : `
                    <a href="login.html" class="block px-4 py-2 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg">Login</a>
                    <button id="config-api-btn-mobile" class="w-full text-left block px-4 py-2 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-colors">Configurar API</button>
                    <a href="signup.html" class="block px-4 py-2 text-center bg-accent-500 text-[#080808] rounded-lg font-bold hover:bg-accent-600 transition-all">
                        Cadastrar
                    </a>
                `}
            </div>
        </nav>
    `;

    // Handle Image Error fallback if logo not found
    const logoImg = placeholder.querySelector('.onerror-fallback');
    if (logoImg) {
        logoImg.onerror = function() {
            this.style.display = 'none';
        };
    }

    // Set up Mobile menu toggle
    const mobileBtn = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileBtn && mobileMenu) {
        mobileBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Set up Config API handlers
    const configBtn = document.getElementById('config-api-btn');
    const configBtnMobile = document.getElementById('config-api-btn-mobile');
    const handleConfig = () => {
        const currentUrl = localStorage.getItem('BACKEND_URL') || '';
        const userUrl = prompt("Configure a URL do seu backend do Monetra (ex: https://caiosampaio-monetra.hf.space):", currentUrl);
        if (userUrl !== null) {
            const cleanedUrl = userUrl.trim().replace(/\/$/, "");
            if (cleanedUrl) {
                localStorage.setItem('BACKEND_URL', cleanedUrl);
                showToast("URL da API atualizada com sucesso!");
                setTimeout(() => { window.location.reload(); }, 1000);
            } else {
                localStorage.removeItem('BACKEND_URL');
                showToast("Configuração customizada removida.");
                setTimeout(() => { window.location.reload(); }, 1000);
            }
        }
    };
    if (configBtn) configBtn.addEventListener('click', handleConfig);
    if (configBtnMobile) configBtnMobile.addEventListener('click', handleConfig);

    // Set up Logout handlers
    const logoutBtn = document.getElementById('logout-btn');
    const logoutBtnMobile = document.getElementById('logout-btn-mobile');
    const handleLogout = async () => {
        try {
            const csrfToken = await fetchCSRFToken();
            const res = await fetch(`${BACKEND_URL}/api/auth/logout/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                credentials: 'include'
            });
            if (res.ok) {
                showToast('Logout realizado com sucesso!');
                setTimeout(() => { window.location.href = 'index.html'; }, 1000);
            }
        } catch (e) {
            console.error('Logout error:', e);
            window.location.href = 'index.html';
        }
    };

    if (logoutBtn) logoutBtn.addEventListener('click', handleLogout);
    if (logoutBtnMobile) logoutBtnMobile.addEventListener('click', handleLogout);
}
}

// Render Footer HTML
function renderFooter() {
    const placeholder = document.getElementById('footer-placeholder');
    if (!placeholder) return;

    placeholder.innerHTML = `
        <footer class="bg-bg-secondary border-t border-bg-tertiary py-8 mt-auto">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-text-muted text-sm">
                <p>&copy; ${new Date().getFullYear()} Monetra - Todos os direitos reservados.</p>
            </div>
        </footer>
    `;
}
