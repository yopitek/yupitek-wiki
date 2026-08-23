import mediumZoom from 'medium-zoom';

let zoomInstance = null;

function applyZoom() {
  if (typeof window === 'undefined') {
    return;
  }

  if (zoomInstance) {
    zoomInstance.detach();
  }

  const images = Array.from(
    document.querySelectorAll(
      '.markdown img:not(.no-zoom), article img:not(.no-zoom)'
    )
  ).filter((img) => {
    return !img.closest('.navbar') && !img.closest('.footer');
  });

  if (images.length > 0) {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    zoomInstance = mediumZoom(images, {
      margin: 24,
      background: isDark ? 'rgba(10, 15, 29, 0.94)' : 'rgba(255, 255, 255, 0.96)',
      scrollOffset: 40,
    });
  }
}

export function onRouteDidUpdate() {
  setTimeout(applyZoom, 150);
}

if (typeof window !== 'undefined') {
  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.attributeName === 'data-theme') {
        applyZoom();
      }
    }
  });

  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme'],
  });

  if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', applyZoom);
  } else {
    setTimeout(applyZoom, 100);
  }
}
