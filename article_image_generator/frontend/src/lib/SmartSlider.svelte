<script lang="ts">
    export let value_min = 0;
    export let value_max = 100;
    export let value = Math.round(value_max / 2);
    export let slider_text = "Slider";
    export let disabled = false;
</script>

<div class="slider">
    <span>{slider_text}: {value}</span>
    <!--suppress HtmlWrongAttributeValue -->
    <input
        type="range"
        min="{value_min}"
        max="{value_max}"
        value="{value}"
        on:input={event => value = event.target.value}
        disabled="{disabled === true ? 'disabled' : ''}"
    />
</div>

<style>
    .slider {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;

        margin: 0.5em;
    }

    input[type=range] {
        -webkit-appearance: none;
        width: 100%;
        height: 10px;
        border-radius: 5px;
        background-color: var(--color-scrollbar);
        outline: none;
        margin: 0;
    }

    input[type=range]::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background-color: var(--color-secondary);
        cursor: pointer;
    }

    span {
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>

