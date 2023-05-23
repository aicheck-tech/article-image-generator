<script lang="ts">
    import { onMount } from "svelte";
    
    import favicon from "@assets/favicon.ico";
    import Dropdown from "@lib/Dropdown.svelte";
    import OutputImageSection from "@lib/OutputImageSection.svelte";
    import { textToImage } from "@scripts/api-calls"

    const tags = ["realistic", "cinematic", "cartoon", "sketch"];

    let image_look: string;
    let textarea_value: string = "";
    let output_of_generated_objects: Array<{image: string, article: string, prompt: string}> = [];

    async function imagine() {
        output_of_generated_objects.push({
            image: undefined,
            article: textarea_value,
            prompt: undefined
        });
        output_of_generated_objects = output_of_generated_objects;

        textToImage(textarea_value, image_look).then((data) => {
            output_of_generated_objects[output_of_generated_objects.length - 1].image = `data:image/png;base64,${data.image_base64}`;
            output_of_generated_objects[output_of_generated_objects.length - 1].prompt = data.prompt;
            output_of_generated_objects = output_of_generated_objects;
        });
    }

    onMount(() => {
        let link = document.getElementById("favicon") as HTMLLinkElement;
        link.href = favicon;
    });
</script>

<main>
    <section class="title-panel">
        <h1>Article image generator</h1>
        <h2>Generate images for articles</h2>
    </section>

    <section class="input-panel">
        <textarea bind:value={textarea_value} class="article-textarea group" placeholder="Insert you article here..." />
        
        <section class="group input-panel-settings">
            <Dropdown 
                name="Type" 
                border_radius={["top-left", "top-right"]} 
                current_item_id={0} 
                items={["summarization", "key words"]} 
            />
            <Dropdown 
                name="Look" 
                border_radius={[]} 
                current_item_id={0} 
                items={tags}
                bind:current_item={image_look} 
            />
            <button on:click={imagine} style="border-radius: 0 0 var(--border-radius) var(--border-radius)">Imagine</button>
        </section>
    </section>

    <output class="output-panel">
        {#each output_of_generated_objects.slice().reverse() as output }
            <OutputImageSection image={output.image} article={output.article} prompt={output.prompt} />
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

        background: rgb(var(--color-primary));
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

        background: rgb(var(--color-secondary));

        border-bottom: 2px solid rgb(var(--color-tertiary));

        text-align: left;
    }

    .input-panel {
        grid-row: 2;
        grid-column: 1;

        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        gap: -0.5em;

        width: fit-content;
        height:100%;

        box-sizing: border-box;

        border-right: 2px solid rgb(var(--color-tertiary));
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

        background: rgb(var(--color-secondary));

        border: 1px solid rgb(var(--color-tertiary));
        border-radius: var(--border-radius);
    }

    .article-textarea::placeholder {
        color: rgba(var(--color-text), 0.5);

        font-family: 'Roboto Mono', monospace;
        font-weight: 300;
        font-size: 0.9em;
    }

    .article-textarea:focus {
        border: 2px solid rgba(var(--color-text), 0.4);
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

        background: rgb(var(--color-primary));

        display: flex;
        flex-direction: column;

        box-sizing: border-box;
        overflow-y: scroll;
    }
</style>
