"""
FlyBuddy - Premium Real Glassmorphism Design System & Client-Side Interactive Layer
---------------------------------------------------------------------------------
Provides color tokens, atmospheric aviation gradients, real glassmorphism styling,
high-contrast inputs, distinct sidebar styling, clean Streamlit overrides,
and Streamlit-compatible client-side interactive background, parallax, cursor & trail.
"""

import streamlit as st
import streamlit.components.v1 as components

THEME = {
    'bg_deep': '#040912',
    'bg_surface': '#0A172B',
    'sidebar_bg': '#0B192C',
    'glass_card': 'rgba(12, 24, 46, 0.72)',
    'glass_floating': 'linear-gradient(145deg, rgba(14, 28, 52, 0.88) 0%, rgba(20, 38, 68, 0.72) 100%)',
    'primary_cyan': '#22D3EE',
    'secondary_violet': '#8B5CF6',
    'accent_blue': '#38BDF8',
    'text_primary': '#F8FAFC',
    'text_secondary': '#94A3B8',
    'text_muted': '#64748B',
    'border_subtle': 'rgba(255, 255, 255, 0.08)',
    'border_cyan': 'rgba(34, 211, 238, 0.3)',
    'success': '#34D399',
    'success_bg': 'rgba(52, 211, 153, 0.14)',
    'warning': '#FBBF24',
    'warning_bg': 'rgba(251, 191, 36, 0.14)',
    'card_radius': '20px',
    'card_shadow': '0 16px 40px rgba(0, 0, 0, 0.55)'
}

def apply_custom_theme():
    """
    Inject clean, real glassmorphism CSS, high-contrast inputs, distinct sidebar,
    and client-side interactive visual canvas (parallax, glowing cursor & trail).
    """
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* Global Dark Aviation Canvas */
    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: {THEME['bg_deep']} !important;
        background-image: 
            radial-gradient(circle at 14% 16%, rgba(34, 211, 238, 0.11) 0%, transparent 45%),
            radial-gradient(circle at 86% 84%, rgba(139, 92, 246, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(10, 23, 43, 0.55) 0%, transparent 100%) !important;
        background-attachment: fixed !important;
        color: {THEME['text_primary']} !important;
    }}

    /* Streamlit Chrome & Viewport Padding */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        height: 1.2rem !important;
        z-index: 10 !important;
    }}
    header[data-testid="stHeader"] [data-testid="stToolbar"] {{
        top: 0.2rem !important;
        right: 1rem !important;
    }}
    
    .main .block-container {{
        padding-top: 0.8rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 1.8rem !important;
        padding-right: 1.8rem !important;
        max-width: 1260px !important;
        position: relative !important;
        z-index: 2 !important;
    }}

    /* DISTINCT SIDEBAR SURFACE */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0B192C 0%, #050E1B 100%) !important;
        border-right: 1.5px solid rgba(34, 211, 238, 0.16) !important;
        box-shadow: 10px 0 35px rgba(0, 0, 0, 0.6) !important;
        z-index: 10 !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 1.25rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }}

    /* IMPROVED SIDEBAR BUTTONS */
    [data-testid="stSidebar"] div.stRadio > div {{
        gap: 8px !important;
    }}
    [data-testid="stSidebar"] div.stRadio > div > label {{
        background: rgba(15, 26, 46, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        padding: 10px 15px !important;
        border-radius: 14px !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        color: {THEME['text_secondary']} !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        cursor: pointer !important;
    }}
    [data-testid="stSidebar"] div.stRadio > div > label:hover {{
        background: rgba(34, 211, 238, 0.12) !important;
        color: {THEME['primary_cyan']} !important;
        border-color: rgba(34, 211, 238, 0.35) !important;
        transform: translateX(3px) !important;
        box-shadow: 0 4px 15px rgba(34, 211, 238, 0.1) !important;
    }}
    [data-testid="stSidebar"] div.stRadio > div > label:has(input:checked) {{
        background: linear-gradient(135deg, rgba(34, 211, 238, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%) !important;
        border: 1.5px solid rgba(34, 211, 238, 0.5) !important;
        color: #F8FAFC !important;
        font-weight: 700 !important;
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.25) !important;
    }}
    [data-testid="stSidebar"] div.stRadio > div > label > div:first-child {{
        display: none !important;
    }}

    /* HIGH-CONTRAST Form Controls (Light & Dark Mode Safe) */
    div[data-baseweb="select"] > div {{
        background-color: #0B1728 !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
    }}
    div[data-baseweb="select"] span {{
        color: #F8FAFC !important;
        font-weight: 500 !important;
    }}
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {{
        background-color: #0B1728 !important;
        border: 1px solid rgba(34, 211, 238, 0.3) !important;
        border-radius: 12px !important;
    }}
    li[data-baseweb="menu-item"] {{
        color: #F8FAFC !important;
        font-weight: 500 !important;
    }}
    li[data-baseweb="menu-item"]:hover {{
        background-color: rgba(34, 211, 238, 0.18) !important;
        color: #22D3EE !important;
    }}
    div[data-baseweb="input"] > div {{
        background-color: #0B1728 !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
    }}
    input {{
        color: #F8FAFC !important;
    }}
    label, [data-testid="stWidgetLabel"] p {{
        color: {THEME['text_secondary']} !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
    }}

    /* Real Glassmorphism Cards */
    .fb-glass-card {{
        background: {THEME['glass_card']};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {THEME['border_subtle']};
        border-top: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: {THEME['card_radius']};
        padding: 22px 26px;
        box-shadow: {THEME['card_shadow']};
        margin-bottom: 20px;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
        position: relative;
        z-index: 2;
    }}
    .fb-glass-card:hover {{
        border-color: rgba(34, 211, 238, 0.25);
        box-shadow: 0 16px 44px rgba(0, 0, 0, 0.55), 0 0 20px rgba(34, 211, 238, 0.08);
    }}

    /* Floating Flight Search Glass Card (Landing Right Column) */
    .fb-floating-card {{
        background: {THEME['glass_floating']};
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-top: 1px solid rgba(255, 255, 255, 0.24);
        border-radius: 24px;
        padding: 24px 26px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.65), 0 0 25px rgba(34, 211, 238, 0.08);
        position: relative;
        z-index: 2;
    }}

    /* KPI Metric Cards */
    .fb-kpi-card {{
        background: {THEME['glass_card']};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid {THEME['border_subtle']};
        border-top: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: {THEME['card_shadow']};
        height: 100%;
        transition: transform 0.2s ease, border-color 0.2s ease;
        position: relative;
        z-index: 2;
    }}
    .fb-kpi-card:hover {{
        border-color: rgba(34, 211, 238, 0.3);
        transform: translateY(-2px);
    }}
    .fb-kpi-label {{
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {THEME['text_secondary']};
        margin-bottom: 4px;
    }}
    .fb-kpi-value {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {THEME['text_primary']};
        line-height: 1.2;
    }}
    .fb-kpi-sub {{
        font-size: 0.82rem;
        color: {THEME['text_secondary']};
        margin-top: 4px;
    }}

    /* Badges */
    .fb-badge {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
    }}
    .fb-badge-good {{
        background-color: {THEME['success_bg']};
        color: {THEME['success']};
        border: 1px solid rgba(52, 211, 153, 0.3);
    }}
    .fb-badge-typical {{
        background-color: rgba(34, 211, 238, 0.12);
        color: {THEME['primary_cyan']};
        border: 1px solid rgba(34, 211, 238, 0.3);
    }}
    .fb-badge-violet {{
        background-color: rgba(139, 92, 246, 0.12);
        color: {THEME['secondary_violet']};
        border: 1px solid rgba(139, 92, 246, 0.3);
    }}

    /* Animated Pill CTA Button (✦ Analyze My Trip) */
    div[data-testid="stButton"] > button {{
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 50%, #8B5CF6 100%) !important;
        background-size: 200% 200% !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.35) !important;
        border-radius: 9999px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 24px rgba(34, 211, 238, 0.4), 0 0 16px rgba(139, 92, 246, 0.3) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4) !important;
        cursor: pointer !important;
        pointer-events: auto !important;
    }}
    div[data-testid="stButton"] > button:hover {{
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 32px rgba(34, 211, 238, 0.6), 0 0 28px rgba(139, 92, 246, 0.45) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
    }}
    div[data-testid="stButton"] > button:active {{
        transform: translateY(0px) scale(0.99) !important;
    }}

    /* Insight Box */
    .fb-insight-box {{
        background: {THEME['glass_card']};
        backdrop-filter: blur(14px);
        border: 1px solid {THEME['border_subtle']};
        border-left: 4px solid {THEME['primary_cyan']};
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }}
    .fb-insight-title {{
        font-weight: 700;
        font-size: 0.96rem;
        color: {THEME['text_primary']};
        margin-bottom: 4px;
    }}
    .fb-insight-body {{
        font-size: 0.88rem;
        color: {THEME['text_secondary']};
        line-height: 1.5;
    }}

    /* Flight Recommendation Card */
    .fb-flight-card {{
        background: {THEME['glass_card']};
        backdrop-filter: blur(16px);
        border: 1px solid {THEME['border_subtle']};
        border-top: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 14px;
        box-shadow: {THEME['card_shadow']};
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .fb-flight-card:hover {{
        border-color: rgba(34, 211, 238, 0.3);
        transform: translateY(-2px);
    }}
    .fb-flight-price {{
        font-size: 1.6rem;
        font-weight: 800;
        color: {THEME['primary_cyan']};
        text-shadow: 0 0 14px rgba(34, 211, 238, 0.3);
    }}

    /* Zero-height iframe helper container */
    iframe[title="st.iframe"] {{
        display: none !important;
        height: 0 !important;
        width: 0 !important;
        position: absolute !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # Streamlit-compatible parent window DOM injection for Custom Cursor & Background Canvas
    cursor_js = """
    <script>
    (function() {
        try {
            const pWin = window.parent;
            const pDoc = window.parent.document;
            if (!pWin || !pDoc) return;

            // Detect touch devices
            const isTouch = ('ontouchstart' in pWin) && pWin.matchMedia && pWin.matchMedia('(hover: none) and (pointer: coarse)').matches;
            const prefersReducedMotion = pWin.matchMedia && pWin.matchMedia('(prefers-reduced-motion: reduce)').matches;

            if (isTouch) return;

            // Inject Cursor & Canvas CSS into parent document head
            if (!pDoc.getElementById('fb-cursor-styles')) {
                const styleEl = pDoc.createElement('style');
                styleEl.id = 'fb-cursor-styles';
                styleEl.textContent = `
                    #fb-bg-canvas {
                        position: fixed !important;
                        top: 0 !important;
                        left: 0 !important;
                        width: 100vw !important;
                        height: 100vh !important;
                        pointer-events: none !important;
                        z-index: 0 !important;
                    }
                    #fb-trail-canvas {
                        position: fixed !important;
                        top: 0 !important;
                        left: 0 !important;
                        width: 100vw !important;
                        height: 100vh !important;
                        pointer-events: none !important;
                        z-index: 9997 !important;
                    }
                    #fb-cursor-dot {
                        position: fixed !important;
                        top: -100px;
                        left: -100px;
                        width: 7px !important;
                        height: 7px !important;
                        border-radius: 50% !important;
                        background: #22D3EE !important;
                        box-shadow: 0 0 10px #22D3EE, 0 0 20px rgba(34, 211, 238, 0.9) !important;
                        pointer-events: none !important;
                        z-index: 9999 !important;
                        transform: translate(-50%, -50%) !important;
                        transition: opacity 0.2s ease, transform 0.15s ease !important;
                        opacity: 0;
                    }
                    #fb-cursor-ring {
                        position: fixed !important;
                        top: -100px;
                        left: -100px;
                        width: 32px !important;
                        height: 32px !important;
                        border-radius: 50% !important;
                        border: 1.5px solid rgba(34, 211, 238, 0.65) !important;
                        box-shadow: 0 0 14px rgba(34, 211, 238, 0.35) !important;
                        pointer-events: none !important;
                        z-index: 9998 !important;
                        transform: translate(-50%, -50%) !important;
                        transition: width 0.2s ease, height 0.2s ease, border-color 0.2s ease, background-color 0.2s ease, box-shadow 0.2s ease !important;
                        opacity: 0;
                    }
                    #fb-cursor-ring.fb-cursor-hover {
                        width: 48px !important;
                        height: 48px !important;
                        border-color: #8B5CF6 !important;
                        background-color: rgba(34, 211, 238, 0.08) !important;
                        box-shadow: 0 0 22px rgba(139, 92, 246, 0.55) !important;
                    }
                    @media (hover: none) and (pointer: coarse) {
                        #fb-cursor-dot, #fb-cursor-ring, #fb-trail-canvas, #fb-bg-canvas {
                            display: none !important;
                        }
                    }
                `;
                pDoc.head.appendChild(styleEl);
            }

            // Create Canvas & Cursor elements on parent body
            let bgCanvas = pDoc.getElementById('fb-bg-canvas');
            if (!bgCanvas) {
                bgCanvas = pDoc.createElement('canvas');
                bgCanvas.id = 'fb-bg-canvas';
                pDoc.body.appendChild(bgCanvas);
            }

            let trailCanvas = pDoc.getElementById('fb-trail-canvas');
            if (!trailCanvas) {
                trailCanvas = pDoc.createElement('canvas');
                trailCanvas.id = 'fb-trail-canvas';
                pDoc.body.appendChild(trailCanvas);
            }

            let cursorDot = pDoc.getElementById('fb-cursor-dot');
            if (!cursorDot) {
                cursorDot = pDoc.createElement('div');
                cursorDot.id = 'fb-cursor-dot';
                pDoc.body.appendChild(cursorDot);
            }

            let cursorRing = pDoc.getElementById('fb-cursor-ring');
            if (!cursorRing) {
                cursorRing = pDoc.createElement('div');
                cursorRing.id = 'fb-cursor-ring';
                pDoc.body.appendChild(cursorRing);
            }

            // Prevent duplicate initialization on parent window
            if (pWin._fb_cursor_initialized) return;
            pWin._fb_cursor_initialized = true;

            const bgCtx = bgCanvas.getContext('2d');
            const trailCtx = trailCanvas.getContext('2d');

            let width = pWin.innerWidth;
            let height = pWin.innerHeight;

            function resize() {
                width = pWin.innerWidth;
                height = pWin.innerHeight;
                if (bgCanvas) {
                    bgCanvas.width = width;
                    bgCanvas.height = height;
                }
                if (trailCanvas) {
                    trailCanvas.width = width;
                    trailCanvas.height = height;
                }
            }
            pWin.addEventListener('resize', resize);
            resize();

            // Mouse coordinates & lerp
            let mouseX = width / 2;
            let mouseY = height / 2;
            let ringX = width / 2;
            let ringY = height / 2;
            let targetParallaxX = 0;
            let targetParallaxY = 0;
            let currentParallaxX = 0;
            let currentParallaxY = 0;
            let isMouseActive = false;

            // Constellation nodes for background
            const nodeCount = 14;
            const nodes = [];
            for (let i = 0; i < nodeCount; i++) {
                nodes.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    vx: (Math.random() - 0.5) * 0.3,
                    vy: (Math.random() - 0.5) * 0.3,
                    radius: Math.random() * 1.5 + 1.2,
                    color: i % 2 === 0 ? 'rgba(34, 211, 238, 0.45)' : 'rgba(139, 92, 246, 0.45)'
                });
            }

            // Trail particles (5-7 max, 0.5-0.7s fading)
            const trailParticles = [];
            const maxParticles = 7;

            pWin.addEventListener('mousemove', function(e) {
                isMouseActive = true;
                mouseX = e.clientX;
                mouseY = e.clientY;
                targetParallaxX = (e.clientX - width / 2) * 0.02;
                targetParallaxY = (e.clientY - height / 2) * 0.02;

                if (cursorDot) {
                    cursorDot.style.left = mouseX + 'px';
                    cursorDot.style.top = mouseY + 'px';
                    cursorDot.style.opacity = '1';
                }
                if (cursorRing) {
                    cursorRing.style.opacity = '1';
                }

                if (!prefersReducedMotion && trailParticles.length < maxParticles) {
                    trailParticles.push({
                        x: mouseX,
                        y: mouseY,
                        alpha: 0.65,
                        color: Math.random() > 0.5 ? '#22D3EE' : '#8B5CF6',
                        radius: Math.random() * 2.5 + 1.5
                    });
                }
            });

            // Hover interactions on parent
            pDoc.addEventListener('mouseover', function(e) {
                if (!cursorRing) return;
                const target = e.target;
                if (target && target.closest && target.closest('button, [data-baseweb="select"], .stRadio label, .fb-glass-card, .fb-kpi-card, a, input, [role="button"], [role="option"]')) {
                    cursorRing.classList.add('fb-cursor-hover');
                } else {
                    cursorRing.classList.remove('fb-cursor-hover');
                }
            });

            pDoc.addEventListener('mouseleave', function() {
                if (cursorDot) cursorDot.style.opacity = '0';
                if (cursorRing) cursorRing.style.opacity = '0';
            });

            // Animation Loop
            function animate() {
                pWin.requestAnimationFrame(animate);

                currentParallaxX += (targetParallaxX - currentParallaxX) * 0.05;
                currentParallaxY += (targetParallaxY - currentParallaxY) * 0.05;

                ringX += (mouseX - ringX) * 0.18;
                ringY += (mouseY - ringY) * 0.18;

                if (cursorRing && isMouseActive) {
                    cursorRing.style.left = ringX + 'px';
                    cursorRing.style.top = ringY + 'px';
                }

                // Draw background constellation
                if (bgCtx) {
                    bgCtx.clearRect(0, 0, width, height);

                    if (!prefersReducedMotion) {
                        for (let i = 0; i < nodes.length; i++) {
                            for (let j = i + 1; j < nodes.length; j++) {
                                const dx = (nodes[i].x + currentParallaxX) - (nodes[j].x + currentParallaxX);
                                const dy = (nodes[i].y + currentParallaxY) - (nodes[j].y + currentParallaxY);
                                const dist = Math.sqrt(dx * dx + dy * dy);
                                if (dist < 220) {
                                    bgCtx.strokeStyle = `rgba(34, 211, 238, ${0.08 * (1 - dist / 220)})`;
                                    bgCtx.lineWidth = 0.8;
                                    bgCtx.beginPath();
                                    bgCtx.moveTo(nodes[i].x + currentParallaxX, nodes[i].y + currentParallaxY);
                                    bgCtx.lineTo(nodes[j].x + currentParallaxX, nodes[j].y + currentParallaxY);
                                    bgCtx.stroke();
                                }
                            }
                        }

                        for (let i = 0; i < nodes.length; i++) {
                            const n = nodes[i];
                            n.x += n.vx;
                            n.y += n.vy;
                            if (n.x < 0 || n.x > width) n.vx *= -1;
                            if (n.y < 0 || n.y > height) n.vy *= -1;

                            bgCtx.fillStyle = n.color;
                            bgCtx.beginPath();
                            bgCtx.arc(n.x + currentParallaxX, n.y + currentParallaxY, n.radius, 0, Math.PI * 2);
                            bgCtx.fill();
                        }
                    }
                }

                // Draw cursor trail
                if (trailCtx) {
                    trailCtx.clearRect(0, 0, width, height);
                    if (!prefersReducedMotion) {
                        for (let i = trailParticles.length - 1; i >= 0; i--) {
                            const p = trailParticles[i];
                            p.alpha -= 0.035;
                            p.radius *= 0.94;
                            if (p.alpha <= 0 || p.radius <= 0.5) {
                                trailParticles.splice(i, 1);
                                continue;
                            }
                            trailCtx.fillStyle = p.color;
                            trailCtx.globalAlpha = p.alpha;
                            trailCtx.beginPath();
                            trailCtx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                            trailCtx.fill();
                        }
                        trailCtx.globalAlpha = 1.0;
                    }
                }
            }
            animate();

        } catch (e) {
            console.error('FlyBuddy Cursor error:', e);
        }
    })();
    </script>
    """
    components.html(cursor_js, height=0, width=0)
