<script>
    import TitlePanel from "@/lib/TitlePanel.svelte";
    import MaskedIcon from "@/lib/MaskedIcon.svelte";
    import arrow_icon from "@assets/icons/arrow.svg";
    
    import linkedin_icon from "@assets/icons/icons8-linkedin.svg"
    import github_icon from "@assets/icons/github-mark.svg"
    import ContactSection from "@/lib/ContactSection.svelte";

    const developers = [
        {
            name: "Ondřej Šteffan",
            role: "Frontend/Backend Developer",
            linkedin: "https://www.linkedin.com/in/steffan-ondrej/",
            github: "https://github.com/OriginalStefikO"
        },
        {
            name: "Jan Soukeník",
            role: "AI/Backend Developer",
            linkedin: "https://www.linkedin.com/in/jan-soukenik/",
            github: "https://github.com/Dzeniks"
        }
    ]
</script>

<main>
    <TitlePanel />

    <a href="/" class="home-button">
        <div class="return-home-icon">
            <MaskedIcon icon={arrow_icon} alt="arrow_icon" />
        </div>
        <p class="font-primary">Return home</p>
    </a>
    <div class="body-wrapper">
        <h2 class="font-primary">About us</h2>
        <p class="font-secondary-regular">
            We are passionate developers who want to make the world a better place.
        </p>
        <div class="splitter"></div>

        <h2 class="font-primary">Developers</h2>
        {#each developers as developer }
            <div class="user-section">

                <p class="font-secondary-regular">{developer.name}</p>
                <p class="font-secondary-regular">{developer.role}</p>
                
                <div class="flex-row">
                    <div class="icon-wrapper">
                        <MaskedIcon icon={linkedin_icon} alt="linkedin_icon" url={developer.linkedin} />
                    </div>
                    <div class="icon-wrapper">
                        <MaskedIcon icon={github_icon} alt="github_icon" url={developer.github} />
                    </div>
                </div>
            </div>
                
        {/each}
        <div class="splitter"></div>
    </div>

    <ContactSection />
</main>

<style>
    main {
        width: 100%;
        height: 100%;

        display: flex;
        flex-direction: column;
    }

    .body-wrapper {
        display: flex;
        flex-direction: column;

        height: 100%;
        overflow-y: auto;

        padding: 0.5em;
        margin: 0 2em;

        gap: 1em;
    }

    .splitter {
        height: 2px;
        width: 100%;
        background-color: var(--color-secondary);

        margin-top: 0.25em;
        margin-bottom: 1em;
    }

    .flex-row {
        display: flex;
        flex-direction: row;
    }

    .home-button {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 0.3em;

        font-size: 1.2em;
        margin-left: 0.5em;
        margin-top: 0.5em;
    }

    .return-home-icon {
        width: 1em;
        height: 1em;

        transform: rotate(180deg);
    }
</style>