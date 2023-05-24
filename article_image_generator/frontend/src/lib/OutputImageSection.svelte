<script lang="ts">
    import LoaderIcon from "@lib/LoaderIcon.svelte";

    export let image = undefined;
    export let article = undefined;
    export let prompt = undefined;
</script>

<div class="output-image-section">
    <span class="output-prompt">
        <h3>Article: </h3>
        {#if article}
            <span>{article}</span>
        {:else}
            <span class="placeholder">
                Lorem ipsum, dolor sit amet consectetur adipisicing elit. Asperiores, reiciendis aliquid mollitia quia, ducimus iste voluptas inventore vero ipsam accusamus iure incidunt ullam numquam sequi. Odio ipsam iusto voluptate molestias optio. Necessitatibus, natus temporibus. Placeat consequuntur vitae ullam libero, quidem enim ipsa assumenda accusantium doloremque quibusdam odio.
            </span>
        {/if}

        <h3>Prompt: </h3>
        {#if prompt}
            <span>{prompt}</span>
        {:else}
            <span class="placeholder">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit repellat consequuntur dolore esse molestiae quia necessitatibus, deserunt harum repellendus quod.
            </span>
        {/if}
    </span>
    {#if image}
        <img class="output-image" src={image} alt="output" />
    {:else}
        <div class="image-placeholder output-image"><LoaderIcon/></div>
    {/if}

</div>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Flow+Circular&display=swap');

    h3 {
        margin: 0;
        color: var(--color-text);
    }

    .output-image-section {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;

        height: 20rem;

        box-sizing: border-box;

        background: var(--color-primary);
        border-bottom: 2px solid var(--color-tertiary);

        margin: 0.5em;
    }

    .output-prompt {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;

        width: 100%;
        height: 100%;

        font-size: 1em;
        font-weight: 600;

        color: var(--color-text);

        text-align: left;
        overflow-y: scroll;
        padding: 0 0.5em;

        box-sizing: border-box;
    }

    .output-image {
        height: 100%;

        margin: 0.5em;

        border-radius: var(--border-radius);
    }

    .image-placeholder {
        height: 20rem;
        aspect-ratio: 1/1;

        background: var(--color-text);

        border-radius: var(--border-radius);

        animation: blinking 2s infinite ease-in-out;

        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    @keyframes blinking {
        0% {
            background: rgba(var(--color-tertiary), 0.5);
        }

        40% {
            background: rgba(var(--color-tertiary), 1);
        }

        100% {
            background: rgba(var(--color-tertiary), 0.5);
        }
    }

    .placeholder {
        font-family: 'Flow Circular', cursive;
        color: var(--color-tertiary);
        font-size: 1.1em;
        margin-top: 0em;

        animation: blinking-text 2s infinite ease-in-out;

        user-select: none;
    }

    @keyframes blinking-text {
        0% {
            color: var(--color-tertiary);
        }

        40% {
            color: var(--color-primary);
        }

        100% {
            color: var(--color-tertiary);
        }
    }
</style>