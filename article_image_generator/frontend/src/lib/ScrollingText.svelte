<script lang="ts">

</script>

<div id="scroll-container">
    <div id="scroll-text">
        <slot></slot>
    </div>
</div>

<style>
    #scroll-container {
        border: 3px solid black;
        border-radius: 5px;
        overflow: hidden;
    }

    #scroll-text {
        /* animation properties */
        -moz-transform: translateX(100%);
        -webkit-transform: translateX(100%);
        transform: translateX(100%);

        -moz-animation: my-animation 15s linear infinite;
        -webkit-animation: my-animation 15s linear infinite;
        animation: my-animation 15s linear infinite;
    }

    /* for Firefox */
    @-moz-keyframes my-animation {
        from { -moz-transform: translateX(100%); }
        to { -moz-transform: translateX(-100%); }
    }

    /* for Chrome */
    @-webkit-keyframes my-animation {
        from { -webkit-transform: translateX(100%); }
        to { -webkit-transform: translateX(-100%); }
    }

    @keyframes my-animation {
        from {
            -moz-transform: translateX(100%);
            -webkit-transform: translateX(100%);
            transform: translateX(100%);
        }
        to {
            -moz-transform: translateX(-100%);
            -webkit-transform: translateX(-100%);
            transform: translateX(-100%);
        }
    }
</style>