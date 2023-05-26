<script lang="ts">
    import { onMount } from "svelte";

    import favicon from "@assets/favicon.ico";
    import Dropdown from "@lib/Dropdown.svelte";
    import OutputImageSection from "@lib/OutputImageSection.svelte";
    import ContactSection from "@lib/ContactSection.svelte";
    import { textToImage } from "@scripts/api-calls";

    import design_services_icon from "@assets/icons/design_services_fill.png";
    import brush_icon from "@assets/icons/brush_fill.png";
    import view_column_icon from "@assets/icons/view_column_fill.svg";
    import TitlePanel from "./lib/TitlePanel.svelte";

    const image_looks = ["realistic", "cinematic", "cartoon", "sketch"];
    const processing_methods = ["Key-words", "Summarization"];

    let current_image_look: string;
    let current_processing_method: string;
    let current_batch_size: string;

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
    }> = []

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
                        prompt: data.prompts[idx],
                        processing_method: current_processing_method,
                        visual_look: current_image_look,
                        date: current_time,
                    }) 
                });
                output_of_generated_objects = output_of_generated_objects;

                event.target.disabled = false;
            }
        );
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
            />

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
            <Dropdown
                name="Number of images"
                current_item_id={0}
                items={["1", "2", "3", "4"]}
                icon={view_column_icon}
                bind:current_item={current_batch_size}
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
                />
            {/each}
        </output>

        <section class="info-panel">
            <h2 class="font-primary">How this works</h2>
            <ul class="font-secondary-regular color-text-lighter">
                <li>Enter your article</li>
                <li>Our advanced algorithms analyze your text</li>
                <li>Sit back and watch as the generator selects relevant images to perfectly complement your content</li>
            </ul>
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

        padding: 0.5em;
        padding-right: 0.25em;
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
        padding: 0;
        
        padding-left: 1em;
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

