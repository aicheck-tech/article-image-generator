<script lang="ts">
    import { onMount } from "svelte";

    import favicon from "@assets/favicon.ico";
    import Dropdown from "@lib/Dropdown.svelte";
    import OutputImageSection from "@lib/OutputImageSection.svelte";
    import { textToImage } from "@scripts/api-calls";

    import design_services_icon from "@assets/icons/design_services_fill.png"
    import brush_icon from "@assets/icons/brush_fill.png"

    const tags = ["realistic", "cinematic", "cartoon", "sketch"];

    let image_look: string;
    let textarea_value: string = "";
    let output_of_generated_objects: Array<{
        image: string;
        article: string;
        prompt: string;
    }> = [
        {
            image: "https://picsum.photos/512/512",
            article: "Lorem ipsum",
            prompt: "Lorem ipsum ale jinde",
        },
    ];

    async function imagine(event) {
        event.target.disabled = true;

        output_of_generated_objects.push({
            image: undefined,
            article: textarea_value,
            prompt: undefined,
        });
        output_of_generated_objects = output_of_generated_objects;

        textToImage(textarea_value, image_look).then((data) => {
            output_of_generated_objects[
                output_of_generated_objects.length - 1
            ].image = `data:image/png;base64,${data.image_base64}`;
            output_of_generated_objects[
                output_of_generated_objects.length - 1
            ].prompt = data.prompt;
            output_of_generated_objects = output_of_generated_objects;

            event.target.disabled = false;
        });
    }

    onMount(() => {
        let link = document.getElementById("favicon") as HTMLLinkElement;
        link.href = favicon;
    });
</script>

<main>
    <section class="title-panel">
        <h1 class="invert">Article image generator</h1>
        <h2 class="invert">Generate images for articles</h2>
    </section>

    <section class="input-panel">
        <textarea
            bind:value={textarea_value}
            class="article-textarea group"
            placeholder="Insert you article here..."
        />

        <section class="group input-panel-settings">
            <Dropdown
                name="Processing method"
                border_radius={["top-left", "top-right"]}
                current_item_id={0}
                items={["summarization", "key words"]}
                icon={design_services_icon}
            />
            <Dropdown
                name="Look"
                border_radius={[]}
                current_item_id={0}
                items={tags}
                bind:current_item={image_look}

                icon={brush_icon}
            />
            <button
                on:click={imagine}
                style="border-radius: 0 0 var(--border-radius) var(--border-radius)"
            >
                <span class="invert">Imagine</span>
            </button>
        </section>
    </section>

    <output class="output-panel">
        {#each output_of_generated_objects.slice().reverse() as output}
            <OutputImageSection
                image={output.image}
                article={output.article}
                prompt={output.prompt}
            />
        {/each}
    </output>
</main>

<style>
    main {
        display: grid;
        grid-template-rows: fit-content(1ch) 1fr;
        grid-template-columns: fit-content(1ch) 1fr;

        width: 100vw;
        height: 100vh;

        background: var(--color-primary);
    }

    button {
        border-radius: 0;
        width: 100%;
    }

    .title-panel {
        grid-row: 1;
        grid-column: 1 / 3;

        padding-top: 0.5em;
        padding-bottom: 1.4em;

        width: 100%;
        height: fit-content;

        display: flex;
        flex-direction: column;
        align-items: flex-start;

        background: var(--color-secondary);

        border-bottom: 2px solid var(--color-tertiary);

        text-align: left;
    }

    .invert {
        filter: invert(1);
    }

    .input-panel {
        grid-row: 2;
        grid-column: 1;

        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        gap: -0.5em;

        width: fit-content;
        height: 100%;

        box-sizing: border-box;

        border-right: 2px solid var(--color-tertiary);
    }

    .group {
        box-sizing: border-box;
    }

    .article-textarea {
        resize: both;
        overflow: auto;

        width: 15rem;
        min-width: 12rem;
        max-width: 25rem;

        height: 50%;
        min-height: 12rem;
        max-height: 65vh;

        margin: 0.5em;
        padding: 0.5em;

        background: var(--color-tertiary);

        border: 1px solid var(--color-tertiary);
        border-radius: var(--border-radius);

        color: var(--color-text);
    }

    .article-textarea::placeholder {
        color: var(--color-text);

        font-family: "Roboto Mono", monospace;
        font-weight: 300;
        font-size: 1em;
    }

    .article-textarea:focus {
        border: 2px solid var(--color-text);
        outline: none;
    }

    .input-panel-settings {
        display: flex;
        flex-direction: column;

        justify-content: space-between;

        margin: 0.5em;
    }

    .output-panel {
        grid-row: 2;
        grid-column: 2;

        background: var(--color-primary);

        display: flex;
        flex-direction: column;

        box-sizing: border-box;
        overflow-y: scroll;
    }
</style>
