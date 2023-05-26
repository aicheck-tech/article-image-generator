<section class="contact-wrapper">
    <a class="font-primary" href="/contact">contact</a>
    <a href="http://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1" target="_blank" class="font-primary license-link">
        License
        <div class="license-icons">
            <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"
            alt="">
            <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"
            alt="">
            <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1"
            alt="">
            <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nd.svg?ref=chooser-v1"
            alt="">
        </div>
    </a>
</section>

<style>
    .contact-wrapper {
        position: absolute;
        bottom: 0.5em;
        right: 1em;

        display: flex;
        flex-direction: row;
        align-items: flex-end;

        gap: 0.5em;
    }

    .contact-wrapper a {
        cursor: pointer;
    }

    .license-link {
        display: flex;
        flex-direction: column-reverse;
        align-items: flex-end;

        gap: 0.5em;
    }

    .license-icons {
        display: none;
        flex-direction: column;

        gap: 0.25em;
        text-decoration: none;
    }

    .license-link:hover .license-icons {
        display: flex;
    }
</style>