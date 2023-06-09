<script lang="ts">
    import { onMount } from "svelte";

    import favicon from "@assets/favicon.ico";
    import Dropdown from "@lib/Dropdown.svelte";
    import OutputImageSection from "@lib/OutputImageSection.svelte";
    import ContactSection from "@lib/ContactSection.svelte";
    import { textToImage } from "@scripts/api-calls";

    import design_services_icon from "@assets/icons/design_services_fill.png";
    import brush_icon from "@assets/icons/brush_fill.png";
    import TitlePanel from "./lib/TitlePanel.svelte";
    import SmartSlider from "@lib/SmartSlider.svelte";
    import ScrollingText from "@lib/ScrollingText.svelte";

    const image_looks = ["realistic", "cinematic", "cartoon", "sketch"];
    const processing_methods = ["Key-words", "Summarization"];

    let current_image_look: string;
    let current_processing_method: string;
    let current_batch_size: string = "1";
    let image_preview: {
        image_base64: string,
        prompt: string,
        processing_method: string,
        visual_look: string,
        date: string,
    } = {
        image_base64: null,
        prompt: null,
        processing_method: null,
        visual_look: null,
        date: null
    }

    let textarea_value: string = "";
    let output_of_generated_objects: Array<{
        images: Array<{
            image_base64: string,
            prompt: string,
            processing_method: string,
            visual_look: string,
            date: string,
        }>,
        article: string
    }> = [
        {
            images: [
                {
                    image_base64: "https://picsum.photos/512/512",
                    prompt: "Something something",
                    processing_method: "summarization",
                    visual_look: "realistic",
                    date: new Date().toISOString().split('T')[0]
                },
                {
                    image_base64: "https://picsum.photos/515/515",
                    prompt: "Something else",
                    processing_method: "summarization",
                    visual_look: "realistic",
                    date: new Date().toISOString().split('T')[0]
                },
            ],
            article: "This is a article"
        }
    ]

    async function imagine(event) {
        event.target.disabled = true;
        const current_time = (new Date()).toISOString().split('T')[0];

        if (textarea_value.length < 3) {

            event.target.children[0].innerHTML = "Text missing!";

            setTimeout(() => {
                event.target.children[0].innerHTML = "Imagine";
                event.target.disabled = false;
            }, 2000);

            return;
        }

        const image_placeholder = {
            image_base64: undefined,
            prompt: undefined,
            processing_method: current_processing_method,
            visual_look: current_image_look,
            date: current_time,
        }
        let image_placeholders = [];
        for (let i = 0; i < parseInt(current_batch_size); i++) {
            image_placeholders.push(image_placeholder);
        }

        output_of_generated_objects.push({
            images: image_placeholders,
            article: textarea_value,
        });
        output_of_generated_objects = output_of_generated_objects;

        textToImage(
            textarea_value,
            current_image_look,
            current_processing_method,
            parseInt(current_batch_size)
            ).then((data) => {
                if (data.images_base64.length == 0) {
                    output_of_generated_objects.pop();
                    output_of_generated_objects = output_of_generated_objects;
                    event.target.disabled = false;
                    return;
                }

                output_of_generated_objects[output_of_generated_objects.length - 1].images = [];
                data.images_base64.forEach((image, idx) => {
                    output_of_generated_objects[output_of_generated_objects.length - 1].images.push({
                        image_base64: `data:image/png;base64,${image}`,
                        prompt: data.prompts[idx].text,
                        processing_method: current_processing_method,
                        visual_look: current_image_look,
                        date: current_time,
                    })
                });
                output_of_generated_objects = output_of_generated_objects;

                saveImage();

                event.target.disabled = false;
            }
        );
    }

    function saveImage() {
        const link = document.createElement('a');
        link.href = image_preview.image_base64;
        link.download = 'image.png';

        // Set the anchor element to trigger a download only after the image data has fully loaded
        link.addEventListener('load', () => {
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });

        // Start loading the image
        link.dispatchEvent(new MouseEvent('click'));
    }

    onMount(() => {
        let link = document.getElementById("favicon") as HTMLLinkElement;
        link.href = favicon;
    });
</script>

<main>
    <TitlePanel />

    <div class="body-wrapper">
        <section class="input-panel">
            <textarea
                bind:value={textarea_value}
                class="article-textarea font-secondary-regular"
                placeholder="Insert you article here..."
            ></textarea>
            <Dropdown
                name="Processing method"
                current_item_id={1}
                items={processing_methods}
                icon={design_services_icon}
                bind:current_item={current_processing_method}
            />
            <Dropdown
                name="Look"
                current_item_id={0}
                items={image_looks}
                bind:current_item={current_image_look}
                icon={brush_icon}
            />
            <SmartSlider
                slider_text="Number of images"
                value_min="1"
                value_max="4"
                bind:value={current_batch_size}

            />
            <button on:click={imagine} class="imagine-button">
                <span class="invert">Imagine</span>
            </button>
        </section>

        <output class="output-panel">
            {#each output_of_generated_objects.slice().reverse() as output}
                <OutputImageSection
                    images={output.images}
                    article={output.article}
                    bind:image_preview={image_preview}
                />
            {/each}
        </output>

        <section class="info-panel">
            {#if image_preview.image_base64 !== null}
                <h2 class="font-primary">Image preview</h2>
                <img src={image_preview.image_base64} alt="Generated"/>
                <div class="image-preview-line">
                    <p class="font-secondary-bold">Prompt: </p>
                    <ScrollingText>
                        <p class="font-secondary-regular color-text-lighter text-compact">{image_preview.prompt}</p>
                    </ScrollingText>
                </div>
                <div class="image-preview-line">
                    <p class="font-secondary-bold">Processing method: </p>
                    <p class="font-secondary-regular color-text-lighter">{image_preview.processing_method}</p>
                </div>
                <div class="image-preview-line">
                    <p class="font-secondary-bold">Visual look: </p>
                    <p class="font-secondary-regular color-text-lighter">{image_preview.visual_look}</p>
                </div>
                <div class="image-preview-line">
                    <p class="font-secondary-bold">Creation date: </p>
                    <p class="font-secondary-regular color-text-lighter">{image_preview.date}</p>
                </div>
            {:else}
                <h2 class="font-primary">How this works</h2>
                <ul class="font-secondary-regular color-text-lighter">
                    <li>Enter your article</li>
                    <li>Our advanced algorithms analyze your text</li>
                    <li>Sit back and watch as the generator selects relevant images to perfectly complement your content</li>
                </ul>
            {/if}
        </section>
    </div>
</main>

<ContactSection />

<style>
    main {
        width: 100%;
        height: 100%;

        display: flex;
        flex-direction: column;
    }

    .body-wrapper {
        display: flex;
        flex-direction: row;

        height: 100%;

        overflow-y: auto;
    }

    .input-panel {
        width: 100%;

        flex: calc(1 / 4);
        min-width: 20em;

        overflow-y: scroll;

        display: flex;
        flex-direction: column;

        padding: 0.5em 0.25em 0.5em 0.5em;
        box-sizing: border-box;
    }

    .output-panel {
        width: 100%;

        flex: calc(1 / 2);

        overflow-y: scroll;
    }

    .info-panel {
        flex: calc(1 / 4);

        width: 100%;

        display: flex;
        flex-direction: column;

        padding: 0.5em;
    }

    .info-panel > ul {
        margin: 0;
        padding: 0 0 0 1em;
    }

    .image-preview-line {
        display: inline-block;
    }

    .info-panel > img {
        width: 100%;
    }

    .article-textarea {
        max-height: 30em;
        min-height: 10em;

        resize: vertical;

        background: var(--color-primary);
        border: 2px solid var(--color-secondary);
        border-radius: var(--border-radius);

        padding: 0.5em;

        font-size: 1em;

        color: var(--color-text);
    }

    .article-textarea:focus {
        outline: none;
    }

    .article-textarea::placeholder {
        color: var(--color-text-lighter);
    }

    .imagine-button {
        position: sticky;
        bottom: 0;
    }
</style>

