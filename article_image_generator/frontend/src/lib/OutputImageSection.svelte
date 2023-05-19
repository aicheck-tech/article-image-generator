<script lang="ts">
    import Loader from "./Loader.svelte";

    export let image = undefined;
</script>

<div class="output-image-section">
    <span class="output-prompt">
        <h3>Prompt: </h3>
        <slot name="prompt">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Asperiores, reiciendis aliquid mollitia quia, ducimus iste voluptas inventore vero ipsam accusamus iure incidunt ullam numquam sequi. Odio ipsam iusto voluptate molestias optio. Necessitatibus, natus temporibus. Placeat consequuntur vitae ullam libero, quidem enim ipsa assumenda accusantium doloremque quibusdam odio, aut dolor rerum, voluptate corporis ipsam alias modi temporibus ut distinctio neque id cupiditate totam. Atque voluptate optio ullam molestias sequi odit eos praesentium, at quidem debitis neque voluptatem unde sunt ipsum adipisci quisquam ad porro dolor quia accusantium nulla aperiam exercitationem quae tenetur? Voluptatibus blanditiis laborum debitis velit natus possimus quo sapiente temporibus eum. Corporis error impedit voluptas ab fugiat illum, repellendus maiores quia rerum modi, nam mollitia, hic pariatur. Similique molestias, ut, architecto molestiae libero dolores quam ipsa repudiandae consectetur eius rem? Voluptatum asperiores error quos dolore ex amet fuga eum ipsum animi qui reprehenderit quasi earum, dolorum vero? Eveniet, quisquam.</slot>
    </span>
    {#if image}
        <img class="output-image" src={image} alt="output" />
    {:else}
        <div class="image-placeholder output-image"><Loader/></div>
    {/if}
</div>

<style>
    h3 {
        margin: 0;
        color: rgba(var(--color-text), 0.8);
    }

    .output-image-section {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;

        height: 20rem;

        box-sizing: border-box;

        background: rgb(var(--color-primary));
        border-bottom: 2px solid rgb(var(--color-tertiary));

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

        color: rgba(var(--color-text), 0.5);

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

        background: rgba(var(--color-text), 0.1);

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
</style>