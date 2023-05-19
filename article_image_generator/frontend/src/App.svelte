<script lang="ts">
    import { onMount } from "svelte";

    import Dropdown from "./lib/Dropdown.svelte";
    import ResizableArea from "./lib/ResizableArea.svelte";

    import favicon from "./assets/favicon.ico";

    var link = document.querySelector("link[rel~='icon']");
    if (!link) {
        link = document.createElement("link");
        link.rel = "icon";
        document.head.appendChild(link);
    }
    link.href = `${favicon}`;

    const tags = ["realistic", "cinematic", "cartoon", "sketch"];
    let default_item = 0;

    let left;
    let resizer;
    let container;
    let x = 0;
    let y = 0;
    let leftWidth = 0;
    const MINWIDTH = 50;

    const mouseDownHandler = (e) => {
        x = e.clientX;
        y = e.clientY;
        leftWidth = left.getBoundingClientRect().width;

        document.addEventListener("mousemove", mouseMoveHandler);
        document.addEventListener("mouseup", mouseUpHandler);
    };

    const mouseMoveHandler = (e) => {
        const dx = e.clientX - x;
        const newLeftWidth =
            ((leftWidth + dx) * 100) /
            resizer.parentNode.getBoundingClientRect().width;
        left.style.width = `${newLeftWidth}%`;
    };

    const mouseUpHandler = () => {
        resizer.style.removeProperty("cursor");
        document.body.style.removeProperty("cursor");
        left.style.removeProperty("user-select");
        left.style.removeProperty("pointer-events");

        document.removeEventListener("mousemove", mouseMoveHandler);
        document.removeEventListener("mouseup", mouseUpHandler);
    };

    onMount(() => {
        left = document.querySelector(".input-area");
        resizer = document.querySelector(".resize-bar");
        container = document.querySelector(".input-section");

        resizer.addEventListener("mousedown", mouseDownHandler);

        return () => {
            resizer.removeEventListener("mousedown", mouseDownHandler);
            document.removeEventListener("mousemove", mouseMoveHandler);
            document.removeEventListener("mouseup", mouseUpHandler);
        };
    });
</script>

<main>
    <section class="title-section">
        <h1>Article image generator</h1>
        <h2>Generate images for articles</h2>
    </section>
    <section class="input-section">
        <section class="input-area">
            <textarea class="resizable-textarea" />
            
            <Dropdown default_item={default_item} tags={tags} />

            <button>Imagine</button>
        </section>
        <div class="resize-bar" id="resize" />
    </section>
</main>

<style>
    main {
        display: grid;
        grid-template-rows: fit-content(1ch) 1fr;
        grid-template-columns: 1fr 1fr;

        width: 100vw;
        height: 100vh;

        background: rgb(var(--color-primary));
    }

    button {
        border-radius: 0;
    }

    .title-section {
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

    .input-section {
        grid-row: 2;
        grid-column: 1;

        width: 100%;
        height: 100%;

        min-width: 10em;

        display: flex;
        flex-direction: row;
    }

    .input-area {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;

        min-width: 12em;
        max-width: 25em;
        width: 20em;

        box-sizing: border-box;
    }

    .input-area > * {
        box-sizing: border-box;
    }


    .input-section > * {
        box-sizing: border-box;
    }

    .resize-bar {
        width: 2px;
        height: 100%;

        cursor: col-resize;

        background: rgba(var(--color-tertiary), 0.5);

        transition: 0.2s ease-in-out;
    }

    .resizable-textarea {
        width: 100%;

        min-height: 4em;
        max-height: 40em;

        height: 50%;

        resize: vertical;
    }
</style>
