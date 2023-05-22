<script lang="ts">
    import { onMount } from "svelte";
    
    import favicon from "@assets/favicon.ico";
    import Dropdown from "@lib/Dropdown.svelte";
    import OutputImageSection from "@lib/OutputImageSection.svelte";

    const tags = ["realistic", "cinematic", "cartoon", "sketch"];
    let image_look;
    let textarea_value: string = "";
    let outputs: Array<{image: string, article: string, prompt: string}> = [
        {
            image: "https://picsum.photos/512/512",
            article: "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Obcaecati praesentium, necessitatibus fugit tempora magni vero ea dignissimos. Eius, aperiam rerum quis dolore nisi repellendus sunt voluptatibus iste minima amet omnis.",
            prompt: "Lorem ipsum in many words"
        }
    ];

    async function textToImage(text:string): Promise<{ image_base64: string; prompt: string; confidence: number; }> {
        const obj = { 
            text_for_processing: text,
            image_look: image_look 
        };

        const request = new Request("/backend/text-to-image", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(obj),
        });

        const output = await fetch(request);
        const data = await output.json();
        return {
            image_base64: data.image_base64,
            prompt: data.prompt,
            confidence: data.confidence
        };
    }

    async function imagine() {
        outputs.push({
            image: undefined,
            article: textarea_value,
            prompt: undefined
        });
        outputs = outputs;

        textToImage(textarea_value).then((data) => {
            outputs[outputs.length - 1].image = `data:image/png;base64,${data.image_base64}`;
            outputs[outputs.length - 1].prompt = data.prompt;
            outputs = outputs;
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
        {#each outputs.slice().reverse() as output }
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
