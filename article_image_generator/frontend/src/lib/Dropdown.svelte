<script lang="ts">
    import { onMount } from "svelte";
    import MaskedIcon from "@lib/MaskedIcon.svelte";
    import arrow_forward from "@assets/icons/arrow_forward_fill.png";
    import check_icon from "@assets/icons/check_fill.svg";

    export let name: string;
    export let items: string[];
    export let icon: string = "https://picsum.photos/48/48";
    export let alt: string = "dropdown_icon";
    export let current_item_id: number;
    export let current_item: string | string[] = items[current_item_id];
    export let input_type: "radio" | "checkbox" = "radio";

    let dropdown_active: boolean = false;

    function switcher() {
        dropdown_active = !dropdown_active;
    }

    onMount(() => {
        document.getElementById("dropdown").setAttribute("tabindex", "0");
    });
</script>

<div class="dropdown" id="dropdown" data-active={dropdown_active}>
    <div class="dropdown-info" on:mousedown={switcher}>
        <div class="dropdown-info-text">
            <div class="icon-wrapper">
                <MaskedIcon icon={icon} alt={alt} />
            </div>
            <span class="dropdown-text">
                <p class="font-secondary-bold">{name}:</p>
                <p class="font-secondary-regular">{current_item}</p>
            </span>
        </div>
        <div class="icon-wrapper arrow_forward">
            <MaskedIcon icon={arrow_forward} alt="arrow_forward" />
        </div>
    </div>
    <div class="dropdown-content">
        {#each items as item}
            <label class="input-wrapper font-secondary-regular">
                {#if input_type === "checkbox"}
                    <input 
                        tabindex="0" 
                        type="checkbox"
                        name={name} 
                        value={item} 
                        bind:group={current_item} 
                    />
                {:else}
                    <input 
                        tabindex="0" 
                        type="radio"
                        name={name} 
                        value={item} 
                        bind:group={current_item} 
                    />
                {/if}
                <span class="checkmark"></span>

                {item}
            </label>
        {/each}
    </div>
</div>

<style>
    p {
        margin: 0;
    }
    .dropdown {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        width: 100%;
        box-sizing: border-box;

        background-color: var(--color-primary);
    }

    .dropdown-info {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;

        width: 100%;
        box-sizing: border-box;

        white-space: nowrap;

        user-select: none;
        cursor: pointer;
    }

    .dropdown-info-text {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;

        width: 100%;
        box-sizing: border-box;

        padding: 0.5em;

        text-align: left;
    }
    
    .dropdown-content {
        display: none;
        
        left: 0;
        top: 100%;

        padding-left: 4em;

        width: 100%;
        height: fit-content;

        box-sizing: border-box;
    }

    .input-wrapper {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;

        cursor: pointer;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }

    .input-wrapper input {
        position: absolute;
        opacity: 0;
        cursor: pointer;
        height: 0;
        width: 0;
    }

    .checkmark {
        position: relative;
        top: 0;
        left: 0;
        
        width: 0.8em;
        height: 0.8em;
        margin-right: 0.25em;

        border-radius: 0.25em;

        border: 2px solid var(--color-secondary);

        box-sizing: border-box;
    }

    .input-wrapper:hover input ~ .checkmark {
        background-color: var(--color-text-lighter);
    }

    .input-wrapper input:checked ~ .checkmark {
        background-color: var(--color-secondary);
    }

    .dropdown[data-active = "true"] .dropdown-content {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;

        transform-origin: top left;

        animation: growDown 150ms ease-in-out;
    }

    .dropdown[data-active = "true"] .arrow_forward {
        transform: rotate(90deg);
    }

    .dropdown .arrow_forward {
        transition: 150ms ease-in-out;
    }

    @keyframes growDown {
        0% {
            transform: scaleY(0);
        }
        100% {
            transform: scaleY(1);
        }
    }
</style>
