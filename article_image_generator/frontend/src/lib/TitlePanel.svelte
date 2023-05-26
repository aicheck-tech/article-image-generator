<script lang="ts">
    import MaskedIcon from "@lib/MaskedIcon.svelte";
    import github_icon from "@assets/icons/github-mark.svg";
</script>

<section class="title-panel">
    <h1 class="font-primary">ARTIQ</h1>
    <a href="https://github.com/aicheck-tech/article-image-generator" target="_blank" class="icon-wrappers">
        <MaskedIcon icon={github_icon} alt="favicon" />
    </a>
</section>

<style>
    .title-panel {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: 0.5em;
        padding-bottom: 0;
        height: 4rem;

        border-bottom: 2px solid var(--color-secondary);
    }

    .icon-wrappers {
        width: 2.5rem;
        height: 2.5rem;

        margin-bottom: 0.25em;
    }
</style>