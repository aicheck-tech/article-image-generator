<script lang="ts">
    import { onMount } from "svelte";

    export let default_item: string;
    export let tags: string[];
    export let border_radius: string = "var(--border-radius)";

    import arrow_forward from "../assets/icons/arrow_forward_fill.png";
    import design_services from "../assets/icons/design_services_fill.png";
    
    let current_tag = tags[default_item];
    let dropdown;

    onMount(() => {
        dropdown.setAttribute("tabindex", "0");
        const dropdown_content:HTMLDivElement = dropdown.querySelector(".dropdown-content");

    });
</script>

<div class="dropdown" bind:this={dropdown} style="border-radius: {border_radius};">
    <div class="group">
        <img src={design_services} alt="design_services" />
        <span>Look: {current_tag}</span>
    </div>
    <img src={arrow_forward} alt="arrow_forward" />
    <div class="dropdown-content">
        {#each tags as tag}
            <label class="tag">
                <input tabindex="0" type="radio" name="tags" value={tag} bind:group={current_tag} />
                {tag}
            </label>
        {/each}
    </div>
</div>

<style>
    img {
        height: 1.5em;
        margin-right: 0.25em;
    }

    .group {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        gap: 0.5em;
        margin: 0 0.5em;
    }

    .dropdown {
        position: relative;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;

        padding-top: 0.75em;
        padding-bottom: 0.75em;

        border: 2px solid rgb(var(--color-tertiary));
    }

    .dropdown-content {
        display: none;
        position: absolute;
        left: 100%;
        top: -100%;

        padding: 0px;

        width: 75%;
        min-width: 160px;
        box-sizing: border-box;

        background-color: rgb(var(--color-primary));
        border: 1px solid rgb(var(--color-tertiary));
        border-radius: var(--border-radius);

        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
        z-index: 10;

        transition: 150ms ease-out;
    }

    .dropdown:hover .dropdown-content {
        display: block;

        animation: growDown 150ms ease-in-out forwards;
        transform-origin: top left;
    }

    .dropdown:focus .dropdown-content {
        display: block;

        animation: growDown 150ms ease-in-out forwards;
        transform-origin: top left;
    }   

    .tag {
        display: block;
        width: 100%;
        box-sizing: border-box;

        padding: 0.5em;
        margin: 0px;

        border-radius: var(--border-radius);

        text-align: left;
        text-decoration: none;
        font-size: 1em;
        cursor: pointer;
    }

    .tag:hover {
        background-color: rgb(var(--color-tertiary));
    }

    @keyframes growDown {
        0% {
            transform: scaleX(0);
        }
        80% {
            transform: scaleX(1.1);
        }
        100% {
            transform: scaleX(1);
        }
    }
</style>