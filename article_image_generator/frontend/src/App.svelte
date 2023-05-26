<script lang="ts">
    import { onMount } from "svelte";

    import favicon from "@assets/favicon.ico";
    import Dropdown from "@lib/Dropdown.svelte";
    import OutputImageSection from "@lib/OutputImageSection.svelte";
    import ContactSection from "@lib/ContactSection.svelte";
    import { textToImage } from "@scripts/api-calls";

    import design_services_icon from "@assets/icons/design_services_fill.png";
    import brush_icon from "@assets/icons/brush_fill.png";
    import github_icon from "@assets/icons/github-mark.svg";
    import MaskedIcon from "./lib/MaskedIcon.svelte";

    const tags = ["realistic", "cinematic", "cartoon", "sketch"];

    let image_look: string;
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
                    prompt: "Lorem ipsum ale jinde",
                    processing_method: "Key words",
                    visual_look: "realistic",
                    date: "2021-01-01",
                }
            ],
            article: "Lorem ipsum",
        },
    ];

    async function imagine(event) {
        event.target.disabled = true;

        output_of_generated_objects.push({
            images: [
                {
                    image_base64: "https://picsum.photos/512/512",
                    prompt: "Lorem ipsum ale jinde",
                    processing_method: "Key words",
                    visual_look: "realistic",
                    date: "2021-01-01",
                }
            ],
            article: textarea_value,
        });
        output_of_generated_objects = output_of_generated_objects;

        textToImage(textarea_value, image_look).then((data) => {
            console.log(data);
        });

        // textToImage(textarea_value, image_look).then((data) => {
        //     output_of_generated_objects[
        //         output_of_generated_objects.length - 1
        //     ].images[0].image_base64 = `data:image/png;base64,${data.image_base64}`;
        //     output_of_generated_objects[
        //         output_of_generated_objects.length - 1
        //     ].images[0].prompt = data.prompt;
        //     output_of_generated_objects = output_of_generated_objects;

        //     event.target.disabled = false;
        // });
    }

    onMount(() => {
        let link = document.getElementById("favicon") as HTMLLinkElement;
        link.href = favicon;
    });
</script>

<main>
    <section class="title-panel">
        <h1>ARTIQ</h1>
        <a href="https://github.com/aicheck-tech/article-image-generator" target="_blank" class="icon-wrapper">
            <MaskedIcon icon={github_icon} alt="favicon" />
        </a>
    </section>

    <div class="body-wrapper">
        <section class="input-panel">
            <textarea
                bind:value={textarea_value}
                class="article-textarea font-secondary-regular"
                placeholder="Insert you article here..."
            />

            <Dropdown
                name="Processing method"
                current_item_id={0}
                items={["Key words", "Summarization"]}
                icon={design_services_icon}
                input_type="checkbox"
            />
            <Dropdown
                name="Look"
                current_item_id={0}
                items={tags}
                bind:current_item={image_look}

                icon={brush_icon}
            />
            <button on:click={imagine}>
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
            <h2 class="font-primary">Info</h2>
            <p class="font-secondary-regular color-text-lighter">Lorem ipsum dolor sit amet consectetur, adipisicing elit. Sit suscipit provident tenetur accusantium esse dolores sunt earum. Doloribus, consequuntur ipsa!</p>
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

    h1 {
        margin: 0;
    }

    .title-panel {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: 0.5em;
        padding-bottom: 0;
        height: 4rem;

        border-bottom: 2px solid var(--color-secondary);
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

        /* border-right: 2px solid var(--color-secondary); */
    }

    .output-panel {
        width: 100%;

        flex: calc(1 / 2);

        overflow-y: scroll;
    }

    .info-panel {
        flex: calc(1 / 4);

        width: 100%;
    }

    .article-textarea {
        max-height: 70%;
        min-height: 15em;

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
</style>

