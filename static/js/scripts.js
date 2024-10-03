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


