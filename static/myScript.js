const nav  = document.querySelector('nav')
const toggleLink = document.getElementById('toggleNav');

  toggleLink.addEventListener('click', function (event) {
    event.preventDefault(); // prevent page jump

    if (nav.style.display !== 'none') {
      nav.style.display = 'none';
      toggleLink.textContent = '[ ▼ ]';
    } else {
      nav.style.display = 'flex';
      toggleLink.textContent = '[ ▲ ]';
    }
  });


/* 
    Previous Sloka and Next Sloka
*/

const prevLink = document.getElementById('prevSloka');
const nextLink = document.getElementById('nextSloka');

// When user clicks the anchor
prevLink.addEventListener('click', function(event) {
  event.preventDefault();

  window.location.href = this.getAttribute('href');

});

nextLink.addEventListener('click', function(event) {
  event.preventDefault();
  window.location.href = this.getAttribute('href');


  // window.history.forward();
});

// When user presses left/right arrow keys
document.addEventListener('keydown', function(event) {
  if (event.key === 'ArrowLeft') {
    prevLink.click();
    // window.history.back();
  } else if (event.key === 'ArrowRight') {
    nextLink.click();
    // window.history.forward();
  } else if (event.key === 'ArrowUp')  {
    toggleLink.click();
    // window.history.forward();
  }
  else if (event.key === 'ArrowDown')  {
    toggleLink.click();
    // window.history.forward();
  }  
});


