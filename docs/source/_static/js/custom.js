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

// Point every license/contact button at the URL configured once in conf.py
// (`pro_license_url`), injected as a global by `_templates/layout.html`.
function wireProLicenseButtons() {
    const url = window.MOTRIXSIM_PRO_LICENSE_URL;
    if (!url) {
        return;
    }
    document.querySelectorAll("a.pro-license-btn").forEach(function (a) {
        a.href = url;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
    });
}

document.addEventListener("DOMContentLoaded", wireProLicenseButtons);
