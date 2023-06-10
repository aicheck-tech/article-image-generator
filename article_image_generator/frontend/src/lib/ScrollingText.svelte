<script lang="ts">

</script>

<div id="scroll-container">
    <div id="scroll-text">
        <slot></slot>
    </div>
</div>

<style>
    #scroll-container {
        border-left: 2px solid black;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;

        box-sizing: border-box;
    }

    #scroll-text {
        /* animation properties */
        -moz-transform: translateX(0%);
        -webkit-transform: translateX(0%);
        transform: translateX(0%);

        -moz-animation: my-animation 15s linear infinite;
        -webkit-animation: my-animation 15s linear infinite;
        animation: my-animation 15s linear infinite;
    }

    /* for Firefox */
    @-moz-keyframes my-animation {
        from { -moz-transform: translateX(0%); }
        to { -moz-transform: translateX(-100%); }
    }

    /* for Chrome */
    @-webkit-keyframes my-animation {
        from { -webkit-transform: translateX(0%); }
        to { -webkit-transform: translateX(-100%); }
    }

    @keyframes my-animation {
        0% {
            -moz-transform: translateX(0%);
            -webkit-transform: translateX(0%);
            transform: translateX(0%);
        }
        5% {
            -moz-transform: translateX(0%);
            -webkit-transform: translateX(0%);
            transform: translateX(0%);
        }
        100% {
            -moz-transform: translateX(-100%);
            -webkit-transform: translateX(-100%);
            transform: translateX(-100%);
        }
    }
</style>