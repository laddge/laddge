if (document.defaultView.getComputedStyle(document.getElementById('sidebar'), null).display != 'none') {
    fetch('https://api.laddge.net/profile')
        .then(res => {
            return res.json();
        })
        .then(data => {
            document.getElementById('twitterBanner').src = data.profile_banner;
            document.getElementById('twitterImage').src = data.profile_image;
            document.getElementById('twitterName').innerText = data.name;
            document.getElementById('twitterScreenName').innerText = '@' + data.screen_name;
            document.getElementById('twitterDesc').innerText = data.desc;
            document.getElementById('twitterFollow').innerText += data.follow;
            document.getElementById('twitterFollower').innerText += data.follower;
            twemoji.parse(document.getElementById('twitterCardBody'));
            document.getElementById('twitterCard').classList.remove('d-none');
        })
        .catch(err => {
            console.log(err);
        });
}

let cardLoaded = false;

function loadCards() {
    if (cardLoaded) {
        return;
    }
    const cardAPIInstance = new CardAPI('cardapi', '\
        <div class="card mt-3 me-3 d-inline-block" style="width: 18rem;">\
        <img class="bd-placeholder-img card-img-top w-100" src="{{ image }}" style="width: 18rem; height: 9rem;" alt="">\
        <div class="card-body">\
        <div class="card-title w-100 text-truncate my-0 h3">{{ title }}</div>\
        <div class="card-text w-100 text-truncate-2 text-secondary small mt-1">{{ description }}</div>\
        <div class="text-end">\
        <a href="{{ href }}" class="btn btn-outline-primary btn-sm mt-3">Open</a>\
        </div>\
        </div>\
        </div>\
        ');
    cardAPIInstance.load();
    cardLoaded = true;
}

if (document.getElementById('products').getBoundingClientRect().top + window.pageYOffset < window.innerHeight) {
    loadCards();
}

window.addEventListener('scroll', loadCards);
