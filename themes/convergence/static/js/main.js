// ============================================
// THE CONVERGENCE THESIS — Scroll Animations
// Vanilla JS, no dependencies
// ============================================

(function() {
  'use strict';

  // --- Header scroll effect ---
  const header = document.getElementById('site-header');
  let lastScrollY = 0;

  function handleHeaderScroll() {
    const currentScrollY = window.scrollY;
    if (currentScrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    lastScrollY = currentScrollY;
  }

  // --- Mobile menu toggle ---
  const menuToggle = document.getElementById('menu-toggle');
  const siteNav = document.getElementById('site-nav');

  if (menuToggle && siteNav) {
    menuToggle.addEventListener('click', function() {
      siteNav.classList.toggle('open');
    });

    // Close menu on nav link click
    siteNav.querySelectorAll('.nav-link').forEach(function(link) {
      link.addEventListener('click', function() {
        siteNav.classList.remove('open');
      });
    });
  }

  // --- Intersection Observer for reveal animations ---
  function createRevealObserver() {
    const observerOptions = {
      root: null,
      rootMargin: '0px 0px -80px 0px',
      threshold: 0.1
    };

    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observe chapter numbers
    document.querySelectorAll('.chapter-number').forEach(function(el) {
      observer.observe(el);
    });

    // Observe paragraphs inside chapters
    document.querySelectorAll('.chapter p').forEach(function(el) {
      observer.observe(el);
    });

    // Observe callout boxes
    document.querySelectorAll('.callout').forEach(function(el) {
      observer.observe(el);
    });

    // Observe generic reveal elements
    document.querySelectorAll('.reveal').forEach(function(el) {
      observer.observe(el);
    });

    // Observe scenario blocks
    document.querySelectorAll('.scenario').forEach(function(el) {
      el.classList.add('reveal');
      observer.observe(el);
    });
  }

  // --- Hero fade-in on load ---
  function initHero() {
    const heroElements = document.querySelectorAll('.hero .reveal-fade');
    // Small delay to ensure CSS transitions work
    setTimeout(function() {
      heroElements.forEach(function(el) {
        el.classList.add('revealed');
      });
    }, 100);
  }

  // --- Smooth scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header-height')) || 64;
        const targetPosition = target.getBoundingClientRect().top + window.scrollY - offset - 20;
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // --- Initialize ---
  window.addEventListener('scroll', handleHeaderScroll, { passive: true });
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      initHero();
      createRevealObserver();
    });
  } else {
    initHero();
    createRevealObserver();
  }

})();
