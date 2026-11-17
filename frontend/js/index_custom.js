function navigateToCountryProperties() {
              const sel = document.getElementById('homeCountrySelect');
              const country = sel ? sel.value : 'in';
              window.location.href = '/property?country=' + country;
            }

// Real-Time Device Auto-Detection
    (function detectDeviceMode() {
      function checkDevice() {
        const isMobileScreen = window.innerWidth <= 768;
        const isTouch = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
        const isMobileUA = /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

        if (isMobileScreen || (isTouch && isMobileUA)) {
          document.documentElement.classList.add('device-mobile');
          document.documentElement.classList.remove('device-desktop');
        } else {
          document.documentElement.classList.add('device-desktop');
          document.documentElement.classList.remove('device-mobile');
        }
      }

      checkDevice();
      window.addEventListener('resize', checkDevice);

      // Mobile Menu Toggle logic
      document.addEventListener('DOMContentLoaded', function() {
        const toggleBtn = document.getElementById('mobileMenuToggle');
        const navList = document.getElementById('navLinks');
        if (toggleBtn && navList) {
          toggleBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            navList.classList.toggle('mobile-open');
          });

          // Close menu when clicking outside or clicking a link
          document.addEventListener('click', function(e) {
            if (!navList.contains(e.target) && !toggleBtn.contains(e.target)) {
              navList.classList.remove('mobile-open');
            }
          });

          navList.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
              navList.classList.remove('mobile-open');
            });
          });
        }
      });
    })();
