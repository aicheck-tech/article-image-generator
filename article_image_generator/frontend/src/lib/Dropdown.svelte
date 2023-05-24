<script lang="ts">
    import { onMount } from "svelte";
    import MaskedIcon from "@lib/MaskedIcon.svelte";
    import arrow_forward from "@assets/icons/arrow_forward_fill.png";

    export let name: string;
    export let items: string[];
    export let icon: string = "https://picsum.photos/48/48";
    export let alt: string = "dropdown_icon";
    export let current_item_id: number;
    export let current_item = items[current_item_id];
    export let border_radius: Array<"top-left" | "top-right" | "bottom-left" | "bottom-right"> | ["all"];

    onMount(() => {
        document.getElementById("dropdown").setAttribute("tabindex", "0");
    });
</script>

<div class="dropdown border-radius-{border_radius.join(" border-radius-")}" id="dropdown">
    <div class="group">
        <MaskedIcon icon={icon} alt={alt} />
        <span class="dropdown-text"><b>{name}</b>:<br>{current_item}</span>
    </div>
    <MaskedIcon icon={arrow_forward} alt="arrow_forward" />
    <div class="dropdown-content">
        {#each items as item}
            <label class="tag">
                <input 
                    tabindex="0" 
                    type="radio" 
                    name={name} 
                    value={item} 
                    bind:group={current_item} 
                />
                {item}
            </label>
        {/each}
    </div>
</div>

<style>
    .group {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        gap: 0.5em;
        margin: 0 0.5em;
    }

    .dropdown-text {
        text-align: left;
        white-space: nowrap;
    }

    .dropdown {
        position: relative;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;

        padding-top: 0.75em;
        padding-bottom: 0.75em;

        border: 1px solid var(--color-tertiary);
    }

    .dropdown-content {
        display: none;
        position: absolute;
        left: 100%;
        top: 0%;

        padding: 0px;

        width: fit-content;
        min-width: 160px;
        box-sizing: border-box;

        background-color: var(--color-primary);
        border: 1px solid var(--color-tertiary);
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
        background-color: var(--color-tertiary);
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

    .border-radius-top-left {
        border-top-left-radius: var(--border-radius);
    }

    .border-radius-top-right {
        border-top-right-radius: var(--border-radius);
    }

    .border-radius-bottom-left {
        border-bottom-left-radius: var(--border-radius);
    }

    .border-radius-bottom-right {
        border-bottom-right-radius: var(--border-radius);
    }

    .border-radius-all {
        border-radius: var(--border-radius);
    }
</style>
