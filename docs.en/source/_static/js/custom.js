function openVideoControls(video) {
    video.controls = true;
}

function isWeChatMobile() {
    const ua = navigator.userAgent.toLowerCase();
    return /micromessenger/.test(ua) && /android|iphone|ipad|ipod/.test(ua);
}

if (isWeChatMobile()) {
    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll("video").forEach(openVideoControls);
    });
}
