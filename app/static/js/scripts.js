// toast 
document.addEventListener('DOMContentLoaded', function () {
    if (!sessionStorage.getItem('animationPlayed')) {
        sessionStorage.setItem('animationPlayed', 'true');
        document.getElementById('lab-music-title').classList.add('animate__animated', 'animate__fadeInDown', 'animate__slower');
    }
});

document.addEventListener('DOMContentLoaded', function () {
    var toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(function (toastElement) {
        var toast = new bootstrap.Toast(toastElement);
        toast.show();
    });
});

// mobile 
window.addEventListener('resize', function () {
    const mainContainer = document.querySelector('#main_container');
    const searchbar = document.querySelector("#searchbar")
    if (window.innerWidth <= 768) {
        mainContainer.classList.remove('vh-100');
        searchbar.classList.remove('w-50');
    } else {
        mainContainer.classList.add('vh-100');
        searchbar.classList.add('w-50');
    }
});

window.dispatchEvent(new Event('resize'));

// queue scroll 
document.getElementById('queueScrollDownBtn').addEventListener('click', function() {
  const queueContainer = document.querySelector('#current_queue > div');
  const buttonIcon = this.querySelector('i');

  if (buttonIcon.classList.contains('fa-arrow-down')) {
      queueContainer.scrollTo({ top: queueContainer.scrollHeight, behavior: 'smooth' });
      buttonIcon.classList.remove('fa-arrow-down');
      buttonIcon.classList.add('fa-arrow-up');
  } else {
      queueContainer.scrollTo({ top: 0, behavior: 'smooth' });
      buttonIcon.classList.remove('fa-arrow-up');
      buttonIcon.classList.add('fa-arrow-down');
  }
});


