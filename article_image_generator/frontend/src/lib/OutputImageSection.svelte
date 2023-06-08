<script lang="ts">
    import LoaderIcon from "@lib/LoaderIcon.svelte";
    import arrow_icon from "@assets/icons/arrow.svg";
    import MaskedIcon from "./MaskedIcon.svelte";

    export let images: Array<{
            image_base64: string,
            prompt: string,
            processing_method: string,
            visual_look: string,
            date: string,
        }> = undefined;
    export let article = undefined;
    export let image_preview: {
        image_base64: string,
        prompt: string,
        processing_method: string,
        visual_look: string,
        date: string,
    } = undefined;

    function downloadImage(image) {
        downloadBase64Image(image.image_base64, `${image.date}.png`);
    }

    function downloadBase64Image(base64Data, filename) {
        window.open(base64Data, '_blank')
    }
</script>

<div class="output-image-section">
    <div class="image-container">
        {#each images as image}
            {#if image.image_base64 !== undefined }
                <img
                    class="output-image"
                    src={image.image_base64}
                    alt="output"
                    on:click={() => downloadImage(image)}
                    on:mouseover={() => {image_preview = image}}
                    on:mouseleave={() => image_preview = {
                        image_base64: null,
                        prompt: null,
                        processing_method: null,
                        visual_look: null,
                        date: null,
                    }}
                />
            {:else}
                <div class="image-placeholder output-image"><LoaderIcon/></div>
            {/if}
        {/each}
    </div>

    <div class="description-container">
        <div class="font-primary description-section">
            <p>ARTICLE:</p>
            {#if article}
                <p class="color-text-lighter article-text">{article}</p>
            {:else}
                <p class="color-text-lighter placeholder">Lorem ipsum dolor sit amet...</p>
            {/if}
        </div>
        <a class="font-primary description-section" href="/contact">
            <p>More info</p>
            <div class="arrow-more-info">
                <MaskedIcon icon={arrow_icon} alt="More info" />
            </div>
        </a>
    </div>
</div>

<style>
    /*noinspection CssUnknownTarget*/
    @import url('https://fonts.googleapis.com/css2?family=Flow+Circular&display=swap');

    .output-image-section {
        border-bottom: 2px solid var(--color-secondary);

        margin: 0.5em;
    }

    .image-container {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        gap: 0.5em;

        height: 10rem;

        overflow-x: scroll;
    }

    .output-image {
        height: 100%;
        aspect-ratio: 1/1;

        border-radius: var(--border-radius);

        cursor: pointer;
    }

    .description-container {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: 0;
    }

    .description-section {
        display: flex;
        flex-direction: row;

        width: fit-content;
        white-space: nowrap;

        margin: 0;
    }

    .description-section p, a {
        margin: 0 0.5em 0 0;
    }

    .arrow-more-info {
        width: 1em;
        height: 1em;

        margin-left: -0.25em;
    }

    .image-placeholder {
        display: flex;
        justify-content: center;
        align-items: center;

        height: 100%;
        aspect-ratio: 1/1;
    }

    .article-text {
        width: 10em;

        overflow: hidden;
        text-overflow: ellipsis;
    }
</style>