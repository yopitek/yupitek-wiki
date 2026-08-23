/**
 * Yupitek Interactive Image Lightbox & Zoom System
 * Features:
 * - Fullscreen high-resolution vector/bitmap overlay
 * - Click-to-open on all documentation images (.svg, .png, .jpg)
 * - Zoom Controls: Zoom In (+), Zoom Out (-), Reset (1:1), Fullscreen, Open Raw
 * - Mouse Wheel Zoom & Double-Click 2x Zoom
 * - Drag-to-Pan when zoomed in
 * - Keyboard navigation (ESC to close, +/- to zoom)
 * - Dark & Light mode adaptive
 */

let activeLightbox = null;

function createLightbox() {
  if (document.getElementById('yupitek-image-lightbox')) {
    return document.getElementById('yupitek-image-lightbox');
  }

  const container = document.createElement('div');
  container.id = 'yupitek-image-lightbox';
  container.className = 'yp-lightbox-overlay';
  container.setAttribute('aria-hidden', 'true');

  container.innerHTML = `
    <div class="yp-lightbox-backdrop"></div>
    <div class="yp-lightbox-toolbar">
      <div class="yp-lightbox-info">
        <span class="yp-lightbox-title"></span>
      </div>
      <div class="yp-lightbox-actions">
        <button type="button" class="yp-btn yp-btn-zoom-out" title="縮小 (Zoom Out)">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        </button>
        <span class="yp-lightbox-scale">100%</span>
        <button type="button" class="yp-btn yp-btn-zoom-in" title="放大 (Zoom In)">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        </button>
        <button type="button" class="yp-btn yp-btn-reset" title="重設大小 (Reset)">1:1</button>
        <a href="#" target="_blank" rel="noopener noreferrer" class="yp-btn yp-btn-open" title="在新分頁開啟原圖 (Open in new tab)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
        </a>
        <button type="button" class="yp-btn yp-btn-close" title="關閉 (Close ESC)">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>
    </div>
    <div class="yp-lightbox-stage">
      <div class="yp-lightbox-content">
        <img class="yp-lightbox-img" src="" alt="" draggable="false" />
      </div>
    </div>
  `;

  document.body.appendChild(container);

  // State variables for zoom & pan
  let scale = 1;
  let translateX = 0;
  let translateY = 0;
  let isDragging = false;
  let startX = 0;
  let startY = 0;

  const stage = container.querySelector('.yp-lightbox-stage');
  const content = container.querySelector('.yp-lightbox-content');
  const img = container.querySelector('.yp-lightbox-img');
  const scaleLabel = container.querySelector('.yp-lightbox-scale');
  const titleLabel = container.querySelector('.yp-lightbox-title');
  const openLink = container.querySelector('.yp-btn-open');
  const btnZoomIn = container.querySelector('.yp-btn-zoom-in');
  const btnZoomOut = container.querySelector('.yp-btn-zoom-out');
  const btnReset = container.querySelector('.yp-btn-reset');
  const btnClose = container.querySelector('.yp-btn-close');
  const backdrop = container.querySelector('.yp-lightbox-backdrop');

  function updateTransform() {
    content.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    scaleLabel.textContent = `${Math.round(scale * 100)}%`;
    if (scale > 1) {
      stage.classList.add('yp-is-zoomed');
    } else {
      stage.classList.remove('yp-is-zoomed');
    }
  }

  function setScale(newScale, centerX = 0, centerY = 0) {
    const clamped = Math.min(Math.max(newScale, 0.5), 4.0);
    scale = clamped;
    if (scale <= 1) {
      translateX = 0;
      translateY = 0;
    }
    updateTransform();
  }

  function open(src, alt) {
    img.src = src;
    img.alt = alt || '';
    titleLabel.textContent = alt || '圖片檢視 (Image Viewer)';
    openLink.href = src;
    scale = 1;
    translateX = 0;
    translateY = 0;
    updateTransform();

    container.classList.add('yp-active');
    container.setAttribute('aria-hidden', 'false');
    document.body.classList.add('yp-lightbox-open');
    activeLightbox = container;
  }

  function close() {
    container.classList.remove('yp-active');
    container.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('yp-lightbox-open');
    activeLightbox = null;
    setTimeout(() => {
      img.src = '';
    }, 200);
  }

  // Event Listeners
  backdrop.addEventListener('click', close);
  btnClose.addEventListener('click', close);

  btnZoomIn.addEventListener('click', (e) => {
    e.stopPropagation();
    setScale(scale + 0.25);
  });

  btnZoomOut.addEventListener('click', (e) => {
    e.stopPropagation();
    setScale(scale - 0.25);
  });

  btnReset.addEventListener('click', (e) => {
    e.stopPropagation();
    setScale(1);
  });

  // Double click to toggle 2x zoom
  stage.addEventListener('dblclick', (e) => {
    if (e.target.closest('.yp-lightbox-toolbar')) return;
    if (scale === 1) {
      setScale(2);
    } else {
      setScale(1);
    }
  });

  // Mouse wheel zoom
  stage.addEventListener('wheel', (e) => {
    e.preventDefault();
    const delta = e.deltaY < 0 ? 0.15 : -0.15;
    setScale(scale + delta);
  }, { passive: false });

  // Pan / Dragging
  stage.addEventListener('mousedown', (e) => {
    if (scale <= 1 || e.target.closest('.yp-lightbox-toolbar')) return;
    isDragging = true;
    startX = e.clientX - translateX;
    startY = e.clientY - translateY;
    stage.classList.add('yp-is-dragging');
  });

  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    translateX = e.clientX - startX;
    translateY = e.clientY - startY;
    updateTransform();
  });

  window.addEventListener('mouseup', () => {
    if (isDragging) {
      isDragging = false;
      stage.classList.remove('yp-is-dragging');
    }
  });

  // Touch Support
  let initialTouchDist = 0;
  let initialTouchScale = 1;

  stage.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1 && scale > 1) {
      isDragging = true;
      startX = e.touches[0].clientX - translateX;
      startY = e.touches[0].clientY - translateY;
    } else if (e.touches.length === 2) {
      isDragging = false;
      initialTouchDist = Math.hypot(
        e.touches[0].clientX - e.touches[1].clientX,
        e.touches[0].clientY - e.touches[1].clientY
      );
      initialTouchScale = scale;
    }
  }, { passive: true });

  stage.addEventListener('touchmove', (e) => {
    if (isDragging && e.touches.length === 1) {
      translateX = e.touches[0].clientX - startX;
      translateY = e.touches[0].clientY - startY;
      updateTransform();
    } else if (e.touches.length === 2 && initialTouchDist > 0) {
      const dist = Math.hypot(
        e.touches[0].clientX - e.touches[1].clientX,
        e.touches[0].clientY - e.touches[1].clientY
      );
      const factor = dist / initialTouchDist;
      setScale(initialTouchScale * factor);
    }
  }, { passive: true });

  stage.addEventListener('touchend', () => {
    isDragging = false;
    initialTouchDist = 0;
  });

  // Keyboard shortcut
  window.addEventListener('keydown', (e) => {
    if (!activeLightbox) return;
    if (e.key === 'Escape') {
      close();
    } else if (e.key === '+' || e.key === '=') {
      setScale(scale + 0.25);
    } else if (e.key === '-' || e.key === '_') {
      setScale(scale - 0.25);
    } else if (e.key === '0') {
      setScale(1);
    }
  });

  return { container, open, close };
}

let lightboxAPI = null;

function bindArticleImages() {
  if (typeof window === 'undefined') return;

  if (!lightboxAPI) {
    lightboxAPI = createLightbox();
  }

  const images = Array.from(
    document.querySelectorAll('.markdown img, article img, .theme-doc-markdown img')
  ).filter((img) => {
    return (
      !img.classList.contains('no-lightbox') &&
      !img.closest('.navbar') &&
      !img.closest('.footer') &&
      !img.closest('.badge')
    );
  });

  images.forEach((img) => {
    if (img.dataset.ypLightboxBound === 'true') return;
    img.dataset.ypLightboxBound = 'true';
    img.classList.add('yp-lightbox-target');

    // Add visual hint overlay / cursor
    img.addEventListener('click', (e) => {
      e.preventDefault();
      const highResSrc = img.getAttribute('src');
      const altText = img.getAttribute('alt') || img.getAttribute('title') || '';
      lightboxAPI.open(highResSrc, altText);
    });
  });
}

export function onRouteDidUpdate() {
  setTimeout(bindArticleImages, 150);
}

if (typeof window !== 'undefined') {
  if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', bindArticleImages);
  } else {
    setTimeout(bindArticleImages, 100);
  }
}
