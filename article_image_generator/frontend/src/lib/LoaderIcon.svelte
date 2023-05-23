<div class="loader-ellipsis"><div></div><div></div><div></div><div></div></div>

<!-- FIXME variables not perfect -->
<style>
    .loader-ellipsis {
        display: inline-block;
        position: relative;
        width: var(--loader-size);
        height: var(--loader-size);
    }

    .loader-ellipsis div {
        position: absolute;
        top: 33px;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: rgb(var(--color-text));
        animation-timing-function: var(--loader-animation-timing);
    }

    .loader-ellipsis div:nth-child(1) {
        left: 8px;
        animation: loader-ellipsis1 var(--loader-animation-duration) infinite;
    }

    .loader-ellipsis div:nth-child(2) {
        left: 8px;
        animation: loader-ellipsis2 var(--loader-animation-duration) infinite;
    }

    .loader-ellipsis div:nth-child(3) {
        left: 32px;
        animation: loader-ellipsis2 var(--loader-animation-duration) infinite;
    }

    .loader-ellipsis div:nth-child(4) {
        left: 56px;
        animation: loader-ellipsis3 var(--loader-animation-duration) infinite;
    }

    @keyframes loader-ellipsis1 {
        0% {
            transform: scale(0);
        }
        100% {
            transform: scale(1);
        }
    }

    @keyframes loader-ellipsis3 {
        0% {
            transform: scale(1);
        }
        100% {
            transform: scale(0);
        }
    }

    @keyframes loader-ellipsis2 {
        0% {
            transform: translate(0, 0);
        }
        100% {
            transform: translate(24px, 0);
        }
    }
</style>

